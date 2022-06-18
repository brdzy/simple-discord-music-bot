import nextcord
from nextcord.ext import commands
from nextcord import Interaction


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    testServerId = YOUR_SERVER_ID_HERE

    @nextcord.slash_command(name='ping', description='You can check bots latency.', guild_ids=[testServerId])
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f'```\nBots latency is: {round(self.bot.latency * 1000)}ms\n```')


def setup(bot):
    bot.add_cog(Ping(bot))
