import discord
from discord.ext import commands
from core.enums import Color, Emoji

class Image(commands.Cog, description="Generate memes and apply filters using single commands using the epic image manipulation commands! :ok_hand:", name="image"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Generates an image with epic triggered filter!",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='triggered [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def triggered(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/triggered?avatar={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates an image with epic GTA 5 wasted filter!",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='wasted [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def wasted(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/wasted?avatar={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates a change my mind meme with provided text!",
        description="`text` (Optional): The text to use on image.",
        brief='image/filters',
        usage='changemymind <text>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def changemymind(self, ctx, *, text=None):
        if text == None:
            await ctx.send(Emoji.info+" You need to provide the text.")
            return

        text = text.replace(' ', '%20')
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/changemymind?text="+text)
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates a clyde message image with provided text!",
        description="`text` (Optional): The text to use on image.",
        brief='image/filters',
        usage='clyde <text>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def clyde(self, ctx, *, text=None):
        if text == None:
            await ctx.send(Emoji.info+" You need to provide the text.")
            return

        text = text.replace(' ', '%20')
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/clyde?text="+text)
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)
    
    @commands.command(
        help="Generates an image with greyscale filter!",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='greyscale [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def greyscale(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/greyscale?avatar={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates an image with blurry filter!",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='blur [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def blur(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/blur?avatar={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Sends someone to jail lol.",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='jail [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def jail(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/jail?avatar={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates an image with RIP filter.",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='rip [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def rip(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/rip?avatar={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates an image with facepalm filter.",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='facepalm [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def facepalm(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/facepalm?avatar={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates an image with gay filter.",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='gay [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def gay(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/gay?avatar={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates an image with trash filter.",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='trash [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def trash(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/trash?avatar={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates an image with sephia filter.",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='sephia [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def sephia(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/sephia?avatar={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)


    @commands.command(
        help="Hands over a gun to a person's avatar.",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='gun [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def gun(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author


        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/gun?image={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Puts on grabby filter on a person's avatar.",
        description="`user` (Optional): The person whose avatar should be used, defaults to command's user.",
        brief='image/filters',
        usage='grabby [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def grabby(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/grab?image={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates a two button meme.",
        description="`text1` (Required): The first text.\n`text2` (Required): The second text.",
        brief='image/filters',
        usage='twobuttons <text1> ;; <text2>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def twobuttons(self, ctx, *, text=None):
        if text == None:
            await ctx.send(Emoji.info+" You need to specify the text like: `TEXT 1 HERE ;; TEXT 2 HERE`.")
            return


        text = text.split(";;")
        t1 = text[0]
        t1 = t1.replace(' ', '%20')
        t2 = text[1]
        t2 = t2.replace(' ', '%20')
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/two-buttons?button1={t1}&button2={t2}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates a scroll of truth meme.",
        description="`text` (Required): The text to put on image.",
        brief='image/filters',
        usage='scrolloftruth <text>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def scrolloftruth(self, ctx, *, text=None):
        if text == None:
            await ctx.send(Emoji.info+" You need to specify the text to put in the image.")
            return

        text = text.replace(' ', '%20')
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/truth?text={text}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates a calling image.",
        description="`text` (Required): The text to put on image.",
        brief='image/filters',
        usage='calling <text>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def calling(self, ctx, *, text=None):
        if text == None:
            await ctx.send(Emoji.info+" You need to specify the text to put in the image.")
            return

        text = text.replace(' ', '%20')
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.cool-img-api.ml/calling?text={text}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates a drake meme.",
        description="`text1` (Required): The first text.\n`text2` (Required): The second text.",
        brief='image/filters',
        usage='drake <text1> ;; <text2>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def drake(self, ctx, *, text=None):
        if text == None:
            await ctx.send(Emoji.info+" You need to specify the text like: `TEXT 1 HERE ;; TEXT 2 HERE`.")
            return


        text = text.split(";;")
        t1 = text[0]
        t1 = t1.replace(' ', '%20')
        t2 = text[1]
        t2 = t2.replace(' ', '%20')
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/drake?top={t1}&bottom={t2}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)


    @commands.command(
        help="This one is for simps.",
        description="`user` (Optional): The simp whose avatar should be used, If not provided, you will be the target so be careful lol.",
        brief='image/filters',
        usage='simp [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def simp(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/simp?image={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)


    @commands.command(
        help="Generates a did you mean google image.",
        description="`text1` (Required): The first text.\n`text2` (Required): The second text.",
        brief='image/filters',
        usage='didyoumean <text1> ;; <text2>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def didyoumean(self, ctx, *, text=None):
        if text == None:
            await ctx.send(Emoji.info+" You need to specify the text like: `TEXT 1 HERE ;; TEXT 2 HERE`.")
            return


        text = text.split(";;")
        t1 = text[0]
        t1 = t1.replace(' ', '%20')
        t2 = text[1]
        t2 = t2.replace(' ', '%20')
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.cool-img-api.ml/didyoumean?top={t1}&bottom={t2}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates a tuxedo pooh image.",
        description="`text1` (Required): The first text.\n`text2` (Required): The second text.",
        brief='image/filters',
        usage='pooh <text1> ;; <text2>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def pooh(self, ctx, *, text=None):
        if text == None:
            await ctx.send(Emoji.info+" You need to specify the text like: `TEXT 1 HERE ;; TEXT 2 HERE`.")
            return


        text = text.split(";;")
        t1 = text[0]
        t1 = t1.replace(' ', '%20')
        t2 = text[1]
        t2 = t2.replace(' ', '%20')
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/tuxedo-pooh?normal={t1}&tuxedo={t2}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    

    @commands.command(
        help="Puts on hearts filter on person's avatar ;).",
        description="`user` (Optional): The person's whose avatar should be used.",
        brief='image/filters',
        usage='hearts [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def hearts(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author


        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/hearts?image={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates a sponge bob timecard.",
        description="`text` (Optional): The text of timecard.",
        brief='image/filters',
        usage='timecard <text>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def timecard(self, ctx, *, text=None):
        if text == None:
            await ctx.send(Emoji.info+" You need to provide the text.")
            return

        text.replace(' ', '%20')
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.toxy.ga/api/spongebob-timecard?text="+text)
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates a panik meme.",
        description="`text1` (Required): The first text.\n`text2` (Required): The second text.\n`text3` (Required): The third text.",
        brief='image/filters',
        usage='panik <text1> ;; <text2> ;; <text3>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def panik(self, ctx, *, text=None):
        if text == None:
            await ctx.send(Emoji.info+" You need to specify the text like: `TEXT 1 HERE ;; TEXT 2 HERE ;; TEXT 3 HERE`.")
            return


        text = text.split(";;")
        t1 = text[0]
        t1 = t1.replace(' ', '%20')
        t2 = text[1]
        t2 = t2.replace(' ', '%20')
        t3 = text[2]
        t3 = t3.replace(' ', '%20')
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/panik?panik={t1}&kalm={t2}&panik2={t3}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Puts on \"Everyone liked that\" filter on an image.",
        description="`image` (Required): The image to apply filter on.",
        brief='image/filters',
        usage='like <image>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def like(self, ctx):
        if len(ctx.message.attachments) == 0:
            await ctx.send(Emoji.info+" You need to attach an image in order for this command to function.")
            return


        image= ctx.message.attachments[0]

        if not image.content_type.startswith('image/'):
            await ctx.send(Emoji.info+" The message attachement has to be an image!")
            return
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/like?image={image.url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Puts on \"Everyone disliked that\" filter on an image.",
        description="`image` (Required): The image to apply filter on.",
        brief='image/filters',
        usage='dislike <image>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def dislike(self, ctx):
        if len(ctx.message.attachments) == 0:
            await ctx.send(Emoji.info+" You need to attach an image in order for this command to function.")
            return


        image= ctx.message.attachments[0]

        if not image.content_type.startswith('image/'):
            await ctx.send(Emoji.info+" The message attachement has to be an image!")
            return
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/dislike?image={image.url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Puts on \"Jokes over the head\" filter on a user's avatar.",
        description="`user` (Optional): The user's whose avatar should be used.",
        brief='image/filters',
        usage='jokeoverhead [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def jokeoverhead(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/joke-over-the-head?image={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Puts on \"beautiful painting\" filter on an image.",
        description="`image` (Required): The image to apply filter on.",
        brief='image/filters',
        usage='beautiful <image>'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def beautiful(self, ctx):
        if len(ctx.message.attachments) == 0:
            await ctx.send(Emoji.info+" You need to attach an image in order for this command to function.")
            return


        image= ctx.message.attachments[0]

        if not image.content_type.startswith('image/'):
            await ctx.send(Emoji.info+" The message attachement has to be an image!")
            return
        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/beautiful?image={image.url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Deletes the trash.",
        description="`user` (Optional): The user's whose avatar should be memified.",
        brief='image/filters',
        usage='delete [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def delete(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/delete?image={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Magikify the avatar of a user.",
        description="`user` (Optional): The user's whose avatar should be Magikifyed.\nlevel (optional): The level of magikifiaction.",
        brief='image/filters',
        usage='magik [user] [level]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def magik(self, ctx, user: discord.Member = None, level='50'):
        if user == None:
            user = ctx.author

        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/magik?image={user.avatar_url}&level={level}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Generates a wanted poster from user's avatar.",
        description="`user` (Optional): The user's whose avatar should be memified.",
        brief='image/filters',
        usage='wanted [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def wanted(self, ctx, user: discord.Member = None, level='50'):
        if user == None:
            user = ctx.author

        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.cool-img-api.ml/wanted?image={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

    @commands.command(
        help="Applies the communist filter on user's avatar.",
        description="`user` (Optional): The user's whose avatar should be memified.",
        brief='image/filters',
        usage='communist [user]'

        )
    @commands.cooldown(1, 5, commands.BucketType.user)

    async def communist(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        
        
        embed = discord.Embed(color=Color.neutral)
        embed.set_image(url=f"https://api.devs-hub.xyz/communist?image={user.avatar_url}")
        embed.set_footer(text="If the image doesn't load within few seconds, Please contact us through support server.")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Image(bot))