import discord
from discord.ext import commands
import datetime
import sqlite3
from utilities import *
import random

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

class Game():   
    def __init__(self, players):
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

        # shuffle the deck
        for i in range(random.randint(10, 100)):
            random.shuffle(self.deck)

        # players - save the array of Player objects, it has .name - name and .hand - array of cards
        self.__players = [Player(f"{players[i]}", [self.deck[j] for j in range(len(self.deck)) if j%4 == i]) for i in range(len(players))]

        # choose the current player accouring to "smallest card" rule :)
        self.current_player = [min(self.__players[i].hand, key=self.takepower) for i in range(len(self.__players))].index(min([min(self.__players[i].hand, key=self.takepower) for i in range(len(self.__players))], key=self.takepower))

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

        elif cards[1][0] == cards[2][0] == cards[3][0] == cards[4][0]:     # 3 4 4 4 4 and other
            return self.powers[cards[4]]

        else:
            return 0

    # check if cards is a straight flush
    def straight_flush(self, cards):
        if self.straight(cards) != 0 and self.flush(cards) != 0:
            return self.powers[max(cards, key=self.takepower)]

        else:
            return 0

    def show_deck(self):
        sorted_hand = f"/msg user:{self.__players[self.current_player].name} message:{' '.join(sorted(self.__players[self.current_player].hand, key=self.takepower))}"
        hand = f"/msg user:{self.__players[self.current_player].name} message:{' '.join(self.__players[self.current_player].hand)}"
        options = f"/msg user:{self.__players[self.current_player].name} message:{' '.join([str(i+1) + ' ' * 6 for i in range(len(self.__players[self.current_player].hand))])}"

        return [sorted_hand, hand, options]

    def turn(self, cards):
        userinput = cards.split()
        userchoice = [int(i) - 1 for i in userinput if i.isdigit()]
        userchoice.sort(reverse = True)

        # invalid choices
        if len(userchoice) != len(userinput) or not userchoice:
            return ["Invalid choice", -1]
        
        # pass option
        if userchoice[0] == -1:

            # invalid pass
            if self.combination == 0:
                return ["You should not pass at the start of the circle", -1]
            
            # valid pass
            else:
                self.passes += 1

                # if all people pass (new circle start)
                if self.passes == len(self.__players) - 1:
                    self.combination = 0
                    self.current_power = 0
                    self.passes = 0
                    return ["All people pass", 0]

                else:
                    return [f"Pass... Current cards: {' '.join(self.current_cards)}", 0]
        
        # check if all choices are valid
        for card_number in userchoice:

            # invalid turn
            if card_number >= len(self.__players[self.current_player].hand):
                return ["Invalid choice", -1]
        
        # cards that user want to play
        cards = [self.__players[self.current_player].hand[card_number] for card_number in userchoice]

        if len(cards) == 1:     # 1 card 
            self.user_power = self.powers[cards[0]]
        
        elif len(cards) == 2:   # 2 cards (pair)
            if cards[0][0] == cards[1][0]:
                self.user_power = self.powers[max(cards, key=self.takepower)]
            else:
                self.user_power = -1
                return ["Your choice is not a valid pair", -1]

        elif len(cards) == 3:   # 3 cards (triple)
            if cards[0][0] == cards[1][0] == cards[2][0]:
                self.user_power = self.powers[max(cards, key=self.takepower)]
            else:
                self.user_power = -1
                return ["Your choice is not a valid triple", -1]
        
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
                self.user_power = -1
                return ["Your choice is not a valid 5 cards combination", -1]

        else:       # invalid number of cards
            self.user_power = -1
            return ["Invalid number of cards chosen", -1]

        # check if it is a valid combination
        if self.combination == len(cards) or self.combination == 0:

            # if valid choice
            if self.user_power > self.current_power:

                self.combination = len(cards)
                self.current_cards = cards.copy()
                self.current_power = self.user_power

                # remove the played cards from the handclient
                for card_number in userchoice:
                    del self.__players[self.current_player].hand[card_number]

                # finish the turn
                self.passes = 0
                return [f"Played cards: {' '.join(cards)}", 0]

            # weaker combination
            else:
                return ["Your card is not good enough to beat it, try again", -1]
        
        # invalid combination
        else:
            return [f"Invalid combination, current combination is {self.combination} cards", -1]
    
    def one_card_only(self):
        if len(self.__players[self.current_player].hand) == 1:
            return [f"{self.__players[self.current_player].name} has only 1 more card!", 0]
        return ["NO", -1]
    
    def game_finished(self):
        if not self.__players[self.current_player].hand:
            winner = self.__players[self.current_player].name
            loser = 0
            for i in range(1, len(self.__players)):
                if len(self.__players[i].hand) > len(self.__players[loser].hand):
                    loser = i
                elif len(self.__players[i].hand) == len(self.__players[loser].hand) and max(self.__players[i].hand, key=self.takepower) > max(self.__players[loser].hand, key=self.takepower):
                    loser = i

            loser = self.__players[loser].name

            return [f"{winner} just won :)", f"{loser} just lost :(", 0]

        return ["noone", "noone", -1]

class Game_Room(commands.Cog):
    def __init__(self, client, room_name, time_create):
        self.client = client
        self.__room_name = room_name
        self.__time_create = time_create

    @commands.command()
    async def create_game_room(self, ctx, room_name="magic"):
        game_room = Game_Room([ctx.message.author.id], room_name, datetime.datetime.now().replace(microsecond=0))

        self.__members = [f"@{ctx.author.name}#{ctx.author.discriminator}"]

        create_game_room_embed=discord.Embed(title=f"{game_room.get_room_name()} game room", color=0x3584e4)
        create_game_room_embed.add_field(name="Player amount", value="1")
        create_game_room_embed.add_field(name="Created time", value=game_room.get_time_create(), inline=False)
        create_game_room_embed.add_field(name="Player joined", value=f"@{ctx.author.name}#{ctx.author.discriminator}", inline=False)
        # sqliteConnection = sqlite3.connect("game.db")
        # cursor = sqliteConnection.cursor()
        
        await ctx.send(embed=create_game_room_embed)
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
        self.__members.append(f"@{ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(f"<@{ctx.author.id}> You joined the game successfully")

        file=open("game_file", "r")
        content=file.readlines()
        player_amount=len(content)
        user_name_list=[]
        for i in content:
            if(i[-1] == '\n'):
                i = i[:-1]

            user = await self.client.fetch_user(int(i))
            self.__members.append(f"{user.name}#{user.distdiscriminator}")

        join_game_embed=discord.Embed(title=f"Game room", color=0x3584e4)
        join_game_embed.add_field(name="Player amount", value=player_amount, inline=False)
        join_game_embed.add_field(name="Player joined", value=f"{user_name_list}", inline=False)    # what is this: 'value = f"{var}"'? why not 'value = str(var)'?
        await ctx.send(embed=join_game_embed)

    @commands.command()
    async def leave_room(self, ctx):
        if not (data_exists("game_file", ctx.author.id)):
            await ctx.send(f"<@{ctx.author.id}> You did not join the game")
            return

        remove_content("game_file", ctx.author.id)
        self.__members.remove(f"@{ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(f"<@{ctx.author.id}> You have left the game successfully")
        await ctx.send("Game finished because of the leaver! Liver lost, others won!")
        self.game = None


    def get_room_name(self):
        return self.__room_name

    def get_time_create(self):
        return self.__time_create

    @commands.command()
    async def start_game(self, ctx):
        self.game = Game(self.__members)

        await ctx.send("Game started")

        for i in self.game.show_deck():
            await ctx.send(i)

    @commands.command()
    async def play(self, ctx, *cards):
        output = self.game.turn(' '.join(cards))
        await ctx.send(output[0])

        if output[1] == 0:
            one_card = self.game.one_card_only()
            
            if one_card[1] == 0:
                await ctx.send(one_card[0])
            
            else:
                game_fin = self.game.game_finished()

                if game_fin[2] == 0:
                    await ctx.send("Game finished!")
                    await ctx.send(game_fin[0])
                    await ctx.send(game_fin[1])
                    self.game = None
            
            if self.game is not None:
                for i in self.game.show_deck():
                    await ctx.send(i)

        else:
            await ctx.send(output[0])
            await ctx.send(f"Last played cards: {' '.join(self.game.current_cards)}")


async def setup(client):
    await client.add_cog(Game_Room(client, 0, 0))