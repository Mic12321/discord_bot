import discord
from discord.ext import commands
import datetime
from utilities import is_bot_admin, extension_exists

class Root(commands.Cog):   
    def __init__(self, client):
        self.client=client
    

    # Client event for connection
    @commands.Cog.listener()
    async def on_connect(self):
        print("Connected to Discord")

    @commands.Cog.listener()
    async def on_disconnect(self):
        print("Disconnected from Discord")


    @commands.Cog.listener()
    async def on_resumed(self):
        print("Reconnecteselfd to Discord")


    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready")

    # Client event for guild
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined a guild: {guild.name}")

        bot_join_guild_embed=discord.Embed(title=f"{CLIENT_NAME} is arrived~!",
            description="Thanks for adding me to your server.\nThis bot can help u to manage your server and provide a game big2\nCommand prefix is $$\nEnter $$help to get more help",
                color=0x3584e4)

        for txt_channel in guild.text_channels:

            if (txt_channel.permissions_for(guild.me).send_messages):
                await txt_channel.send(embed=bot_join_guild_embed)
                break


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"Left a guild: {guild.name}")



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error, ctx.message.content)
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Bot does not have this command: {ctx.message.content}")

        else:
            await ctx.send(error)


    @commands.command()
    async def magic(self, ctx):
        await ctx.send("Scriptluck is not here~ Magic~!")

    @commands.command(aliases=["i?", "me?"])
    async def whoami(self, ctx):
        whoami_embed=discord.Embed(title="YOUR INFORMATION", color=0x3584e4)
        whoami_embed.add_field(name="ID", value=ctx.author.id, inline=False)
        whoami_embed.add_field(name="Username", value=ctx.author.name, inline=False)
        whoami_embed.add_field(name="User's tag", value=ctx.author.discriminator, inline=False)
        await ctx.send(embed=whoami_embed)

    @commands.command(aliases=["admin?"])
    async def amibotadmin(self, ctx):
        await ctx.send({is_bot_admin(ctx.author.id)})


async def setup(client):
    await client.add_cog(Root(client))