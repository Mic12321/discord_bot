import discord
from discord.ext import commands
import datetime
import sqlite3
from utilities import *

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
    async def create_game_room(self, ctx, room_name="magic"):
        game_room = Game_Room(room_name, [ctx.message.author.id], datetime.datetime.now().replace(microsecond=0))

        create_game_room_embed=discord.Embed(title=f"{game_room.get_room_name()} game room", color=0x3584e4)
        create_game_room_embed.add_field(name="Player amount", value="1")
        # create_game_room_embed.add_field(name="Created time", value=game_room.get_time_create(), inline=False)
        create_game_room_embed.add_field(name="Player joined", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=False)
        # sqliteConnection = sqlite3.connect("game.db")
        # cursor = sqliteConnection.cursor()

        
        message_id = await ctx.send(embed=create_game_room_embed)
        write_content("game_file", str(ctx.author.id))


    @commands.command()
    async def join_room(self, ctx, room_name="magic"):
        if (data_exists("game_file", ctx.author.id)):
            await ctx.send(f"<@{ctx.author.id}> You have joined the game already")
            return

        file=open("game_file", "r")

        content=file.readlines()
        file.close()
        player_amount=len(content)


        if (player_amount==4):
            await ctx.send("The room is full")
            file.close()
            return


        append_content("game_file", ctx.author.id)
        await ctx.send(f"<@{ctx.author.id}> You joined the game successfully")


        file=open("game_file", "r")
        content=file.readlines()
        player_amount=len(content)
        user_name_list=[]
        for i in content:
            if(i[-1] == '\n'):
                i = i[:-1]

            user = await self.client.fetch_user(int(i))
            user_name_list.append(str(user.name))


        join_game_embed=discord.Embed(title=f"Game room", color=0x3584e4)
        join_game_embed.add_field(name="Player amount", value=player_amount, inline=False)
        join_game_embed.add_field(name="Player joined", value=f"{user_name_list}", inline=False)
        await ctx.send(embed=join_game_embed)



    @commands.command()
    async def leave_room(self, ctx):
        if not (data_exists("game_file", ctx.author.id)):
            await ctx.send(f"<@{ctx.author.id}> You did not join the game")
            return

        remove_content("game_file", ctx.author.id)
        await ctx.send(f"<@{ctx.author.id}> You have left the game successfully")
        


    @commands.command()
    async def start_game(self, ctx):
        await ctx.send("Force start")
        


    
    
    
    
async def setup(client):
    await client.add_cog(Game(client))