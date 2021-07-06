import discord
from discord.ext import commands, menus

from core.utils import format_time
from core.enums import Emoji, Color

import aiohttp
import json
import time
import asyncio
from datetime import datetime
from ytpy import YoutubeClient


class PaginateUrban(menus.ListPageSource):
    def __init__(self, data):
        self.data = data
        super().__init__(data, per_page=1)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        
        embed= discord.Embed(title=f":question: {entries['word']}",
         color=Color.neutral,
         url= entries['permalink'],
         description=entries['definition'],


         )
        embed.set_footer(text=f'Page {self.data.index(entries)+1}/{len(self.data)}')    
        
        embed.add_field(name="Example", value=entries['example'], inline=False)
        embed.add_field(name="Author", value=entries['author'], inline=False)
        embed.add_field(name="Reactions", value= f":+1: {entries['thumbs_up']} :-1: {entries['thumbs_down']}", inline=False)        
        
        return embed

class Utility(commands.Cog, name="utility", description="These are some of the commands to ease your life on discord. {} :billed_cap:".format(Emoji.error)):
    def __init__(self, bot):
        self.bot = bot
        self.bot.afks = {}
        self.deleted_messages = {}
        self.edited_messages  = {}


    @commands.command(
        help="Sets an AFK message that will be shown to anyone who mentions you. Useful to tell your friends that you are AFK.",
        description="`message` (Optional): The AFK message, Defaults to \"I'm AFK right now\"",
        brief='/utility/afk',
        usage='afk [message]'
        )
    @commands.guild_only()
    async def afk(self, ctx, *, message = "{user} is AFK."):
        if str(ctx.author.id) in self.bot.afks:
            pass
        else:
            self.bot.afks[str(ctx.author.id)] = {}

        self.bot.afks[str(ctx.author.id)][str(ctx.guild.id)] = {}
        self.bot.afks[str(ctx.author.id)][str(ctx.guild.id)]['message'] = message
        self.bot.afks[str(ctx.author.id)][str(ctx.guild.id)]['set_on'] = format_time(datetime.utcnow())
        await ctx.send(Emoji.success+" Set your AFK message to: **{}**\n\nThis will be removed when you send a message again.".format(message))

    @commands.command(
        help="Shows info about the server.",
        description="This command takes no arguments",
        brief='/utility/info',
        usage='serverinfo'
        )
    async def serverinfo(self, ctx):
        name = ctx.guild.name

        owner = ctx.guild.owner
        guild_id = ctx.guild.id
        region = ctx.guild.region
        member_count = ctx.guild.member_count
        verification_level = ctx.guild.verification_level
        created_at = str(ctx.guild.created_at.replace(microsecond=0))
        bots_count = len([x for x in ctx.guild.members if x.bot])
        notify = str(ctx.guild.default_notifications).split('NotificationLevel.')

        icon = str(ctx.guild.icon_url)

        embed = discord.Embed(
            title=f":globe_with_meridians: __Info for {name}__",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name=":gear: __Internal Information__", value=f"Verification level: `{str(verification_level).upper()}`\nRegion: `{str(region).upper()}`\nServer ID: `{ctx.guild.id}`\nAFK Timeout: `{ctx.guild.afk_timeout}s`\nNotifications Level: `{str(notify[1]).upper()}`", inline=False)
        embed.add_field(name=":1234: __Counters__", value=f"Member Count: `{member_count}`\nBots Count: `{bots_count}`\nCategories Count: {len(ctx.guild.categories)}\nText Channels Count: `{len(ctx.guild.text_channels)}`\nVoice Channels Count: `{len(ctx.guild.voice_channels)}`\nBoosts Count: `{ctx.guild.premium_tier}`\nRoles Count: `{len(ctx.guild.roles)}`", inline=False)
        embed.add_field(name=":electric_plug: __Channel Statistics__", value=f"AFK Channel: `{str(ctx.guild.afk_channel)}`\nSystem Channel: `{str(ctx.guild.system_channel)}`\nCommunity Rules Channels: `{str(ctx.guild.rules_channel)}`\n")
        embed.add_field(name=":name_badge: __Other Information__", value=f"Owner: `{owner.name}#{owner.discriminator}`\nCreated At: `{created_at}`", inline=False)
        embed.add_field(name=":link: __URLs (If available)__", value=f"[Server Icon]({ctx.guild.icon_url})\n[Banner Icon]({ctx.guild.banner_url})\n[Splash URL]({ctx.guild.splash_url})", inline=False)
        

        await ctx.send(embed=embed)

    @commands.command(
        help="Shows info about an emoji.",
        description="`emoji` (Optional): The emoji to show info of.",
        brief='/utility/info',
        usage='emojiinfo <emoji>'
        )
    async def emojiinfo(self, ctx, emoji: discord.Emoji = None):
        if emoji == None:
            await ctx.send(Emoji.info+" Specify the emoji you want info about.")
            return

        embed = discord.Embed(title=":grin: Emoji Info", description=f"Info about {str(emoji)}", color=Color.neutral)
        embed.add_field(name=":gear: Basic Information", value=f"Animated?: `{'YES' if emoji.animated else 'NO'}`\nAvailable?: `{'YES' if emoji.available else 'NO'}`\nID: `{emoji.id}`", inline=False)
        embed.add_field(name=":1234: Other Information", value=f"Created at: `{time.ctime(emoji.created_at.timestamp())} UTC`\nServer: `{emoji.guild.name}`", inline=False)
        embed.add_field(name=":link: URLs (If available)", value=f"[Emoji]({emoji.url})", inline=False)
        embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=embed)

    @commands.command(
        help="Shows info about an invite.",
        description="`invite` (Optional): The invite to show info of.",
        brief='/utility/info',
        usage='inviteinfo <invite>',
        aliases=['invinfo']

        )
    async def inviteinfo(self, ctx, invite: discord.Invite = None):
        if invite == False:
            await ctx.send(Emoji.info+" Specify the invite you want info about.")
            return

        embed = discord.Embed(title=":e_mail: Invite Info", description=f"Info about discord.gg/{invite.code}", color=Color.neutral)
        embed.add_field(name="Server", value=invite.guild.name, inline=False)
        embed.add_field(name="Total Members", value=invite.approximate_member_count, inline=False)
        embed.add_field(name="Online Members", value=invite.approximate_presence_count, inline=False)
        embed.add_field(name="For channel", value=invite.channel.name, inline=False)
        embed.add_field(name="Invite Code", value=invite.code, inline=False)
        embed.add_field(name="Inviter", value=invite.inviter.name+"#"+invite.inviter.discriminator, inline=False)
        embed.add_field(name="Invite Maximum Age", value=invite.max_age, inline=False)
        embed.add_field(name="Invite Maximum Uses", value=invite.max_uses, inline=False)
        if invite.uses == None:
            uses = "0"
        else:
            uses = str(invite.uses)

        embed.add_field(name="Invite Used", value=uses+" times", inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        help="Shows info about a user.",
        description="`user` (Optional): The user who's info should be showed.",
        brief='/utility/info',
        usage='userinfo [user]',
        aliases=['whois']

        )
    async def userinfo(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        embed = discord.Embed(
            title=f":globe_with_meridians: __Info for {user.name}#{user.discriminator}__",
            color=discord.Color.blue()
        )
        if user.premium_since != None:
            boosting = 'TRUE'
        else: 
            boosting = 'FALSE'

        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name=":gear: __Internal Information__", value=f"BOT?: `{str(user.bot).upper()}`\nColor: `{str(user.color.to_rgb())}`\nID: `{user.id}`\nAnimated Avatar?: `{str(user.is_avatar_animated()).upper()}`\nBoosting?: `{boosting}`", inline=False)
        embed.add_field(name=":1234: __Dates__", value=f"Created at: `{time.ctime(user.created_at.timestamp())}`\nJoined at: `{time.ctime(user.joined_at.timestamp())}`\nBoosting Since: {time.ctime(user.premium_since.timestamp()) if user.premium_since != None else '`Not boosting`'}\nCurrent Voice Channel: `{user.voice.channel.name if user.voice != None else 'No channel'}`\n", inline=False)
        embed.add_field(name=":link: __URLs (If available)__", value=f"[Avatar]({user.avatar_url})", inline=False)
        roles = user.roles
        uroles = ''
        for i in roles:
            uroles = uroles+' '+i.mention

        if len(uroles) > 500:
            uroles = "Too many roles to show."

        embed.add_field(name=":name_badge: __Roles__", value=uroles, inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        help="Shows the bot's latency.",
        description="This command takes no arguments.",
        brief='/utility/misc',
        usage='ping',
        aliases=['latency']

        )
    async def ping(self, ctx):
        await ctx.send(f":ping_pong: Pong!\n**Bot latency:** {round(self.bot.latency * 1000)}ms")

    @commands.command(
        help="Searchs urban dictionary for a term.",
        description="`term` (Required): The term to search for.",
        brief='/utility/searches',
        usage='urban <term>',
        aliases=['urb']

        )
    async def urban(self, ctx, *, term=None):
        if term == None:
            await ctx.send(Emoji.info+" Provide the term to search for.")
            return

        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term":term}
        headers = {
        'x-rapidapi-key': self.bot.config.nsfw_detection_api_key,
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
        }
        async with aiohttp.ClientSession() as session:

            response = await session.get(url, headers=headers, params=querystring)

        j = await response.json()
        pages = menus.MenuPages(source=PaginateUrban(j['list']), clear_reactions_after=True)
        await pages.start(ctx)

    @commands.command(
        help="Searchs YouTube for provided term.",
        description="`term` (Required): The term to search for.",
        brief='/utility/searches',
        usage='youtube <term>',
        aliases=['yt']

        )
    async def youtube(self, ctx, *, query=None):
        if query == None:
            await ctx.send(Emoji.info+" Please provide a search term.")
            return

        session = aiohttp.ClientSession()
        client = YoutubeClient(session)
        response = await client.search(query, max_results=5)
        await session.close()
        titles = []
        e = 0
        for i in response:
            e += 1
            titles.append(f'`{e}`. [{i["title"]}](https://www.youtube.com/watch?v='+i["id"]+')'+'\n')
        
        embed = discord.Embed(title=f"Fetched {len(titles)} results from YouTube.", 
            description=''.join(titles), color=Color.error
            )
        await ctx.send(embed=embed)

    @commands.command(
        help="Shows a random quote.",
        description="This command takes no arguments",
        brief='/utility/misc',
        usage='quote'
        )
    async def quote(self, ctx):
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://zenquotes.io/api/random")
            json_data = json.loads(await response.text())
            quote = json_data[0]['q'] + " -" + json_data[0]['a']
            
        await ctx.send(quote)

    @commands.command(
        help="Shows the last deleted message of channel.",
        description="This command takes no arguments",
        brief='/utility/messages',
        usage='showdelete'
        )
    async def showdelete(self, ctx):
        try:
            deleted_message = self.deleted_messages[str(ctx.guild.id)][str(ctx.channel.id)]
        except KeyError:
            await ctx.send("No deleted message found. :thinking_face:")
            return
        embed = discord.Embed()
        author = ctx.guild.get_member(deleted_message['author'])
        embed.set_author(name=str(author), icon_url=author.avatar_url)
        embed.color = ctx.author.color
        embed.description = deleted_message['message']
        await ctx.send(embed=embed)

    @commands.command(
        help="Shows the last deleted message of channel.",
        description="This command takes no arguments",
        brief='/utility/messages',
        usage='showedit'
        )
    async def showedit(self, ctx):
        try:
            edited_message = self.edited_messages[str(ctx.guild.id)][str(ctx.channel.id)]
        except KeyError:
            await ctx.send("No edited message found. :thinking_face:")
            return
        embed = discord.Embed()
        author = ctx.guild.get_member(edited_message['author'])
        embed.set_author(name=str(author), icon_url=author.avatar_url)
        embed.color = ctx.author.color
        embed.description = edited_message['message']
        await ctx.send(embed=embed)

    

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or isinstance(message.channel, discord.DMChannel):
            return

        if len(message.mentions) > 0:
            for mention in message.mentions:
                if str(mention.id) in self.bot.afks:
                    try:
                        afk_data = self.bot.afks[str(mention.id)][str(message.guild.id)]
                        await message.channel.send("{} ({})".format(afk_data['message'], afk_data['set_on']))
                    except KeyError:
                        return
        if str(message.author.id) in self.bot.afks:
            if str(message.guild.id) in self.bot.afks[str(message.author.id)]:
                self.bot.afks[str(message.author.id)].pop(str(message.guild.id))
                await message.channel.send(message.author.mention+" Your AFK has been removed. :ok_hand:")

                if self.bot.afks[str(message.author.id)] == {}:
                    self.bot.afks.pop(str(message.author.id))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        config = await self.bot.mongo.fetch_one_with_id(message.guild.id, database='guilds_config', collection='behaviour')
        if config['track_deletes'] == True:
            if not str(message.guild.id) in self.deleted_messages:
                self.deleted_messages[str(message.guild.id)] = {}
            
            self.deleted_messages[str(message.guild.id)] = {}
            self.deleted_messages[str(message.guild.id)][str(message.channel.id)] = {}
            self.deleted_messages[str(message.guild.id)][str(message.channel.id)]['message'] = message.content
            self.deleted_messages[str(message.guild.id)][str(message.channel.id)]['author'] = message.author.id
            
            await asyncio.sleep(30)

            self.deleted_messages[str(message.guild.id)].pop(str(message.channel.id))
            if self.deleted_messages[str(message.guild.id)] == {}:
                self.deleted_messages.pop(str(message.guild.id))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            config = await self.bot.mongo.fetch_one_with_id(before.guild.id, database='guilds_config', collection='behaviour')
            if config['track_edits'] == True:
                if not str(before.guild.id) in self.edited_messages:
                    self.edited_messages[str(before.guild.id)] = {}
                
                self.edited_messages[str(before.guild.id)] = {}
                self.edited_messages[str(before.guild.id)][str(before.channel.id)] = {}
                self.edited_messages[str(before.guild.id)][str(before.channel.id)]['message'] = before.content
                self.edited_messages[str(before.guild.id)][str(before.channel.id)]['author'] = before.author.id
                
                await asyncio.sleep(30)

                self.edited_messages[str(before.guild.id)].pop(str(before.channel.id))
                if self.edited_messages[str(before.guild.id)] == {}:
                    self.edited_messages.pop(str(before.guild.id))

        



def setup(bot):
    bot.add_cog(Utility(bot))