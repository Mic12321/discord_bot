# Author Mic12321

import discord
from discord.ext import commands
import asyncio
import datetime
from utilities import data_exists, extension_exists
import os




            
CLIENT_CMD_PREFIX="$$"
client=commands.Bot(intents=discord.Intents.all(), command_prefix=CLIENT_CMD_PREFIX, case_insensitive = False)


@client.command()
async def load(ctx, extension_name):
    if not (data_exists("admin.txt", ctx.author.id)):
        await ctx.send("You are not admin")
        return

    if not (extension_exists(extension_name)):
        await ctx.send(f"Extension {extension_name} is not exists")
        return
    
    try:
        for Filename in os.listdir("./extensions"):
            if (Filename.endswith(".py") and extension_name==Filename[:-3]):
                print(f"Loading {extension_name}")
                await client.load_extension(F"extensions.{extension_name}") 
                print(f"Loaded {extension_name}")
                await ctx.send(f"Loaded extension {extension_name}")
                return
        
        await ctx.send(f"Extension {extension_name} is not exists")

    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f"Extension {extension_name} has already loaded")

    
@client.command()
async def reload(ctx, extension_name):
    if not (data_exists("admin.txt", ctx.author.id)):
        await ctx.send("You are not admin")
        return

    if not (extension_exists(extension_name)):
        await ctx.send(f"Extension {extension_name} is not exists")
        return

    try:
        if (commands.ExtensionAlreadyLoaded(extension_name)):
            for Filename in os.listdir("./extensions"):
                if (Filename[:-3]==extension_name):
                    print(f"Reloading {extension_name}")
                    await client.reload_extension(F"extensions.{extension_name}") 
                    print(f"Reloaded {extension_name}")
                    await ctx.send(f"Reloaded extension {extension_name}")
                    return

        await ctx.send(f"Extension {extension_name} is not loaded")

    except:
        await ctx.send(f"Extension {extension_name} is not loaded")


@client.command()
async def unload(ctx, extension_name):
    if not (is_bot_admin("admin.txt", ctx.author.id)):
        await ctx.send("You are not admin")
        return

    if not (extension_exists(extension_name)):
        await ctx.send(f"Extension {extension_name} is not exists")
        return

    try:
        if (commands.ExtensionAlreadyLoaded(extension_name)):
            for Filename in os.listdir("./extensions"):
                if (Filename[:-3]==extension_name):
                    print(f"Unloading {extension_name}")
                    await client.unload_extension(F"extensions.{extension_name}") 
                    print(f"Unloaded {extension_name}")
                    await ctx.send(f"Unloaded extension {extension_name}")
                    return

        await ctx.send(f"Extension {extension_name} is not loaded")

    except:
        await ctx.send(f"Extension {extension_name} is not loaded")




async def load_extensions():
    for Filename in os.listdir("./extensions"):
        if (Filename.endswith(".py")):
            await client.load_extension(F"extensions.{Filename[:-3]}")
            print(f"Loaded extension {Filename}")





# Connect to discord
async def main():
    async with client:
        #Client information
        
        file=open("../token.txt", "r")
        CLIENT_TOKEN=file.readline()
        file.close()

        client.CLIENT_NAME="lucky bot"
        client.CLIENT_AUTHOR="Mic12321"
        client.CLIENT_VERSION="0.1"
        client.CLIENT_START_TIME=datetime.datetime.now()

        client.CLIENT_REPOSITORY_URL="https://github.com/Mic12321/discord_bot"
        await load_extensions()
        await client.start(CLIENT_TOKEN)

asyncio.run(main())
