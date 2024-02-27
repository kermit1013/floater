import discord 
from discord.ext import commands
from discord import app_commands
import httpx
import json
import pendulum

# 定義名為 Main 的 Cog
class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # @app_commands.describe(參數名稱 = 參數敘述)
    # 參數: 資料型態，可以限制使用者輸入的內容
    @app_commands.command(name = "buoyant", description = "取得過去五小時浮標資料")
    @app_commands.describe(location = "輸入資料站編號")
    async def add(self, interaction: discord.Interaction, location: str):
        url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-B0075-001"
        headers = {
            "Authorization": "rdec-key-123-45678-011121314",
        }

        with httpx.Client() as client:
            now = pendulum.now("Asia/Taipei")
            five_hour_ago = now.subtract(hours=5).format("YYYY-MM-DDTHH:00:00")
            # 46757B
            params = {
                "Authorization": "rdec-key-123-45678-011121314",
                "StationID": location,
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
            await interaction.response.send_message("".join(markdown))


        else:
            print(f"Error: {response.status_code}")


       

    # 前綴指令
    @commands.command()
    async def Hello(self, ctx: commands.Context):
        await ctx.send("Hello, world!")

    # 關鍵字觸發
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content == "Hello":
            await message.channel.send("Hello, world!")
   

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
