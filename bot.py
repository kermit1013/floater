from discord.ext import commands
import discord
import os
import asyncio



intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "$", intents = intents)

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"目前登入身份 --> {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")

@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")

@bot.command()
async def sync(ctx: commands.Context):
    # sync to the guild where the command was used
    bot.tree.copy_global_to(guild=ctx.guild)
    await bot.tree.sync(guild=ctx.guild)
    await ctx.send(content="Success")

@bot.command()
async def sync_global(ctx: commands.Context):
    # sync globally
    await bot.tree.sync()
    await ctx.send(content="Success")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

# async def load_extensions():
#     for cog in [p.stem for p in Path(".").glob("./cogs/*.py")]:
#         bot.load_extension(f'cogs.{cog}')
#         print(f'Loaded {cog}.')
#     print('Done.')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(BOT_TOKEN)

# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())
