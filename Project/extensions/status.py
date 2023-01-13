import discord
from discord.ext import commands
import datetime

class Status(commands.Cog):   
    def __init__(self, client):
        self.client=client
    
    @commands.command()
    async def status_bot(self, ctx):
        bot_status_embed=discord.Embed(title="BOT STATUS", color=0x3584e4)
        bot_status_embed.add_field(name="Latency", value=f"{round(self.client.latency*1000, 2)} ms", inline=False)
        bot_status_embed.add_field(name="Run time", value=datetime.datetime.now()-self.client.CLIENT_START_TIME, inline=False)
        bot_status_embed.add_field(name="Serving", value=f"{(len(self.client.guilds))} servers", inline=False)

        await ctx.send(embed=bot_status_embed)


    @commands.command()
    async def info(self, ctx):
        info_embed=discord.Embed(title="BOT INFORMATION", color=0x3584e4)
        info_embed.add_field(name="Author", value=self.client.CLIENT_AUTHOR, inline=False)
        info_embed.add_field(name="Version", value=self.client.CLIENT_VERSION, inline=False)
        await ctx.send(embed=info_embed)
    
    
async def setup(client):
    await client.add_cog(Status(client))