import discord
from discord.ext import commands
import datetime
import sqlite3
from utilities import *
import random

class Player:
    def __unit__(self, name, hand):
        self.name = name
        self.hand = hand

class Game_Room(commands.Cog):
    def __init__(self, room_name, players, time_create):
        self.__room_name=room_name
        self.__players=players
        self.__time_create=time_create

    @commands.command()
    async def create_game_room(self, ctx, room_name="magic"):
        self.game_room = Game_Room(room_name, [ctx.message.author.id], datetime.datetime.now().replace(microsecond=0))

        create_game_room_embed=discord.Embed(title=f"{self.game_room.get_room_name()} game room", color=0x3584e4)
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

    def get_room_name(self):
        return self.__room_name
    
    def get_players_id(self):
        return self.__players

    def get_time_create(self):
        return self.__time_create

    class Game:   
        def __init__(self, client):
            self.client = client

            self.powers = { "3♦" : 1, " 3♣" : 2,  "3♥" : 3,  "3♠" : 4,
                            "4♦" : 5,  "4♣" : 6,  "4♥" : 7,  "4♠" : 8,
                            "5♦" : 9,  "5♣" : 10, "5♥" : 11, "5♠" : 12,
                            "6♦" : 13, "6♣" : 14, "6♥" : 15, "6♠" : 16,
                            "7♦" : 17, "7♣" : 18, "7♥" : 19, "7♠" : 20,
                            "8♦" : 21, "8♣" : 22, "8♥" : 23, "8♠" : 24,
                            "9♦" : 25, "9♣" : 26, "9♥" : 27, "9♠" : 28,
                            "T♦" : 29, "T♣" : 30, "T♥" : 31, "T♠" : 32,
                            "J♦" : 33, "J♣" : 34, "J♥" : 35, "J♠" : 36,
                            "Q♦" : 37, "Q♣" : 38, "Q♥" : 39, "Q♠" : 40,
                            "K♦" : 41, "K♣" : 42, "K♥" : 43, "K♠" : 44,
                            "A♦" : 45, "A♣" : 46, "A♥" : 47, "A♠" : 48,
                            "2♦" : 49, "2♣" : 50, "2♥" : 51, "2♠" : 52  }

            self.deck = list(self.powers.keys())

            self.passes = 0
            self.current_player = 0
            self.current_power = 0
            self.current_cards = []
            self.user_power = 0
            self.combination = 0

        # use this function to sort by power
        def takepower(self, elem):
            return self.powers[elem]

        # check if cards is a straight
        def straight(self, cards):
            cards.sort(key = self.takepower)
            card_powers = [(self.powers[cards[0]] - 1) // 4, (self.powers[cards[1]] - 1) // 4, (self.powers[cards[2]] - 1) // 4, (self.powers[cards[3]] - 1) // 4, (self.powers[cards[4]] - 1) // 4]
            
            if card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2:  # normal straight
                return self.powers[cards[4]]

            elif card_powers[0] + 10 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2: # Q K A 2 3
                return self.powers[cards[4]]

            elif card_powers[0] + 10 == card_powers[1] + 9 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2: # K A 2 3 4
                return self.powers[cards[4]]

            elif card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 9 == card_powers[4] - 10: # A 2 3 4 5
                return self.powers[cards[4]]

            elif card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 10: # 2 3 4 5 6
                return self.powers[cards[4]]

            # not a straight
            else:
                return 0

        # check if cards is a flush
        def flush(self, cards):
            
            if cards[0][1] == cards[1][1] == cards[2][1] == cards[3][1] == cards[4][1]:
                return self.powers[max(cards, key=self.takepower)]

            else:
                return 0

        # check if cards is a full house
        def full_house(self, cards):
            cards.sort(key = self.takepower)

            if cards[0][0] == cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0]:    # 3 3 3 4 4 and other
                return self.powers[cards[2]]

            elif cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]:  # 3 3 4 4 4 and other
                return self.powers[cards[4]]

            else:
                return 0

        # check if cards is a four of a kind
        def four_of_a_kind(self, cards):
            cards.sort(key = self.takepower)

            if cards[0][0] == cards[1][0] == cards[2][0] == cards[3][0]:        # 3 3 3 3 4 and other
                return self.powers[cards[3]]

            elif cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]:     # 3 4 4 4 4 and other
                return self.powers[cards[4]]

            else:
                return 0

        # check if cards is a straight flush
        def straight_flush(self, cards):

            if self.straight(cards) != 0 and self.flush(cards) != 0:
                return self.powers[max(cards, key=self.takepower)]

            else:
                return 0

        async def send_deck(self, ctx, player):
            await ctx.send(f"/msg user:{player.name} message:{' '.join(player.hand)}")
            await ctx.send(f"/msg user:{player.name} message:{' '.join(sorted(player.hand, key=self.takepower))}")
            await ctx.send(f"/msg user:{player.name} message:{' '.join([str(i+1) + ' ' * (1-(i+1)//10) for i in range(len(player.hand))])}")

        @commands.command()
        async def start_game(self, ctx):

            # shuffle the deck
            for i in range(random.randint(10, 100)):
                random.shuffle(self.deck)

            # players - save the array of Player objects, it has .name - name and .hand - array of cards
            self.__players = [self.client.fetch_user(int(i)) for i in self.game_room.get_players_id()]
            self.__players = [Player(self.__players[i], [self.deck[j] for j in range(len(self.deck)) if j%4 == i]) for i in range(len(self.__players))]

            # choose the current player accouring to "smallest card" rule :)
            self.current_player = [min(self.__players[i].hand, key=self.takepower) for i in range(len(self.__players))].index(min([min(self.__players[i].hand[i], key=self.takepower) for i in range(len(self.__players))]))

            await ctx.send("Game started")

            # option 1, if work, do not touch it :)
            self.send_deck(self, ctx, self.__players[self.current_player])

            # else -> use option 2:
            # await self.send_deck(self, ctx, self.__players[self.current_player])

        @commands.command()
        async def play(self, ctx, cards):
            userinput = cards.split()
            
            userchoice = [int(i) - 1 for i in userinput if i.isdigit()]
            userchoice.sort(reverse = True)

            # invalid choices
            if len(userchoice) != len(userinput) or not userchoice:
                await ctx.send("Invalid choice")
                return -1
            
            # pass option
            if userchoice[0] == -1:

                # invalid pass
                if self.combination == 0:
                    await ctx.send("You should not pass at the start of the circle")
                
                # valid pass
                else:
                    await ctx.send("Pass")
                    self.passes += 1

                    # if all people pass (new circle start)
                    if self.passes == len(self.__players) - 1:
                        await ctx.send("All people pass")
                        self.combination = 0
                        self.current_power = 0
                        self.passes = 0

                    else:
                        await ctx.send(f"Current cards: {' '.join(self.current_cards)}")
                
                return 1
            
            # check if all choices are valid
            for card_number in userchoice:

                # invalid turn
                if card_number >= len(self.__players[self.current_player].hand):
                    await ctx.send("Invalid choice")
                    return -1
            
            # cards that user want to play
            cards = []
            for card_number in userchoice:
                cards.append(self.__players[self.current_player].hand[card_number])

            if len(cards) == 1:     # 1 card 
                self.user_power = self.powers[cards[0]]
            
            elif len(cards) == 2:   # 2 cards (pair)
                if cards[0][0] == cards[1][0]:
                    self.user_power = self.powers[max(cards, key=self.takepower)]
                else:
                    await ctx.send("Your choice is not a valid pair")
                    self.user_power = -1

            elif len(cards) == 3:   # 3 cards (triple)
                if cards[0][0] == cards[1][0] == cards[2][0]:
                    self.user_power = self.powers[max(cards, key=self.takepower)]
                else:
                    await ctx.send("Your choice is not a valid triple")
                    self.user_power = -1
            
            elif len(cards) == 5:   # 5 cards combinations
                
                if self.straight_flush(cards) != 0:      # straight flush
                    self.user_power = self.straight_flush(cards) + 400

                elif self.four_of_a_kind(cards) != 0:     # four of a kind
                    self.user_power = self.four_of_a_kind(cards) + 300

                elif self.full_house(cards) != 0:         # full house
                    self.user_power = self.full_house(cards) + 200

                elif self.flush(cards) != 0:              # flush
                    self.user_power = self.flush(cards) + 100

                elif self.straight(cards) != 0:           # straight
                    self.user_power = self.straight(cards)

                else:
                    await ctx.send("Your choice is not a valid 5 cards combination")
                    self.user_power = -1

            else:       # invalid number of cards
                await ctx.send("Invalid number of cards chosen")
                self.user_power = -1

            # invalid choice -- try another attempt
            if self.user_power == -1:
                return -1

            # no combination (start of the circle)
            if self.combination == 0:
                await ctx.send(f"Played cards: {' '.join(cards)}")

                self.combination = len(cards)
                self.current_cards = cards
                self.current_power = self.user_power

                # remove the played cards from the hand
                for card_number in userchoice:
                    del self.__players[self.current_player].hand[card_number]

                # finish the turn
                self.passes = 0
                return 1
            
            # check if it is a valid combination
            elif self.combination == len(cards):

                # if valid choice
                if self.user_power > self.current_power:
                    await ctx.send(f"Played cards: {' '.join(cards)}")

                    self.current_cards = cards
                    self.current_power = self.user_power

                    # remove the played cards from the hand
                    for card_number in userchoice:
                        del self.__players[self.current_player].hand[card_number]

                     # finish the turn
                    self.passes = 0
                    return 1

                # weaker combination
                else:
                    await ctx.send("Your card is not good enough to beat it, try again")
                    return -1
            
            # invalid combination
            else:
                await ctx.send(f"Invalid combination, current combination is {self.combination} cards")
                return -1
                
async def setup(client):
    await client.add_cog(Game_Room(client))