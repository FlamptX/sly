from discord.ext import commands
from discord import (
    Webhook,
    Embed,
    RequestsWebhookAdapter,
    DMChannel
    )

from core import utils
from core.object import Object
from core.enums import *
from core.mongo import MongoDB

import os
import json

__author__ = 'nerdguyahmad'
__version__ = '1.0.0'
__license__ = 'MIT'
__url__ = 'https://github.com/discordbotdevs/celly'

class Sly(commands.Bot):
    def __init__(self, intents):
        self.config = Object.from_json('config.json')

        super().__init__(
            command_prefix=commands.when_mentioned_or(self.get_prefix),
            intents=intents,
            owner_ids=self.config.owners
            )


        self.mongo = MongoDB(self.config.mongo.production.uri)

        # Prefix cache below exists because the self.get_prefix method is called on literally 
        # every message. And to avoid calling the database on every command the prefix cache
        # exists. If we don't build prefix cache the bot will look into database on every command
        # which will not only make the command processing slow but it is also not the best
        # practice to do.

        self.prefixes_cache = {}

    async def get_prefix(self, message):
        if isinstance(message.channel, DMChannel):
            return 'sly '

        if str(message.guild.id) in self.prefixes_cache:
            return self.prefixes_cache[str(message.guild.id)]

        prefix = await self.mongo.fetch_one_with_id(message.guild.id, database='guilds_config', collection='behaviour')
        if prefix == None:
            prefix = 'sly '
        else:
            prefix = prefix['prefix']

        self.prefixes_cache[str(message.guild.id)] = prefix
        return prefix

def filter_exts(config, ignore_exts=[]):
    return [ext for ext in config.exts if not ext in ignore_exts]

def run(token, intents, ignore_exts, debug):
    sly = Sly(intents=intents)
    failed_cogs = []
    for ext in filter_exts(sly.config, ignore_exts):
        try:
            sly.load_extension(ext)
        except Exception as err:
            if sly.config.quit_on_load_error:
                raise err
                quit()
            else:
                utils.log('[ERROR] (Cog: {}): {}'.format(ext, str(err)), theme='error')
                failed_cogs.append(ext)
    
    if not debug:
        webhook = Webhook.from_url(sly.config.webhooks.error_logging, adapter=RequestsWebhookAdapter())
        embed = Embed()
        if len(failed_cogs) == 0:
            embed.color = COLOR['success']
            embed.title = EMOJI['success'] + ' Successful start'
            embed.description = 'The bot has started with no load errors.'
            embed.add_field(name="Loaded Cogs", value='\n'.join(filter_exts(ignore_exts)))
            if len(ignore_exts):
                embed.add_field(name="Ignored Cogs", value='\n'.join(ignore_exts))
        else:
            embed.color = COLOR['warning']
            embed.title = EMOJI['warning'] + ' Unstable Start'
            embed.description = 'Some cogs have failed to load.'
            embed.add_field(name="Loaded Cogs", value='\n'.join(filter_exts(ignore_exts)))
            embed.add_field(name="Failed Cogs", value='\n'.join(failed_cogs))
            if len(ignore_exts):
                embed.add_field(name="Ignored Cogs", value='\n'.join(ignore_exts))

        webhook.send(embed=embed)

    sly.run(token)