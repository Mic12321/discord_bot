# Author Mic12321

import discord
from discord.ext import commands
import asyncio
import datetime
import os



            
CLIENT_CMD_PREFIX="$$"
client=commands.Bot(intents=discord.Intents.all(), command_prefix=CLIENT_CMD_PREFIX, case_insensitive = True)



# Client event for connection
@client.event
async def on_connect():
    print("Connected to Discord")

@client.event
async def on_disconnect():
    print("Disconnected from Discord")


@client.event
async def on_resumed():
    print("Reconnected to Discord")


@client.event
async def on_ready():
    print("Ready")



# Client event for guild
@client.event
async def on_guild_join(guild):
    print(f"Joined a guild: {guild.name}")

    bot_join_guild_embed=discord.Embed(title=f"{CLIENT_NAME} is arrived~!",
        description="Thanks for adding me to your server.\nThis bot can help u to manage your server and provide a game big2\nCommand prefix is $$\nEnter $$help to get more help",
            color=0x3584e4)

    for txt_channel in guild.text_channels:

        if (txt_channel.permissions_for(guild.me).send_messages):
            await txt_channel.send(embed=bot_join_guild_embed)

        break


@client.event
async def on_guild_remove(guild):
    print(f"Left a guild: {guild.name}")


async def load_extensions():
    for Filename in os.listdir("./extensions"):
        if (Filename.endswith(".py")):
            await client.load_extension(F"extensions.{Filename[:-3]}")
            print(f"Loaded extension {Filename}")


# Connect to discord
async def main():
    async with client:
        #Client information
        CLIENT_TOKEN=open("../token.txt", "r").readline()

        client.CLIENT_NAME="lucky bot"
        client.CLIENT_AUTHOR="Mic12321"
        client.CLIENT_VERSION="0.1"
        client.CLIENT_START_TIME=datetime.datetime.now()

        client.CLIENT_REPOSITORY_URL="https://github.com/Mic12321/discord_bot"

        await load_extensions()
        await client.start(CLIENT_TOKEN)

asyncio.run(main())
