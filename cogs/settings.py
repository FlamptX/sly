import discord
from discord.ext import commands

from core.enums import Emoji, Color
from core import utils

class Settings(commands.Cog, name="config", description="Decide how Sly functions for this server or for you."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='easter-eggs',
        help=utils.createhelp('Enable or disable [easter eggs](https://slybot.gitbook.io/topics/easters) in this server.', '`MANAGE_MESSAGES`'),
        description="`mode` (Required): Can either be `enable` or `disable`",
        brief="/settings/easters",
        usage="easter-eggs <mode>"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def eastereggs(self, ctx, mode = None):
        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='behaviour')

        if config == None:
            config = {'_id': ctx.guild.id, 'prefix': 'sly ', 'easters': 0, 'track_deletes': 1, 'track_edits': 1}
            await self.bot.mongo['guilds_config']['behaviour'].insert_one({'_id': ctx.guild.id, 'prefix': 'sly ', 'easters': 0, 'track_deletes': 1, 'track_edits': 1})

        replacers = {
            1: 'enabled',
            0: 'disabled'

        }

        if not mode in ['enable', 'disable']:
            await ctx.send(Emoji.info+" "+' Easter eggs are currently '+replacers[config['easters']]+'. Use `easter-eggs disable` or `easter-eggs enable` to change that.')
            return
            
        message = await ctx.send(Emoji.lookup+" Gimme a minute...")

        collection = self.bot.mongo['guilds_config']['behaviour']
        
        post = {
            '_id': ctx.guild.id
        }
        update = {
            '$set': {
                'easters': 1 if mode == 'enable' else 0
            }
        }
        await collection.update_one(post, update)

        await message.edit(content=Emoji.success+' Easter eggs have been {}'.format('enabled. I will send funny messages or react with funny reactions on certain moments. :wink:' if mode == 'enable' else 'disabled'))
        

    @commands.command(name='set-prefix',
        help=utils.createhelp('Change server prefix of this server.', '`MANAGE_SERVER`'),
        description="`prefix` (Required): The new prefix.",
        brief="/settings/prefix",
        usage="set-prefix <mode>"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix = None):
        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='behaviour')

        if config == None:
            config = {'_id': ctx.guild.id, 'prefix': 'sly ', 'easters': 0, 'track_deletes': 1, 'track_edits': 1}
            await self.bot.mongo['guilds_config']['behaviour'].insert_one({'_id': ctx.guild.id, 'prefix': 'sly ', 'easters': 0, 'track_deletes': 1, 'track_edits': 1})

        if prefix == None:
            await ctx.send(Emoji.info+" "+' Prefix is currently '+config['prefix']+'. Use this command again with prefix to change it. For example, `set-prefix ?` will change prefix to `?`.')
            return
            
        message = await ctx.send(Emoji.lookup+" Gimme a minute...")

        collection = self.bot.mongo['guilds_config']['behaviour']
        
        post = {
            '_id': ctx.guild.id
        }
        update = {
            '$set': {
                'prefix': prefix
            }
        }
        await collection.update_one(post, update)

        await message.edit(content=Emoji.success+' Prefix has been set to: {prefix}, In order to use any command, you need to use new prefix, e.g `{prefix}help`. You can use `{prefix}reset-prefix` to reset it to `sly`.'.format(prefix=prefix))
        self.bot.prefixes_cache[str(ctx.guild.id)] = prefix

    @commands.command(name='reset-prefix',
        help=utils.createhelp('Resets the server prefix to default.', '`MANAGE_SERVER`'),
        description="This command takes no arguments.",
        brief="/settings/prefix",
        usage="reset-prefix <mode>"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def resetprefix(self, ctx):
        message = await ctx.send(Emoji.lookup+" Gimme a minute...")
        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='behaviour')

        if config == None:
            config = {'_id': ctx.guild.id, 'prefix': 'sly ', 'easters': 0, 'track_deletes': 1, 'track_edits': 1}
            await self.bot.mongo['guilds_config']['behaviour'].insert_one({'_id': ctx.guild.id, 'prefix': 'sly ', 'easters': 0, 'track_deletes': 1, 'track_edits': 1})
            await ctx.send(Emoji.success+" The prefix has been reset!")
            return 
            

        collection = self.bot.mongo['guilds_config']['behaviour']
        
        post = {
            '_id': ctx.guild.id
        }
        update = {
            '$set': {
                'prefix': 'sly '
            }
        }
        await collection.update_one(post, update)

        await message.edit(content=Emoji.success+' Prefix has been reset to: `sly`, In order to use any command, you need to use new prefix, e.g `sly help`.')
        self.bot.prefixes_cache[str(ctx.guild.id)] = 'sly '

    @commands.command(name='delete-tracking',
        help=utils.createhelp('Enable or disable [recent delete messages tracking](https://slybot.gitbook.io/topics/tracking) in this server. `showdelete` command is powered by thing setting.', '`MANAGE_MESSAGES`'),
        description="`mode` (Required): Can either be `enable` or `disable`",
        brief="/settings/tracking",
        usage="delete-tracking <mode>"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def deletetracking(self, ctx, mode = None):
        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='behaviour')

        if config == None:
            config = {'_id': ctx.guild.id, 'prefix': 'sly ', 'easters': 0, 'track_deletes': 1, 'track_edits': 1}
            await self.bot.mongo['guilds_config']['behaviour'].insert_one({'_id': ctx.guild.id, 'prefix': 'sly ', 'easters': 0, 'track_deletes': 1, 'track_edits': 1})

        replacers = {
            1: 'enabled',
            0: 'disabled'

        }

        if not mode in ['enable', 'disable']:
            await ctx.send(Emoji.info+" "+' Delete messages tracking is currently '+replacers[config['track_deletes']]+'. Use `delete-tracking disable` or `delete-tracking enable` to change that.')
            return
            
        message = await ctx.send(Emoji.lookup+" Gimme a minute...")

        collection = self.bot.mongo['guilds_config']['behaviour']
        
        post = {
            '_id': ctx.guild.id
        }
        update = {
            '$set': {
                'track_deletes': 1 if mode == 'enable' else 0
            }
        }
        await collection.update_one(post, update)

        await message.edit(content=Emoji.success+' Delete messages tracking has been {}'.format('enabled.' if mode == 'enable' else 'disabled. `showdelete` will not work now.'))

    @commands.command(name='edit-tracking',
        help=utils.createhelp('Enable or disable [recent edited messages tracking](https://slybot.gitbook.io/topics/tracking) in this server. `showedit` command is powered by thing setting.', '`MANAGE_MESSAGES`'),
        description="`mode` (Required): Can either be `enable` or `disable`",
        brief="/settings/tracking",
        usage="edit-tracking <mode>"
        )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def edittracking(self, ctx, mode = None):
        config = await self.bot.mongo.fetch_one_with_id(ctx.guild.id, database='guilds_config', collection='behaviour')

        if config == None:
            config = {'_id': ctx.guild.id, 'prefix': 'sly ', 'easters': 0, 'track_deletes': 1, 'track_edits': 1}
            await self.bot.mongo['guilds_config']['behaviour'].insert_one({'_id': ctx.guild.id, 'prefix': 'sly ', 'easters': 0, 'track_deletes': 1, 'track_edits': 1})

        replacers = {
            1: 'enabled',
            0: 'disabled'

        }

        if not mode in ['enable', 'disable']:
            await ctx.send(Emoji.info+" "+' Edited messages tracking is currently '+replacers[config['track_edits']]+'. Use `edit-tracking disable` or `edit-tracking enable` to change that.')
            return
            
        message = await ctx.send(Emoji.lookup+" Gimme a minute...")

        collection = self.bot.mongo['guilds_config']['behaviour']
        
        post = {
            '_id': ctx.guild.id
        }
        update = {
            '$set': {
                'track_edits': 1 if mode == 'enable' else 0
            }
        }
        await collection.update_one(post, update)

        await message.edit(content=Emoji.success+' Edited messages tracking has been {}'.format('enabled.' if mode == 'enable' else 'disabled. `showedit` will not work now.'))

    




def setup(bot):
    bot.add_cog(Settings(bot))