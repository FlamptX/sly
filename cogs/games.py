import discord
from discord.ext import commands

class Games(commands.Cog, name="games", description="These games will help you not get bored when your homies are offline. Give em' a try."):
    def __init__(self, bot):
        self.bot = bot

    

def setup(bot):
    bot.add_cog(Games(bot))