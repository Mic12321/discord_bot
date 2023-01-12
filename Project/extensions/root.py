import discord
from discord.ext import commands
import datetime

class Root(commands.Cog):   
    def __init__(self, client):
        self.client=client
    
    @commands.command()
    async def status_bot(self, ctx):
        bot_status_embed=discord.Embed(title="BOT STATUS", color=0x3584e4)
        bot_status_embed.add_field(name="Latency", value=f"{round(self.client.latency*1000, 2)} ms", inline=False)
        bot_status_embed.add_field(name="Run time", value=datetime.datetime.now()-self.client.CLIENT_START_TIME, inline=False)
        bot_status_embed.add_field(name="Serving", value=f"{(len(self.client.guilds))} servers", inline=False)

        await ctx.send(embed=bot_status_embed)



    # Guild status
    @commands.command(aliases=["gs", "guild_status"])
    async def status(self, ctx):
        human_count=len([mem for mem in ctx.guild.members if not mem.bot])
        all_count=len(ctx.guild.members)
        status_embed=discord.Embed(title="GUILD STATUS", color=0x3584e4)
        status_embed.add_field(name="Member count", value=f"{human_count} human users\n{all_count-human_count} bots\n{all_count} in total", inline=False)
        await ctx.send(embed=status_embed)


    @commands.command(aliases=["clear"])
    async def clean(self, ctx, amount=2):
        if (101>amount>0):
            await ctx.channel.purge(limit = int(amount))
            await ctx.send(f"Cleaned {amount} messages", delete_after=3)

        else:
            await ctx.send("clean quantity should be between 1 and 100", delete_after=3)

    @commands.command()
    async def info(self, ctx):
        info_embed=discord.Embed(title="BOT INFORMATION", color=0x3584e4)
        info_embed.add_field(name="Author", value=self.client.CLIENT_AUTHOR, inline=False)
        info_embed.add_field(name="Version", value=self.client.CLIENT_VERSION, inline=False)
        await ctx.send(embed=info_embed)



    # Manage server
    @commands.command()
    async def create_category(self, ctx, name):
        await ctx.guild.create_category(name)


    @commands.command()
    async def create_text_channel(self, ctx, name):
        await ctx.message.guild.create_text_channel(name)
    
    
    
    
async def setup(client):
    await client.add_cog(Root(client))