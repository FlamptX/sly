import discord
from discord.ext import commands, tasks

import random
import aiohttp

from core import utils

class Fun(commands.Cog, name="fun", description="These are some fun commands to cure your boredom lol."):
    def __init__(self, bot):
        self.bot = bot
        self.memes = []
        self.update_memes.start()

    def cog_unload(self):
        update_memes.stop()

    @tasks.loop(seconds=1800)
    async def update_memes(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get('https://memifyapi.herokuapp.com/api/meme/dank/100', headers={'x-api-key': self.bot.config.memify_api_key})
            response = await response.json()
            self.memes = response['response']

    @commands.command(
        help="Sends a random dank meme.",
        description="This command takes no arguments.",
        brief='/fun/meme',
        usage='meme'
        )
    async def meme(self, ctx):
        m = random.choice(self.memes)
        embed = discord.Embed(title=m['title'], color=discord.Color.random())
        embed.set_author(name='u/'+m['author'])
        embed.set_footer(text="Likes: {}".format(m['thumbs_up']))
        embed.set_image(url=m['url'])
        await ctx.send(embed=embed)

    @commands.command(
        help="Shows how much a user is gay.",
        description="`user` (Optional): The user to calculate gay rate of.",
        brief='/fun/rates',
        usage='gayrate'
        )
    async def gayrate(self, ctx, user:discord.Member = None):
        if user is None:
            user = ctx.author

        msg = await ctx.send(":thinking_face:")
        embed = discord.Embed(title=":rainbow: Gay Rate")
        embed.set_author(name=str(user), icon_url=ctx.author.avatar_url)

        rate = random.randint(0, 100)
        if random.randint(0, 100) == random.randint(0, 100):
            embed.description = "{}\n\n**INFINITY!** The gay rate of {} is so high that I can't even calculate it!".format(str(user))
            embed.set_image(url=f'https://api.toxy.ga/api/gay?avatar={user.avatar_url}')
        else: 
            embed.description = r"**{}** is **{}% gay!**".format(str(user), str(rate))

        embed.color = int(random.choice([
                    '0xff0018', 
                    '0xffa52c',
                    '0xffff41',
                    '0x008018',
                    '0x000DF9',
                    '0x86007D']), 16) # These are Pride flag colors

        await msg.edit(embed=embed)

    @commands.command(
        help="Calculates a user's simp rate.",
        description="`user` (Optional): The user to calculate simp rate of.",
        brief='/fun/rates',
        usage='simprate'
        )
    async def simprate(self, ctx, user:discord.Member = None):
        if user is None:
            user = ctx.author

        msg = await ctx.send(":thinking_face:")
        embed = discord.Embed(title=":heart_eyes: Simp Rate")
        embed.set_author(name=str(user), icon_url=ctx.author.avatar_url)

        rate = random.randint(0, 100)
        if random.randint(0, 100) == random.randint(0, 100):
            embed.description = "{}\n\n**INFINITY!** The simp rate of {} is so high that I can't even calculate it!".format(str(user))
            embed.set_image(url=f"https://api.devs-hub.xyz/simp?image={user.avatar_url}")
        else: 
            embed.description = r"**{}** is **{}% simp!**".format(str(user), str(rate))

        embed.color = discord.Color.random()
        await msg.edit(embed=embed)

    @commands.command(
        help="Calculates a user's IQ.",
        description="`user` (Optional): The user to calculate IQ of.",
        brief='/fun/rates',
        usage='iq'
        )
    async def iq(self, ctx, user:discord.Member = None):
        if user is None:
            user = ctx.author

        msg = await ctx.send(":thinking_face:")
        embed = discord.Embed(title=":brain: IQ Test")
        embed.set_author(name=str(user), icon_url=ctx.author.avatar_url)

        iqrange = random.randint(0, 10)
        rate = random.randint(0, 50)*iqrange

        if random.randint(0, 100) == random.randint(0, 100):
            embed.description = "{}\n\n**INFINITY!** {} is so smart that I can't even calculate it!".format(str(user))
        else: 
            embed.description = r"**{}**'s IQ is **{}**!".format(str(user), str(rate))

        embed.color = discord.Color.random()
        await msg.edit(embed=embed)

    

    

def setup(bot):
    bot.add_cog(Fun(bot))