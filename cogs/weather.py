import nextcord
from nextcord.ext import commands
import requests
from nextcord import Interaction

api_key = "YOUR_API_KEY_HERE"
base_url = "http://api.openweathermap.org/data/2.5/weather?"


class Weather(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    testServerId = YOUR_SERVER_ID_HERE

    @nextcord.slash_command(name='weather', description='You can check any citys weather.', guild_ids=[testServerId])
    async def weather(self, interaction: Interaction, *, city: str):
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":

            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]

            weather_description = z[0]["description"]
            embed = nextcord.Embed(title=f"Weather in {city_name}", color=interaction.guild.me.top_role.color)
            embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature", value=f"**{current_temperature_celsiuis}°C**", inline=False)
            embed.add_field(name="Humidity", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Atmospheric pressure", value=f"**{current_pressure}hPa**", inline=False)
            embed.set_image(url="https://c.tenor.com/ZAEa_nWK5fkAAAAC/niilo22-mikael-kosola.gif")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f'```\nCouldnt find that city.\n```')


def setup(bot):
    bot.add_cog(Weather(bot))
