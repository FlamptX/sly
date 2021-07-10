import discord
from discord.ext import commands, menus

from core import utils
from core.enums import Emoji, Color

class PaginateConfessionChannelMenu(menus.ListPageSource):
    def __init__(self, data, per_page=8):
        self.data = data
        super().__init__(data, per_page=per_page)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=f"Select the server", color=Color.neutral)
        
        for entry in entries:
            embed.add_field(name=entry.name, value='Respond with `{}` to post confession in {}'.format(data.index(entry)+1, entry.name), inline=False)
        
        return embed

class Confessions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_confessions_config(self, guild):
        check = await self.bot.mongo.fetch_one_by_id(guild.id, database='guilds_config', collections='confessions')
        if check == None:
            return False
        else:
            return check

    async def get_eligible_guilds(self, member):
        mutual   = [guild for guild in self.bot.guilds if member in guild.members]
        eligible = [guild for guild in mutual if self.has_confessions_enabled(guild)]
        return eligible


    @commands.command(
        help='Post a completely anonymous confession in the confession channel. This command only work in DMs!',
        brief='/confessions/posting',
        description='`confession` (Required): The confession to post. In favor of long message writers, This can be upto 4000 characters long.',
        usage='confess <message>'
        
        )
    async def confess(self, ctx, message=None):
        if not message:
            await ctx.send("You gotta specify a confession that you want to post.")
            return

        message = await ctx.send(Emoji.lookup+' Give me a moment while I look up for the servers where you can post confessions...\n\nIf it\'s taking long, You can do other things and I will notify you when it\'s done.')
        guilds = await self.get_eligible_guilds(ctx.author)
        if len(guilds) == 0:
            await message.edit(content="I cannot find any server in which you can post a confession. Maybe none of your servers has enabled confessions? If you are a server moderator, You can use `config confessions setup` command and setup suggestions.")
            return

        paginator = menus.MenuPages(source=PaginateConfessionChannelMenu(guilds), clear_reactions_after=True)
        await paginator.start()
def setup(bot):
    bot.add_cog(Confessions(bot))