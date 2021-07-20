import discord
from discord.ext import commands

from core.enums import Color

import aiohttp


class Bot(commands.Cog, name="bot", description="Some bot related commands that you might want to use maybe."):
    def __init__(self, bot):
        self.bot = bot
        # GitHub read only API is way too selfish so here is the issue cache oof.

        self.issues = {}

    async def get_issue(self, id):
        async with aiohttp.ClientSession() as session:
            issue = await session.get('https://api.github.com/repos/nerdguyahmad/sly/issues/%s' % id)
            if issue.status == 200:
                return await issue.json()

            elif issue.status == 404:
                pr = await session.get('https://api.github.com/repos/nerdguyahmad/pulls/issues/%s' % id)
                if pr.status == 200:
                    return await pr.json()
                elif pr.status == 404:
                    return 404

            return None
                


    @commands.command(
        help="Shows info about Sly bot's GitHub issue or pull request.",
        description="`id` (Required): The ID of the issue or pull request.",
        brief='/misc/bot',
        usage='github <id>'
        )
    async def github(self, ctx, id = None):
        if not id:
            await ctx.send("Hey, provide the ID of the issue or pull request you want info about.")
            return

        if not id.isdigit():
            await ctx.send("That isn't a valid ID. Bruh.")
            return

        if str(id) in self.issues:
            await ctx.send(embed=self.issues[str(id)])
            return

        issue = await self.get_issue(id)
        if issue == 404:
            await ctx.send("No issue or PR with ID #{} found.".format(id))
            return
        if issue == None:
            await ctx.send("An error occured.".format(id))
            return

        states = {'open': ':green_circle:', 'closed': ':red_circle:'}
        embed = discord.Embed(
            title=states[issue['state']]+' | '+issue['title'], 
            description=issue['body'] if len(issue['body']) > 2000 else issue['body'][0:2000]+'...',
            url=issue['html_url'])
        embed.set_author(name=issue['user']['login'], icon_url=issue['user']['avatar_url'], url=issue['user']['html_url'])
        if len(issue['labels']) >= 1:
            embed.add_field(name="Labels", value=" | ".join(['**'+label['name']+'**' for label in issue['labels']]))

        await ctx.send(embed=embed)
        self.issues[str(id)] = embed

    @commands.command(
        help="Shows bot's important links.",
        description="This command takes no arguments.",
        brief='/misc/bot',
        usage='links'
        )
    async def links(self, ctx):
        embed = discord.Embed(title="Important Links", color=Color.neutral)
        embed.description = "Here are some cool links that you might want to checkout:\n\n- [Docs](https://slybot.gitbook.io)\n- [GitHub](https://github.com/nerdguyahmad/sly)\n- [Issue Tracker](https://github.com/nerdguyahmad/sly)\n- [Website (Coming soon...)](https://sly-bot.web.app)\n- [Status](https://bit.ly/weebotstatus)\n- [Support & Community server](https://discord.gg/38G3TDabg5)\n- [Invite](https://dsc.gg/slybot)"
        await ctx.send(embed=embed)

    @commands.command(
        help="Shows bot's info.",
        description="This command takes no arguments.",
        brief='/misc/bot',
        usage='info'
        )
    async def info(self, ctx):
        embed = discord.Embed(title="About Sly", description="Sly is an epic fun and entertainment discord bot made to spice up the discord servers.", color=Color.neutral)
        embed.add_field(name="Creator", value="Sly was created by nerdguyahmad#3195 along with the cool community on [GitHub](https://github.com/nerdguyahmad/sly).")
        embed.add_field(name="Version", value="v1.0.0 [BETA]", inline=False)
        embed.add_field(name="Collaborate", value="Help us make Sly better on [GitHub](https://github.com/nerdguyahmad/sly)", inline=False)
        embed.add_field(name="Links", value="- [Docs](https://slybot.gitbook.io)\n- [GitHub](https://github.com/nerdguyahmad/sly)\n- [Issue Tracker](https://github.com/nerdguyahmad/sly)\n- [Website (Coming soon...)](https://sly-bot.web.app)\n- [Status](https://bit.ly/weebotstatus)\n- [Support & Community server](https://discord.gg/38G3TDabg5)\n- [Invite](https://dsc.gg/slybot)")
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Bot(bot))