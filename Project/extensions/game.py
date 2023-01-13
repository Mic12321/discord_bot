import discord
from discord.ext import commands
import datetime
import sqlite3

class Game_Room:
    def __init__(self, room_name, players_id, time_create):
        self.__room_name=room_name
        self.__players_id=players_id
        self.__time_create=time_create

    def get_room_name(self):
        return self.__room_name
    
    def get_players_id(self):
        return self.__players_id

    def get_time_create(self):
        return self.__time_create



class Game(commands.Cog):   
    def __init__(self, client):
        self.client=client
    
    @commands.command()
    async def start_game(self, ctx, room_name="magic"):
        game_room = Game_Room(room_name, ctx.message.author.id, datetime.datetime.now())

        start_game_embed=discord.Embed(title=f"{game_room.get_room_name()} game room", color=0x3584e4)
        
        start_game_embed.add_field(name="Time created", value=game_room.get_time_create(), inline=False)
        start_game_embed.add_field(name="Player joined", value=game_room.get_players_id(), inline=False)
        sqliteConnection = sqlite3.connect("game.db")
        cursor = sqliteConnection.cursor()

        
        await ctx.send(embed=start_game_embed)


    @commands.command()
    async def leave(self, ctx):
        await ctx.send("leave")
        


    @commands.command()
    async def force_start(self, ctx):
        await ctx.send("Force start")
        


    
    
    
    
async def setup(client):
    await client.add_cog(Game(client))