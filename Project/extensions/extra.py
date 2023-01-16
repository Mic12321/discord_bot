import discord
from discord.ext import commands
import datetime

class Extra(commands.Cog):   
    def __init__(self, client):
        self.client=client
    
    @commands.command()
    async def look_up_by_id(self, ctx, user_id):
        user=await self.client.fetch_user(user_id)

        user_info_name = {
            "Name": user.name, 
            "ID": user.id, 
            "Discriminiator": user.discriminator,
            "avatar": user.avatar,
            "Bot": user.bot, 
            "System": user.system, 
            "Created at": user.created_at, 
            "Display name": user.display_name,
            "Public flags": user.public_flags
            }

        user_info_embed=discord.Embed(title="USER INFORMATION", color=0x3584e4)
        for i in user_info_name:
            user_info_embed.add_field(name=i, value=user_info_name[i], inline=False)
        
        
        await ctx.send(embed=user_info_embed)

    

    
    
    
    
async def setup(client):
    await client.add_cog(Extra(client))