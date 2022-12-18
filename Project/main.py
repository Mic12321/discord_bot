# Author Mic12321

import discord
from discord.ext import commands
import asyncio
import datetime

def main():

    client=commands.Bot(intents=discord.Intents.all(), command_prefix="$$", case_insensitive = True)

    # Client information
    CLIENT_TOKEN=open("../token.txt", "r").readline()
    CLIENT_NAME="lucky bot"
    CLIENT_AUTHOR="Mic12321"
    CLIENT_VERSION="0.1"
    CLIENT_START_TIME=datetime.datetime.now()

    # Client event
    @client.event
    async def on_connect():
        print("Bot connected to Discord")

    @client.event
    async def on_disconnect():
        print("Bot disconnected from Discord")


    @client.event
    async def on_resumed():
        print("Bot reconnected to Discord")


    @client.event
    async def on_ready():
        print("Bot is ready")



    # Client command
    @client.command()
    async def status(ctx):
        status_embed=discord.Embed(title="BOT STATUS", color=0x3584e4)
        status_embed.add_field(name="Latency", value=f"{round(client.latency*1000, 2)} ms", inline=False)
        status_embed.add_field(name="Run time", value=datetime.datetime.now()-CLIENT_START_TIME, inline=False)
        await ctx.send(embed=status_embed)

    @client.command()
    async def clean(ctx, amount=2):
        if (101>amount>0):
            await ctx.channel.purge(limit = int(amount))
            await ctx.send(f"Cleaned {amount} messages", delete_after=3)

        else:
            await ctx.send("clean quantity should be between 1 and 100", delete_after=3)

    @client.command()
    async def info(ctx):
        info_embed=discord.Embed(title="BOT INFORMATION", color=0x3584e4)
        info_embed.add_field(name="Author", value="Mic12321", inline=False)
        info_embed.add_field(name="Version", value="0.3", inline=False)
        await ctx.send(embed=info_embed)



    # Connect to discord
    client.run(CLIENT_TOKEN)


if __name__ == "__main__":
    main()
