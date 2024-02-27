from discord.ext import commands
import discord
import httpx
import json

BOT_TOKEN="MTIxMTg0MTM0NTI2NjkxNzQzNg.G8j7S5.3gAA9tIFlTtzqWssCrIXzZRwQc18DsiuW5KrKk"
CHANNEL_ID="1211840720369877004"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# @bot.event
# async def on_ready():

#     channel = bot.get_channel(CHANNEL_ID)
#     await channel.send("test text")


@bot.command()
async def h(ctx):
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-B0075-001"
    headers = {
        "Authorization": "rdec-key-123-45678-011121314",
    }

    with httpx.Client() as client:
        params = {
            "Authorization": "rdec-key-123-45678-011121314",
            "StationID": "46757B",
            "WeatherElement": "WaveHeight,WaveDirection,WavePeriod,Temperature,PrimaryAnemometer",
            "sort": "DataTime",
            "timeFrom": "2024-02-27T09:00:00",
        }

        response = client.get(url, params=params, headers=headers)
    
    # Check for successful response
    if response.status_code == 200:
        data = json.loads(response.text)

        # Extract and format the desired data
        parsed_data = {
            "StationID": data["Records"]["SeaSurfaceObs"]["Location"][0]["Station"]["StationID"],
            "StationObsTime": []
        }

        for obs_time in data["Records"]["SeaSurfaceObs"]["Location"][0]["StationObsTimes"]["StationObsTime"]:
            parsed_data["StationObsTime"].append({
                "DateTime": obs_time["DateTime"],
                "WaveHeight": obs_time["WeatherElements"]["WaveHeight"],
                "WaveDirection": obs_time["WeatherElements"]["WaveDirection"],
                "WavePeriod": obs_time["WeatherElements"]["WavePeriod"],
                "Temperature": obs_time["WeatherElements"]["Temperature"],
                "WindSpeed": obs_time["WeatherElements"]["PrimaryAnemometer"]["WindSpeed"],
                "WindScale": obs_time["WeatherElements"]["PrimaryAnemometer"]["WindScale"],
                "WindDirectionDescription": obs_time["WeatherElements"]["PrimaryAnemometer"]["WindDirectionDescription"],
            })

        # Print the parsed data in the desired format
        print(json.dumps(parsed_data, indent=4))

        await ctx.send(json.dumps(parsed_data, indent=4))

    else:
        print(f"Error: {response.status_code}")



bot.run(BOT_TOKEN)