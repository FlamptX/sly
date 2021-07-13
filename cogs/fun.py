import discord
from discord.ext import commands, tasks
from discord_components import DiscordComponents, Select, SelectOption

import random
import aiohttp

from core import utils

class Fun(commands.Cog, name="fun", description="These are some fun commands to cure your boredom lol."):
    def __init__(self, bot):
        self.bot = bot
        self.memes = []
        self.dc    = DiscordComponents(self.bot)
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

    @commands.command(
        help="Ask a question and I will reply.",
        description="`question` (Required): The question you want to ask.",
        brief='/fun/others',
        usage='8ball',
        aliases=['8ball']

        )
    async def eightball(self, ctx, *, question:str=None):
        if not question:
            await ctx.send("Hey you gotta ask a question that I will answer.")
            return

        responses = [
            'I\'m sure about that!',
            'Without a doubt.',
            'This is certain.',
            'Indeed',
            'Yah man! Yah!',
            'I reply positively',
            'Indeed yes!',
            'Oh hell ya!',
            'There ain\'t a doubt in that',
            'Ask again later bud!',
            'I\'m not in the mood of replying, ask again later',
            'I am not sure about that',
            'Too bad, Ask again later.',
            'Nah! Not a chance.',
            'Too doubtful',
            'Don\'t count on it.',
            'I would say No.',
            'Nope!',
            'Oh hell nah!',
            'My sources say no.',
            'Negative!'
        ]
        embed = discord.Embed(title=":8ball: \"{}\"".format(question), description=random.choice(responses))
        embed.set_author(name="{} asked".format(str(ctx.author)), icon_url=ctx.author.avatar_url)
        embed.color = discord.Color.random()
        await ctx.send(embed=embed)

    @commands.command(
        help="Ships two users. :heart:",
        description="`user1` (Optional): The first user.\n`user2` (Optional): The second user\n\nIf the `user1` is not provided, you will be shipped by second user, If `user2` not provided you will be shipped with random user.",
        brief='/fun/others',
        usage='ship',

        )
    async def ship(self, ctx, *, user1:discord.Member=None, user2:discord.Member=None):
        if not user1 and not user2: # `ship`
            user1 = ctx.author
            user2 = random.choice(ctx.guild.members)

        if not user2: # `ship @user`
            user2 = user1
            user1 = ctx.author
        
        count = random.randint(0, 100)
        print(count)
        if count == 0:
            message = "Oh No! :broken_heart:"

        elif count <= 20:
            message = "Too bad! :sad_face:"

        elif count <= 40:
            message = "Too doubtful there. :neutral_face:"

        elif count <= 60:
            message = "Somewhat good. :thinking_face:"

        elif count == 69:
            message = "Noice. :wink:"

        elif count <= 70:
            message = "Something good. :smiling_face_with_3_hearts:"

        elif count <= 90:
            message = "Pretty good! :heart:"

        elif count == 100:
            message = "PERFECT! :revolving_hearts:"

        if count >= 60:
            emoji = ':heart:'
            ship_name = user1.name[0:len(user1.name)-round(len(user1.name)/2)]+user2.name[0:len(user2.name)-round(len(user2.name)/2)]
        else:
            emoji = ':broken_heart:'
            ship_name = None
        embed = discord.Embed(title='{} | {} {} {}'.format(count, user1.name, emoji, user2.name), description=message)
        if ship_name != None:
            embed.title += ' = {}'.format(ship_name.title())
            embed.color = discord.Color.red()
        else:
            embed.color = discord.Color.darker_grey()
        
        await ctx.send(embed=embed)

    @commands.command()
    async def rockpaperscissor(self, ctx):
        message = await ctx.send(
            "Hey choose from Rock paper or scissor?",
            components = [
                Select(placeholder="Select your choice!", options=[SelectOption(label="Rock", value=0), SelectOption(label="Paper", value=1), SelectOption(label="Scissor", value=2)])
            ]
        )

        interaction = await self.bot.wait_for("select_option", check = lambda i: i.user == ctx.author)

        user = str(interaction.component[0].value)
        my = random.randint(0, 2)

        if str(user) == str(my):
            string = "That's a tie!"
        elif user == '0' and my == 1:
            string = "You lost! heehee!"
        elif user == '0' and my == 2:
            string = "You won! damnnn"
        elif user == '1' and my == 0:
            string = "You won! :O"
        elif user == '1' and my == 2:
            string = "You lost! get rekt!"
        elif user == '2' and my == 0:
            string = "You lost! hehehehe"
        elif user == '2' and my == 1:
            string = "You won! poggers"

        rep = {0: 'rock', 1: 'paper', 2: 'scissor'}
        await message.delete()
        await interaction.respond(content = f"You chose {interaction.component[0].label}, I chose {rep[my]}. {string}")

    

def setup(bot):
    bot.add_cog(Fun(bot))