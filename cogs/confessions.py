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

class Confessions(commands.Cog,
    name='confessions',
    description='Make confession channel and post completely anonymous confessions that neither moderators nor server owner can find out who posted.'
    ):
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
                if config['toggle'] == 1:
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
        description='`confession` (Required): The confession to post. In favor of long message writers, This can be upto 4000 characters long.\n`image` (Optional): The image to include in confessions. To include an image, target server must have confession images settings enabled using `sly image-confessions enable`',
        usage='confess <message> [image]'
        
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

        check_blacklist = await utils.evalsql(database='sqlite/blacklist.db', sql='SELECT * FROM confessions_users where user_id = ?', vals=(ctx.author.id,), fetch='one')
        if check_blacklist:
            embed = discord.Embed(title="You have been blacklisted", description="You have been blacklisted from using Sly's confessions as a result of breaking our rules. This blacklist may or may not be temporary. Please contact support for more info we don't share reasons here.", color=Color.error)
            await ctx.send(embed=embed)
            return

        msg = await ctx.send(Emoji.lookup+' Give me a moment while I look up for the servers where you can post confessions...\n\nIf it\'s taking long, You can do other things and I will notify you when it\'s done.')
        guilds = await self.get_eligible_guilds(ctx.author)
        await msg.delete()
        if len(guilds) == 0:
            embed = discord.Embed(title="Yikes! No servers found", description="I cannot find any servers in which you can post a confessions. The potential cause is, None of your servers has setup confessions in the server.")
            embed.add_field(name="What can you do as a server member?", value="You can ask the server moderators of the server to add Sly and setup confessions in which you want to post confessions.", inline=False)
            embed.add_field(name="What can you do as a server owner/moderator?", value="You can setup confessions in your server by adding Sly using `sly setup-confessions` command.", inline=False)
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
        if str(ctx.author.id) in guild_config['blacklist'].keys():
            await ctx.send(Emoji.error+" You are muted from posting confessions in that server, The confession that was used to mute you is: {} and same number can be used to unmute you, Contact a moderator on the cost of revealing that you posted that confession. Yikes.".format(guild_config['blacklist'][str(ctx.author.id)]))
            return

        if len(ctx.message.attachments) >= 1:
            if any([guild_config['allow_images'], guild_config['allow_nsfw']]):
                pass
            else:
                await ctx.send("You cannot include images in your confessions for that server because moderators have disabled it. If you are a moderator, you can use `sly images-confessions enable` command to allow images.")
                return

            image = ctx.message.attachments[0]

            if guild_config['allow_images'] and not guild_config['allow_nsfw']:
                check = await self.detect_nsfw(image.url)
                if check in [NSFWStatus.nsfw, NSFWStatus.undetectable]:
                    await ctx.send("Way too spicy there! The server you are trying to posting the confessions in does not allow NSFW images and according to my sources this image seems to be NSFW. If you are a server moderator, you can use `sly nsfw-confessions enable` command to allow NSFW confessions.")
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

        embed.set_footer(text='Use "mute-confession" command to mute rules-breaking confessions.')
        conf = await channel.send(embed=embed)
        await ctx.send("Kaboom! Your completely anonymous confession has been sent in <#{0.id}>.".format(channel))

        await utils.evalsql(
            database='sqlite/store.db',
            sql='INSERT INTO confessions VALUES(?, ?, ?, ?, ?, ?, ?)',
            vals=(conf.guild.id, ctx.author.id, conf.id, confession_id, str(message), utils.generate_uid(), str(None) if image == None else image.url)

            )

    @commands.command(name='setup-confessions',
        help=utils.createhelp('Sets up confession channel in the server.', '`MANAGE_SERVER`'),
        description="`channel` (optional): The channel to setup for confessions.",
        brief="/confessions/setup",
        usage="setup-confessions [channel]"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setupconfessions(self, ctx, channel: discord.TextChannel = None):
        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='confessions')

        if config != None:
            await ctx.send(Emoji.error+" Confessions are already setup in this server. Use `update-confessions-channel` to update the channel or use `help confessions` command to see list of all customisation command.")
            return

        if not channel:
            embed = discord.Embed(title="Setting up Confessions • Channel", description="Welcome to confessions setup menu, Real quick, Mention the text channel where your members will post the confessions.")
            init_message = await ctx.send(embed=embed)
            
            attempts = 0
            while True:
                response = await self.bot.wait_for('message', check=lambda message: all([message.channel == ctx.channel, message.author == ctx.author]), timeout=60)
                await init_message.delete()
                converter = commands.TextChannelConverter()
                try:
                    channel = await converter.convert(ctx, response.content)
                except commands.ChannelNotFound:
                    attempts += 1
                    await response.delete()
                    if attempts >= 5:
                        init_message = await ctx.send("You sent invalid response too many times, Run the command again to restart the setup.")
                        return

                    await ctx.send("Hey, I can't find that channel, Maybe you made a typo or I don't have permission to view that channel. Try again.")
                    continue

                break

        message = await ctx.send(Emoji.lookup+" Gimme a minute while I set up confessions in {}...".format(channel.mention))

        collection = self.bot.mongo['guilds_config']['confessions']
        
        post = {
            '_id': ctx.guild.id, 
            'channel_id': channel.id, 
            'embed_color': 0,
            'toggle': 1,
            'allow_nsfw': 0,
            'allow_images': 0,
            'blacklist': []
        }
        await collection.insert_one(post)

        embed = discord.Embed(
            title=Emoji.success+" Setup Complete",
            description="Confession are now setup in {0.mention} ! Members can use `sly confess` command in bot's DMs to post completely anonymous confessions.".format(channel)
            )
        embed.color = Color.success
        embed.add_field(
            name=Emoji.info+" Quick Tips to manage confessions",
            value="""Here are some quick tips for server moderators to properly manage confessions:\n\n-- Members with `MANAGE_MESSAGES` permissions can manage confessions.\n\n-- If a confession is breaking your rules, you can simply use `mute-confession` to mute that confession author without revealing the author.\n\n-- If a confession is really offending and break [bot's rules]({}/topics/rules) you can report it using `report-confession` command and we will take actions against that user."\n\n-- If things get too out of hand, Use the `disable-confessions` command to temporarily disable confessions, you can enable again using `enable-confessions` command.""".format(self.bot.config.docs))

        await message.edit(embed=embed, content=None)

    @commands.command(name='nsfw-confessions',
        help=utils.createhelp('Allows NSFW confessions in server\'s confessions channel.', '`MANAGE_CHANNELS`'),
        description="`mode` (Required): Can either be `enable` or `disable`",
        brief="/confessions/nsfw",
        usage="nsfw-confessions <mode>"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def nsfwconfessions(self, ctx, mode = None):
        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='confessions')

        if config == None:
            await ctx.send(Emoji.error+" Confessions are not setup in this server, Set them up first! Use `setup-confessions` command.")
            return

        replacers = {
            1: 'enabled',
            0: 'disabled'

        }

        if not mode in ['enable', 'disable']:
            await ctx.send(Emoji.info+" "+' NSFW confessions are currently '+replacers[config['allow_nsfw']]+'. Use `nsfw-confessions disable` or `nsfw-confessions enable` to change that.')
            return
            
        message = await ctx.send(Emoji.lookup+" Gimme a minute...")

        collection = self.bot.mongo['guilds_config']['confessions']
        
        post = {
            '_id': ctx.guild.id
        }
        update = {
            '$set': {
                'allow_nsfw': 1 if mode == 'enable' else 0
            }
        }
        await collection.update_one(post, update)

        await message.edit(content=Emoji.success+' NSFW confessions have been {}'.format('enabled' if mode == 'enable' else 'disabled'))

    @commands.command(name='image-confessions',
        help=utils.createhelp('Allows images confessions in server\'s confessions channel.', '`MANAGE_CHANNELS`'),
        description="`mode` (Required): Can either be `enable` or `disable`",
        brief="/confessions/images",
        usage="image-confessions <mode>"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def imageconfessions(self, ctx, mode = None):
        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='confessions')

        if config == None:
            await ctx.send(Emoji.error+" Confessions are not setup in this server, Set them up first! Use `setup-confessions` command.")
            return

        replacers = {
            1: 'enabled',
            0: 'disabled'

        }

        if not mode in ['enable', 'disable']:
            await ctx.send(Emoji.info+" "+' Image confessions are currently '+replacers[config['allow_images']]+'. Use `image-confessions disable` or `nsfw-confessions enable` to change that.')
            return

        if mode == 'enable':
            await ctx.send(Emoji.warning+" Attention fella! If you enable image confessions, Members will be able to include images in the confessions. Though I try my best to filter all the NSFW images, Sometimes NSFW images can bypass that filter so it is recommended to not enable this option.\n\nRespond with `proceed` to proceed and enable or `cancel` to cancel this.")
            response = await self.bot.wait_for('message', check=lambda message: all([message.channel == ctx.channel and message.author == ctx.author and message.content.lower() in ['proceed', 'cancel']]))
            if response.content.lower() == 'proceed':
                pass
            else:
                await ctx.send(Emoji.success+" Operation cancelled successfully. Phew.")
                return

        message = await ctx.send(Emoji.lookup+" Gimme a minute...")

        collection = self.bot.mongo['guilds_config']['confessions']
        
        post = {
            '_id': ctx.guild.id
        }
        update = {
            '$set': {
                'allow_images': 1 if mode == 'enable' else 0
            }
        }
        await collection.update_one(post, update)

        await message.edit(content=Emoji.success+' Image confessions have been {}'.format('enabled' if mode == 'enable' else 'disabled'))

    @commands.command(name='confessions-embed-color',
        help=utils.createhelp('Changes the confessions embed color.', '`MANAGE_MESSAGES`'),
        description="`color` (Required): New color's hex. Set this to `random` to get random color everytime.",
        brief="/confessions/color",
        usage="confessions-embed-color <color>"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def embedcolor(self, ctx, color = None):
        if not color:
            await ctx.send(Emoji.info+" Provide a color's hex code. Use `confessions-embed-color random` to get random color on every confession.")
            return

        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='confessions')

        if config == None:
            await ctx.send(Emoji.error+" Confessions are not setup in this server, Set them up first! Use `setup-confessions` command.")
            return

        if color == 'random':
            int_color = 0
        else:
            if color.startswith('0x'):
                pass
            else:
                color = color.replace('#', '0x')
            try:
                int_color = int(color, 16)
            except ValueError:
                await ctx.send(Emoji.error+" This is not a valid color???")
                return

        message = await ctx.send(Emoji.lookup+" Gimme a minute...")

        collection = self.bot.mongo['guilds_config']['confessions']
        
        post = {
            '_id': ctx.guild.id
        }
        update = {
            '$set': {
                'embed_color': int_color
            }
        }
        await collection.update_one(post, update)

        await message.edit(content=Emoji.success+' Embed color has been updated to {}.'.format(color.replace('0x', '#')))

    @commands.command(name='mute-confession',
        help=utils.createhelp('Mutes a confession\'s author without revealing the author.', '`MANAGE_MESSAGES`'),
        description="`confession` (Required): The confessions's ID.",
        brief="/confessions/muting",
        usage="mute-confession <confession>"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def muteconfession(self, ctx, confession_id = None):
        if not confession_id:
            await ctx.send(Emoji.info+" Provide the confession ID and I'll deal with it. Confession ID can be found in the confession's title.")
            return

        message = await ctx.send(Emoji.lookup+" Gimme a minute while I mute the author...")

        user = await utils.evalsql(
            database='sqlite/store.db',
            sql='SELECT author_id from confessions where guild_id = ? and confession_id = ?',
            vals=(ctx.guild.id, confession_id),
            fetch='one'
            )
        if user == None:
            await message.edit(content="I cannot find that confession. Potential cause is that confession is more then 2 weeks old.")
            return

        user = user['author_id']

        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='confessions')

        if config == None:
            await message.edit(content=Emoji.error+" How the hell are you trying to mute a confession without even setting up the confessions in the server!??!")
            return

        collection = self.bot.mongo['guilds_config']['confessions']
        
        blacklist = config['blacklist']
        if str(user) in blacklist.keys():
            await message.edit(content="That user is already muted. :ok_hand:")
            return

        blacklist[str(user)] = str(confession_id)

        post = {
            '_id': ctx.guild.id
        }
        update = {
            '$set': {
                'blacklist': blacklist
            }
        }
        await collection.update_one(post, update)

        await message.edit(content=Emoji.success+' Confession author has been successfully muted.\n\nDue to confessions being highly anonymous, In order to unmute, Use `unmute-confession` with the same confession ID. There\'s no way of unmuting a confession without the confession ID.')


    @commands.command(name='unmute-confession',
        help=utils.createhelp('Unmutes a confession\'s author without revealing the author.', '`MANAGE_MESSAGES`'),
        description="`confession` (Required): The confessions's ID.",
        brief="/confessions/muting",
        usage="unmute-confession <confession>"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unmuteconfession(self, ctx, confession_id = None):
        if not confession_id:
            await ctx.send(Emoji.info+" Provide the confession ID. Confession ID can be found in the confession's title.")
            return

        message = await ctx.send(Emoji.lookup+" Gimme a minute while I mute the author...")

        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='confessions')

        if config == None:
            await message.edit(content=Emoji.error+" How the hell are you trying to unmute a confession without even setting up the confessions in the server!??!")
            return

        collection = self.bot.mongo['guilds_config']['confessions']
        
        blacklist = config['blacklist']
        if not str(confession_id) in blacklist.values():
            await message.edit(content="Nice try to find out the author. That user isn't even muted lol. You tried :star:")
            return

        for entry in blacklist.keys():
            if blacklist[entry] == confession_id:
                key = entry
                break

        blacklist.pop(key)

        post = {
            '_id': ctx.guild.id
        }
        update = {
            '$set': {
                'blacklist': blacklist
            }
        }
        await collection.update_one(post, update)

        await message.edit(content=Emoji.success+' Confession author has been successfully unmuted.')


    
    


def setup(bot):
    bot.add_cog(Confessions(bot))
