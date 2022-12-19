# Author Mic12321

import discord
from discord.ext import commands
import asyncio
import datetime


def main():

    # Client information
    CLIENT_TOKEN=open("../token.txt", "r").readline()
    CLIENT_NAME="lucky bot"
    CLIENT_AUTHOR="Mic12321"
    CLIENT_VERSION="0.1"
    CLIENT_START_TIME=datetime.datetime.now()
    CLIENT_CMD_PREFIX="$$"
    CLIENT_REPOSITORY_URL="https://github.com/Mic12321/discord_bot"

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


    # Commands
    @client.command(aliases=["bs"])
    async def bot_status(ctx):
        bot_status_embed=discord.Embed(title="BOT STATUS", color=0x3584e4)
        bot_status_embed.add_field(name="Latency", value=f"{round(client.latency*1000, 2)} ms", inline=False)
        bot_status_embed.add_field(name="Run time", value=datetime.datetime.now()-CLIENT_START_TIME, inline=False)
        bot_status_embed.add_field(name="Serving", value=f"{(len(client.guilds))} servers", inline=False)

        await ctx.send(embed=bot_status_embed)



    # Guild status
    @client.command(aliases=["gs", "guild_status"])
    async def status(ctx):
        human_count=len([mem for mem in ctx.guild.members if not mem.bot])
        all_count=len(ctx.guild.members)
        status_embed=discord.Embed(title="GUILD STATUS", color=0x3584e4)
        status_embed.add_field(name="Member count", value=f"{human_count} human users\n{all_count-human_count} bots\n{all_count} in total", inline=False)
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
        info_embed.add_field(name="Version", value="0.1", inline=False)
        await ctx.send(embed=info_embed)



    # Manage server
    @client.command()
    async def create_category(ctx, name):
        await ctx.guild.create_category(name)


    @client.command()
    async def create_text_channel(ctx, name):
        await ctx.message.guild.create_text_channel(name)



    # TODO
    # Bigtwo Game (DM)
    @client.command()
    async def create(ctx, room_name, auto_join=True):
        await ctx.send(ctx.channel.id)
        await ctx.send(f"You have successfully created a new room {room_name}")

    # TODO
    @client.command()
    async def join(ctx, room_name):
        await ctx.send(f"You have successfully joined {room_name}")



    # Connect to discord
    client.run(CLIENT_TOKEN)


if __name__ == "__main__":
    main()
