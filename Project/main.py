# Author Mic12321

import discord
from discord.ext import commands
import asyncio

def main():

    client=commands.Bot(intents=discord.Intents.all(), command_prefix="$$", case_insensitive = True)


    @client.event
    async def on_ready():
        print("Bot is ready")

    @client.command()
    async def test(ctx):
        print("test is working")
        await ctx.send("test is working")


    # Read the token from token.txt
    client.run(open("../token.txt", "r").readline())


if __name__ == "__main__":
    main()
