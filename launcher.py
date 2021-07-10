import bot
import json
from discord import Intents

intents = Intents.default()
intents.members = True

with open('config.json', 'r') as f:
    config = json.load(f)

ignore_exts = []
bot_type = 'production'

bot.run(config['bots'][bot_type]['token'], intents, ignore_exts, True)