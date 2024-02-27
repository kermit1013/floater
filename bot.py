from discord.ext import commands
import discord
import httpx
import json
import pendulum


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
        now = pendulum.now("Asia/Taipei")
        five_hour_ago = now.subtract(hours=5).format("YYYY-MM-DDTHH:00:00")
        
        params = {
            "Authorization": "rdec-key-123-45678-011121314",
            "StationID": "46757B",
            "WeatherElement": "WaveHeight,WaveDirection,WavePeriod,Temperature,PrimaryAnemometer",
            "sort": "DataTime",
            "timeFrom": five_hour_ago
        }
        print(params)

        response = client.get(url, params=params, headers=headers)
    
    # Check for successful response
    if response.status_code == 200:
        data = json.loads(response.text)

        # Extract and format the desired data
        parsed_data = [
            {
                "DateTime": obs_time["DateTime"],
                "WaveHeight": obs_time["WeatherElements"]["WaveHeight"],
                "WaveDirection": obs_time["WeatherElements"]["WaveDirection"],
                "WavePeriod": obs_time["WeatherElements"]["WavePeriod"],
                "Temperature": obs_time["WeatherElements"]["Temperature"],
                "WindSpeed": obs_time["WeatherElements"]["PrimaryAnemometer"]["WindSpeed"],
                "WindScale": obs_time["WeatherElements"]["PrimaryAnemometer"]["WindScale"],
                "WindDirectionDescription": obs_time["WeatherElements"]["PrimaryAnemometer"]["WindDirectionDescription"],
            }
            for obs_time in data["Records"]["SeaSurfaceObs"]["Location"][0]["StationObsTimes"]["StationObsTime"]
            ]



        # Print the parsed data in the desired format
        print(json.dumps(parsed_data, indent=4))
        markdown= [f'''
        > ## {pendulum.parse(data["DateTime"]).format("YY-MM-DD HH:mm")}
        > ### WAVE
        > _height_ `{data["WaveHeight"]}`
        > _period_ `{data["WavePeriod"]}`
        > _dir_ `{data["WaveDirection"]}`
        > ### WIND
        > _speed_ `{data["WindSpeed"]} / {data["WindScale"]}`
        > _dir_ `{data["WindDirectionDescription"]}`
        ''' for data in parsed_data]
        await ctx.send("".join(markdown))


    else:
        print(f"Error: {response.status_code}")



bot.run(BOT_TOKEN)