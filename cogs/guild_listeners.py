import discord
from discord.ext import commands

class GuildListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.bot.mongo['guilds_config']['behaviour'].insert_one({
            '_id': guild.id,
            'prefix': 'sly ',
            'track_deletes': 1,
            'track_edits': 1,
            'easters': 0
            })
        embed = discord.Embed(title=":wave: Hi peeps!", description="I'm Sly and I'm here to make day of each and everyone here, I hope ya'll like me and I'll try my best to entertain ya'll.")
        embed.add_field(name="Help Command", value="My prefix is `sly`, you can use `sly help` to see all commands and categories! :ok_hand:", inline=False)
        embed.add_field(name="Some links you might wanna check out", value="- [Docs](https://slybot.gitbook.io)\n- [GitHub](https://github.com/nerdguyahmad/sly)\n- [Issue Tracker](https://github.com/nerdguyahmad/sly/issues)\n- [Website (Coming soon...)](https://sly-bot.web.app)\n- [Status](https://bit.ly/weebotstatus)\n- [Support & Community server](https://discord.gg/38G3TDabg5)\n- [Invite](https://dsc.gg/slybot)", inline=False)
        embed.color = discord.Color.random()

        for i in guild.channels:
            if isinstance(i, discord.TextChannel):
                if i.permissions_for(guild.me).send_messages:
                    await i.send(embed=embed)
                    break

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.mongo['guilds_config']['behaviour'].delete_one({
            '_id': guild.id
            })
        await self.bot.mongo['guilds_config']['confessions'].delete_one({
            '_id': guild.id
            })


    
def setup(bot):
    bot.add_cog(GuildListeners(bot))