import discord
from discord.ext import commands

from core.enums import Emoji, Color
from core import utils

class CustomHelpCommand(commands.MinimalHelpCommand):
    '''
    Custom Help command.

    This is subclass of commands.MinimalHelpCommand.
    '''
    def __init__(self, config):
        self.config = config
        super().__init__()

    def parse_cogname(self, cog):
        names = {
            'confessions': ':performing_arts: Confessions',
            'image': ':camera: Image Manipulation',
            'utility': ':wrench: Utility',
            'config': ':gear: Config',
            'bot': ':robot: Bot Stuff',
            'fun': ':joy: Fun & Memes'
        }
        return names[cog.qualified_name]

    async def send_cog_help(self, cog):
        '''No cog help. Sheeeesh!'''
        channel = self.get_destination()
        cmds = cog.get_commands()

        embed = discord.Embed(title=self.parse_cogname(cog), description=cog.description)
        embed.color = Color.info
        embed.add_field(name="Commands", value=', '.join(['`'+command.name+'`' for command in cmds]))
        embed.add_field(name="More info", value="For more information on a command, Use `help <command>` command.", inline=False)
        await channel.send(embed=embed)

    async def send_group_help(self, group):
        '''
        Sends the help message for a commands.Group object. (Or a command group).

        This embed basically leads the user to use the main group command for more information.
        '''
        channel = self.get_destination()
        embed = discord.Embed(
            title = group.name,
            description = group.help,
            url=self.config.docs+group.brief # Gitbook Doc Link to command
            )
        embed.color = Color.info
        embed.add_field(name="Commands", value='\n'.join(
            ['`'+group.name+' '+command.name+'`' for command in group.commands]
            ))
        embed.add_field(name="More Help", 
            value="For more information about this, Use `-{name}` or for information about a command use: `-help {name} [command]`".format(name=group.name),
            inline=False)
        await channel.send(embed=embed)

    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        embed = discord.Embed(
            title = ":question: Help Panel",
            description = "These are the list of all the categories, Use command for the respective category to get list of commands of that specific category."
            )
        embed.color = Color.info
        for key in mapping:
            if key == None:
                pass
            elif key.qualified_name in ['Admin', 'HelpCommand', 'Eggs']:
                pass
            else:
                embed.add_field(
                    name=self.parse_cogname(key), 
                    value='`{}help {}`'.format(self.context.bot.prefixes_cache[str(self.context.guild.id)], key.qualified_name),
                    inline=False)
        await channel.send(embed=embed)


    async def send_command_help(self, command):
        '''
        Sends the help message about a certain command.


        [i] command.help.split(||)[1] is the required permissions if applicable.
        [i] command.description is the arguments help.
        [i] command.brief is the gitbook (docs) link to command.
        [i] command.usage is the command's usage.
        '''

        channel = self.get_destination()
        embed = discord.Embed(
            title = '`' + command.usage + '`',
            description = command.help if not '||' in command.help else command.help.split('||')[0],
            url=self.config.docs+command.brief # Gitbook Doc Link to command
            )
        embed.color = Color.info

        embed.add_field(name="Arguments", 
            value=command.description, inline=False)
        
        embed.add_field(name="Required Permissions", 
            value='No special permissions required.' if not '||' in command.help else command.help.split('||')[1], inline=False)
        
        embed.add_field(name="Aliases ({})".format(len(command.aliases)), 
            value=', '.join(command.aliases) if len(command.aliases) else 'No aliases', inline=False)
        
        embed.set_footer(text='Arguments in <> are required and arguments in [] are optional. Don\'t literally type <> or [].')
        await channel.send(embed=embed)



class HelpCommand(commands.Cog):
    '''
    This cog has the help command for bot.
    '''
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = CustomHelpCommand(config=self.bot.config)



def setup(bot):
    bot.add_cog(HelpCommand(bot))