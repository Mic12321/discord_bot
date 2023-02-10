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
        self.id = int(name[2:-1])

class Game:   
    def __init__(self, players):
        self.powers = { "3:diamonds:" : 1, " 3:skull_crossbones:" : 2,  "3:hearts:" : 3,  "3:heart_on_fire:" : 4,
                        "4:diamonds:" : 5,  "4:skull_crossbones:" : 6,  "4:hearts:" : 7,  "4:heart_on_fire:" : 8,
                        "5:diamonds:" : 9,  "5:skull_crossbones:" : 10, "5:hearts:" : 11, "5:heart_on_fire:" : 12,
                        "6:diamonds:" : 13, "6:skull_crossbones:" : 14, "6:hearts:" : 15, "6:heart_on_fire:" : 16,
                        "7:diamonds:" : 17, "7:skull_crossbones:" : 18, "7:hearts:" : 19, "7:heart_on_fire:" : 20,
                        "8:diamonds:" : 21, "8:skull_crossbones:" : 22, "8:hearts:" : 23, "8:heart_on_fire:" : 24,
                        "9:diamonds:" : 25, "9:skull_crossbones:" : 26, "9:hearts:" : 27, "9:heart_on_fire:" : 28,
                        "T:diamonds:" : 29, "T:skull_crossbones:" : 30, "T:hearts:" : 31, "T:heart_on_fire:" : 32,
                        "J:diamonds:" : 33, "J:skull_crossbones:" : 34, "J:hearts:" : 35, "J:heart_on_fire:" : 36,
                        "Q:diamonds:" : 37, "Q:skull_crossbones:" : 38, "Q:hearts:" : 39, "Q:heart_on_fire:" : 40,
                        "K:diamonds:" : 41, "K:skull_crossbones:" : 42, "K:hearts:" : 43, "K:heart_on_fire:" : 44,
                        "A:diamonds:" : 45, "A:skull_crossbones:" : 46, "A:hearts:" : 47, "A:heart_on_fire:" : 48,
                        "2:diamonds:" : 49, "2:skull_crossbones:" : 50, "2:hearts:" : 51, "2:heart_on_fire:" : 52  }

        self.deck = list(self.powers.keys())

        # shuffle the deck
        for i in range(random.randint(10, 100)):
            random.shuffle(self.deck)

        # players - save the array of Player objects, it has .name - name and .hand - array of cards
        self.__players = [Player(f"{players[i]}", sorted([self.deck[j] for j in range(len(self.deck)) if j%4 == i], key = self.takepower)) for i in range(len(players))]

        # use random order for turns
        random.shuffle(self.__players)

        # choose the current player accouring to "smallest card" rule :)
        self.starting_player = [self.__players[i].hand[0] for i in range(len(self.__players))].index(min([self.__players[i].hand[0] for i in range(len(self.__players))], key=self.takepower))

        if self.starting_player != 0:
            self.__players[0], self.__players[self.starting_player] = self.__players[self.starting_player], self.__players[0]

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
        if cards[0][1:] == cards[1][1:] == cards[2][1:] == cards[3][1:] == cards[4][1:]:
            return self.powers[cards[4]]

        else:
            return 0

    # check if cards is a full house
    def full_house(self, cards):
        if cards[0][0] == cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0]:    # 3 3 3 4 4 and other
            return self.powers[cards[2]]

        elif cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]:  # 3 3 4 4 4 and other
            return self.powers[cards[4]]

        else:
            return 0

    # check if cards is a four of a kind
    def four_of_a_kind(self, cards):
        if cards[0][0] == cards[1][0] == cards[2][0] == cards[3][0]:        # 3 3 3 3 4 and other
            return self.powers[cards[3]]

        elif cards[1][0] == cards[2][0] == cards[3][0] == cards[4][0]:     # 3 4 4 4 4 and other
            return self.powers[cards[4]]

        else:
            return 0

    # check if cards is a straight flush
    def straight_flush(self, cards):
        if self.straight(cards) != 0 and self.flush(cards) != 0:
            return self.powers[cards[4]]

        else:
            return 0

    def show_all_userids(self):
        return [player.id for player in self.__players]

    def show_current_user(self):
        return self.__players[self.current_player]

    def show_all_decks(self):
        return [self.show_deck(player) for player in self.__players]

    def show_deck(self, player):
        user_hand = player.hand
        hand = ' '.join(user_hand)
        options = " .. " + ' . . '.join([str(i+1) + ' .' * ((i % 4) != 2) * (i != (len(user_hand) - 1)) for i in range(len(user_hand))])

        return [player.id, hand, options]

    def turn(self, cards):
        userinput = cards.split()
        userchoice = sorted([int(i) - 1 for i in userinput if i.isdigit()])

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
                    return [f"{self.__players[self.current_player].name} Pass... Current cards: {' '.join(self.current_cards)}", 0]
        
        # check if all choices are valid
        for card_number in userchoice:

            # invalid turn
            if card_number >= len(self.__players[self.current_player].hand) or card_number < 0:
                return ["Invalid choice", -1]
        
        # cards that user want to play
        cards = [self.__players[self.current_player].hand[card_number] for card_number in userchoice]

        if len(cards) == 1:     # 1 card 
            self.user_power = self.powers[cards[0]]
        
        elif len(cards) == 2:   # 2 cards (pair)
            if cards[0][0] == cards[1][0]:
                self.user_power = self.powers[cards[1]]
            else:
                self.user_power = -1
                return ["Your choice is not a valid pair", -1]

        elif len(cards) == 3:   # 3 cards (triple)
            if cards[0][0] == cards[1][0] == cards[2][0]:
                self.user_power = self.powers[cards[2]]
            else:
                self.user_power = -1
                return ["Your choice is not a valid triple", -1]
        
        elif len(cards) == 5:   # 5 cards combinations     
            self.user_power = self.straight_flush(cards) + 400  # straight flush

            if self.user_power == 400:      # four of a kind
                self.user_power = self.four_of_a_kind(cards) + 300

            elif self.user_power == 300:    # full house
                self.user_power = self.full_house(cards) + 200

            elif self.user_power == 200:    # flush
                self.user_power = self.flush(cards) + 100

            elif self.user_power == 100:    # straight
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

                # remove the played cards from the hand
                for card_number in sorted(userchoice, reverse = True):
                    del self.__players[self.current_player].hand[card_number]

                # finish the turn
                self.passes = 0
                return [f"{self.__players[self.current_player].name} Played: {' '.join(cards)}", 0]

            # weaker combination
            else:
                return ["Your card is not good enough to beat it, try again", -1]
        
        # invalid combination
        else:
            return [f"Invalid combination, current combination is {self.combination} cards", -1]
    
    def next_turn(self):
        self.current_player = (self.current_player + 1) % len(self.__players)

    def one_card_only(self):
        if len(self.__players[self.current_player].hand) == 1:
            return [f"{self.__players[self.current_player].name} has only 1 more card!", 0]
        return ["all good", -1]
    
    def game_finished(self):
        if not self.__players[self.current_player].hand:
            winner = self.__players[self.current_player].name
            loser = 0
            for i in range(1, len(self.__players)):
                if len(self.__players[i].hand) > len(self.__players[loser].hand):
                    loser = i
                elif len(self.__players[i].hand) == len(self.__players[loser].hand) and self.powers[self.__players[i].hand[-1]] > self.powers[self.__players[loser].hand[-1]]:
                    loser = i

            loser = self.__players[loser].name

            return [winner, loser, 0]

        return ["all good", "all good", -1]

class Game_Room(commands.Cog):
    def __init__(self, client, room_name, time_create):
        self.client = client
        self.__room_name = room_name
        self.__time_create = time_create
        self.__game = None
        self.__members = []

    @commands.command()
    async def create_game_room(self, ctx, room_name="Magic"):
        game_room = Game_Room([ctx.message.author.id], room_name, datetime.datetime.now().replace(microsecond=0))

        self.__members.append(f"<@{ctx.author.id}>")

        create_game_room_embed=discord.Embed(title=f"{game_room.get_room_name()} Game-room", color=0x3584e4)
        create_game_room_embed.add_field(name="Player amount", value=len(self.__members))
        create_game_room_embed.add_field(name="Created time", value=game_room.get_time_create(), inline=False)
        create_game_room_embed.add_field(name="Players", value=f"{' '.join(self.__members)}", inline=False)
        # sqliteConnection = sqlite3.connect("game.db")
        # cursor = sqliteConnection.cursor()
        
        await ctx.send(embed=create_game_room_embed)
        write_content("game_file", str(ctx.author.id))


    @commands.command()
    async def join_room(self, ctx, room_name="Magic"):
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
        self.__members.append(f"<@{ctx.author.id}>")
        await ctx.send(f"<@{ctx.author.id}> You joined the game successfully")

        join_game_embed=discord.Embed(title=f"Game room", color=0x3584e4)
        join_game_embed.add_field(name="Player amount", value=len(self.__members), inline=False)
        join_game_embed.add_field(name="Players", value=f"{' '.join(self.__members)}", inline=False)    # what is this: 'value = f"{var}"'? why not 'value = str(var)'?
        await ctx.send(embed=join_game_embed)

    @commands.command()
    async def leave_room(self, ctx):
        if not (data_exists("game_file", ctx.author.id)):
            await ctx.send(f"<@{ctx.author.id}> You did not join the game")
            return

        remove_content("game_file", ctx.author.id)
        self.__members.remove(f"<@{ctx.author.id}>")
        await ctx.send(f"<@{ctx.author.id}> You have left the game successfully")
        await ctx.send(f"Game finished because of the leaver! <@{ctx.author.id}> is loser, {' '.join(self.__members)} are winners!")
        self.__game = None


    def get_room_name(self):
        return self.__room_name

    def get_time_create(self):
        return self.__time_create

    @commands.command()
    async def start_game(self, ctx):
        if 1 < len(self.__members) < 5:

            self.__game = Game(self.__members)

            await ctx.send("Game started")

            magicarr = self.__game.show_all_decks()

            for magic in magicarr:
                user = await self.client.fetch_user(magic[0])
                user_hand_embed = discord.Embed(title="Your Deck", color=0xffffff)
                user_hand_embed.add_field(name=magic[1], value=magic[2], inline=False)
                await user.send(embed=user_hand_embed)
                await user.send(f"{self.__game.show_current_user().name} Start this game")
        
        else:
            await ctx.send("Invalid number of players :(")

    @commands.command()
    async def play(self, ctx, *cards):

        # game is not started
        if self.__game is None:
            await ctx.send("Game... IS NOT STARTED!!!")
            return  
    
        # invalid player try to play (not his/her turn)
        if ctx.author.id != self.__game.show_current_user().id:
            await ctx.send(f"It is NOT your turn now! Please ask {self.__game.show_current_user().name} to hurry up!")
            return  

        output = self.__game.turn(' '.join(cards))
        # invalid turn
        if output[1] != 0: 
            await ctx.send(output[0])
            last_played_card_embed = discord.Embed(title=f"Last cards played: {' '.join(self.__game.current_cards)}", color=0xffffff)
            await ctx.send(embed = last_played_card_embed)
            return  

        for userid in self.__game.show_all_userids():
            user = await self.client.fetch_user(userid)
            await user.send(output[0])

        one_card = self.__game.one_card_only()

        if one_card[1] == 0:
            for userid in self.__game.show_all_userids():
                user = await self.client.fetch_user(userid)
                await user.send(one_card[1][0])
        
        else:
            game_fin = self.__game.game_finished()

            if game_fin[2] == 0:
                game_fin_embed = discord.Embed(title="Game finished!", color=0xffffff)
                game_fin_embed.add_field(name="Winner", value=game_fin[0], inline=False)
                game_fin_embed.add_field(name="Loser", value=game_fin[1], inline=False)

                for userid in self.__game.show_all_userids():
                    user = await self.client.fetch_user(userid)
                    await user.send(embed = game_fin_embed)

                self.__game = None

        # game is not finished yet
        if self.__game is not None:
            magic = self.__game.show_deck(self.__game.show_current_user())
            user = await self.client.fetch_user(magic[0])
            user_hand_embed = discord.Embed(title="Your Deck", color=0xffffff)
            user_hand_embed.add_field(name=magic[1], value=magic[2], inline=False)
            await user.send(embed = user_hand_embed)
            self.__game.next_turn()

async def setup(client):
    await client.add_cog(Game_Room(client, 0, 0))