import discord
from discord.ext import commands
import datetime

class Manage(commands.Cog):   
    def __init__(self, client):
        self.client=client


    ##
    @commands.command(aliases=["clear"])
    async def clean(self, ctx, amount="2"):
        
        try:
            int_amount=int(amount)
            if (101>int_amount>0):
                await ctx.channel.purge(limit = int_amount)
                await ctx.send(f"Cleaned {amount} messages", delete_after=3)

            else:
                await ctx.send("clean quantity should be between 1 and 100, and must be an integer", delete_after=3)

        except:
            await ctx.send("clean quantity should be between 1 and 100, and must be an integer", delete_after=3)

    @commands.command()
    async def create_category(self, ctx, name):
        await ctx.guild.create_category(name)


    @commands.command()
    async def create_text_channel(self, ctx, name):
        await ctx.message.guild.create_text_channel(name)

    # Guild status
    @commands.command(aliases=["gs", "status", "guild_status"])
    async def status_guild(self, ctx):
        human_count=len([mem for mem in ctx.guild.members if not mem.bot])
        all_count=len(ctx.guild.members)
        status_embed=discord.Embed(title="GUILD STATUS", color=0x3584e4)
        status_embed.add_field(name="Member count", value=f"{human_count} human users\n{all_count-human_count} bots\n{all_count} in total", inline=False)
        await ctx.send(embed=status_embed)


async def setup(client):
    await client.add_cog(Manage(client))