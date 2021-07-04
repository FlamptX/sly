import discord
from discord.ext import commands, menus

import asyncio
import random
import aiohttp

from core import utils
from core.enums import Emoji, Color, NSFWStatus


class PaginateConfessionChannelMenu(menus.ListPageSource):
    def __init__(self, data, per_page=8):
        self.data = data
        super().__init__(data, per_page=per_page)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=f"Select the server", color=Color.neutral)
        
        for entry in entries:
            embed.add_field(name=entry.name, value='Respond with `{}` to post confession in {}'.format(self.data.index(entry)+1, entry.name), inline=False)
        
        return embed

class Confessions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_confessions_config(self, guild):
        check = await self.bot.mongo.fetch_one_with_id(guild.id, database='guilds_config', collection='confessions')
        if check == None:
            return False
        else:
            return check

    async def get_eligible_guilds(self, member):
        mutual   = [guild for guild in self.bot.guilds if member in guild.members]
        eligible = []
        for guild in mutual:
            config = await self.get_confessions_config(guild)

            if config: # staircase code goes weeeeeeeeeeeeeee
                if config['toggle'] == 1 and not member.id in config['blacklist']:
                    eligible.append(guild)

        return eligible

    async def detect_nsfw(self, content_url):
        url = self.bot.config.nsfw_detection_api

        payload = '{"url": "'+content_url+'"}'
        headers = {
            'content-type': "application/json",
            'x-rapidapi-key': self.bot.config.nsfw_detection_api_key,
            'x-rapidapi-host': "nsfw-image-classification1.p.rapidapi.com"
            }

        async with aiohttp.ClientSession() as session:
            response = await session.post(url, data=payload, headers=headers)

        if response.status == 200:
            json = await response.json()
            if round(json['NSFW_Prob']) == 1:
                return NSFWStatus.nsfw
            elif round(json['NSFW_Prob']) == 0:
                return NSFWStatus.not_nsfw
            else:
                return NSFWStatus.undetectable

        else:
            return NSFWStatus.undetectable


    @commands.command(
        help='Post a completely anonymous confession in the confession channel. This command only work in DMs!',
        brief='/confessions/posting',
        description='`confession` (Required): The confession to post. In favor of long message writers, This can be upto 4000 characters long.',
        usage='confess <message>'
        
        )
    async def confess(self, ctx, *, message=None):
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Keep your confessions private! This command only works in my DMs.")
            return

        if not message and len(ctx.message.attachments) <= 0:
            await ctx.send("You gotta specify a confession that you want to post or at least attach an image.")
            return

        if message:
            if len(message) > 4000:
                await ctx.send("Enthuasism is good but there's a 4000 characters limit, Shorten your confession!")
                return

        if len(ctx.message.attachments):
            image = ctx.message.attachments[0]
            if not image.content_type.startswith('image/'):
                await ctx.send("Hey you can only add images in your confessions.")
                return

        check_blacklist = await utils.evalsql(db='sqlite/blacklist.db', sql='SELECT * FROM confessions_users where user_id = ?', vals=(ctx.author.id,), fetch='one')
        if check_blacklist:
            embed = discord.Embed(title="You have been blacklisted", description="You have been blacklisted from using Sly's confessions as a result of breaking our rules. This blacklist may or may not be temporary. Please contact support for more info we don't share reasons here.", color=Color.error)
            await ctx.send(embed=embed)
            return

        msg = await ctx.send(Emoji.lookup+' Give me a moment while I look up for the servers where you can post confessions...\n\nIf it\'s taking long, You can do other things and I will notify you when it\'s done.')
        guilds = await self.get_eligible_guilds(ctx.author)
        await msg.delete()
        if len(guilds) == 0:
            embed = discord.Embed(title="No servers found", description="I cannot find any servers in which you can post a confessions. There are some potential causes:\n\n-- None of your servers has setup confessions in the server.\n-- You have been blacklisted from posting confessions.")
            embed.add_field(name="What can you do as a server member?", value="You can ask the server moderators of the server in which you want to post confessions. Most probably confessions might not be setup or disabled or you might be blacklisted.", inline=False)
            embed.add_field(name="What can you do as a server owner/moderator?", value="You can setup confessions in your server by using `sly config confessions setup` command.", inline=False)
            await ctx.send(embed=embed)
            return

        paginator = menus.MenuPages(source=PaginateConfessionChannelMenu(guilds), clear_reactions_after=True)
        await paginator.start(ctx)
        await ctx.send(Emoji.info+" Respond with the guild number in which you want to suggest, for example `1` for the first one or `2` for second one.")

        attempts = 0
        while True:
            try:
                response = await self.bot.wait_for('message', check=lambda message: all([message.author == ctx.author, message.channel == ctx.channel, message.content.isdigit()]), timeout=60)
            except asyncio.TimeoutError:
                await ctx.send(r"You changed your mind didn't you? Okay den. ¯\_(ツ)_/¯")
                return

            try:
                guild = guilds[int(response.content)-1]
            except IndexError:
                attempts += 1
                if attempts >= 5:
                    await ctx.send("You sent wrong response too many times. Try again bud.")
                    return

                await ctx.send("Apparently that number you provided isn't in the list... Try again")
                continue

            break

        guild_config = await self.get_confessions_config(guild)

        if len(ctx.message.attachments) >= 1:
            if any([guild_config['allow_images'], guild_config['allow_nsfw']]):
                pass
            else:
                await ctx.send("You cannot include images in your confessions for that server because moderators have disabled it. If you are a moderator, you can use `sly config confessions allow-images` command to allow images.")
                return

            image = ctx.message.attachments[0]

            if guild_config['allow_images'] and not guild_config['allow_nsfw']:
                check = await self.detect_nsfw(image.url)
                if check in [NSFWStatus.nsfw, NSFWStatus.undetectable]:
                    await ctx.send("Way too spicy there! The server you are trying to posting the confessions in does not allow NSFW images and according to my sources this image seems to be NSFW.")
                    return
                else:
                    pass

            elif guild_config['allow_images'] and guild_config['allow_nsfw']:
                pass
        else:
            image = None

        channel = guild.get_channel(guild_config['channel_id'])
        confession_id = random.randint(1000, 9999)

        embed = discord.Embed()
        embed.set_author(name="Confession #{}".format(confession_id))
        embed.description = message

        if guild_config['embed_color'] == 0:
            embed.color = discord.Color.random()
        else:
            embed.color = guild_config['embed_color']

        if image != None:
            embed.set_image(url=image.url)

        embed.set_footer(text='Use "report-confession" command to report this confession if it is offending.')
        await channel.send(embed=embed)
        await ctx.send("Kaboom! Your completely anonymous confession has been sent in <#{0.id}>.".format(channel))


def setup(bot):
    bot.add_cog(Confessions(bot))