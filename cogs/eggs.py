import discord
import json
import random
from discord.ext import commands

class Eggs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('stuff/eggs.json', 'r') as f:
            self.eggs = json.loads(f.read(), encoding='utf-8')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.lower() in self.eggs:
            if self.eggs[message.content.lower()]['type'] == 'random':
                choice = random.randint(0, 1)
                if choice == 1: choice = 'respond'
                else: choice = 'react'
            else:
                choice = self.eggs[message.content.lower()]['type']

            if random.randint(1, 20) == random.randint(1, 20):
                conf = await self.bot.mongo.fetch_one_with_id(message.guild.id, database='guilds_config', collection='behaviour')
                
                if conf == None:
                    return
                if conf['eggs'] == 1:
                    pass
                else:
                    return

                if choice == 'respond':
                    await message.reply(random.choice(self.eggs[message.content.lower()]['on_respond']['respond_with']))
                elif choice == 'react':
                    await message.add_reaction(random.choice(self.eggs[message.content.lower()]['on_react']['react_with']))

def setup(bot):
    bot.add_cog(Eggs(bot))