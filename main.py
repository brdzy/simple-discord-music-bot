import nextcord
import os
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Game(name="Fortnite"))
    print('------------------------')
    print('The bot is ready to use!')
    print('------------------------')


initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run('YOUR_TOKEN_HERE')
