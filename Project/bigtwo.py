import random

powers = {  "3D" : 1,  "3C" : 2,  "3H" : 3,  "3S" : 4,
            "4D" : 5,  "4C" : 6,  "4H" : 7,  "4S" : 8,
            "5D" : 9,  "5C" : 10, "5H" : 11, "5S" : 12,
            "6D" : 13, "6C" : 14, "6H" : 15, "6S" : 16,
            "7D" : 17, "7C" : 18, "7H" : 19, "7S" : 20,
            "8D" : 21, "8C" : 22, "8H" : 23, "8S" : 24,
            "9D" : 25, "9C" : 26, "9H" : 27, "9S" : 28,
            "TD" : 29, "TC" : 30, "TH" : 31, "TS" : 32,
            "JD" : 33, "JC" : 34, "JH" : 35, "JS" : 36,
            "QD" : 37, "QC" : 38, "QH" : 39, "QS" : 40,
            "KD" : 41, "KC" : 42, "KH" : 43, "KS" : 44,
            "AD" : 45, "AC" : 46, "AH" : 47, "AS" : 48,
            "2D" : 49, "2C" : 50, "2H" : 51, "2S" : 52  }

# create the deck
deck = list(powers.keys())

# shuffle the deck
for i in range(random.randint(10, 100)):
    random.shuffle(deck)

# input number of players and check if it is valid (if not -> program will be ended here)
players_number = int(input("How many players: "))
if players_number < 2 or players_number > 4:
    print("Invalid number of players, it is not allowed")
    exit()

# input usernames and create card hand for each user
names = []
players_cards = []
for i in range(players_number):
    name = input("Input name of next player: ")
    names.append(name)
    players_cards.append([deck[j] for j in range(len(deck)) if j%4 == i])

passes = 0
current_player = 0
current_power = 0
current_cards = []
user_power = 0

combination = 0

# game
while True:
    
    # player turn
    while True:

        # show player's deck
        print("\nYour deck: ")
        print(' '.join(players_cards[current_player]))

        for i in range(len(players_cards[current_player])):
            print(i + 1, ' ' * (1-(i+1)//10), end = '')

        userinput = input("\n\nUse number below cards to play (or 0 - to pass): ").split()
        
        userchoice = [int(i) - 1 for i in userinput if i.isdigit()]
        userchoice.sort(reverse = True)

        if len(userchoice) == len(userinput):

            # pass option
            if userchoice[0] < 0:
                
                # invalid pass
                if combination == 0:
                    print("You should not pass at the start of the circle")
                    continue
                
                # valid pass
                else:
                    print("\nPass")
                    passes += 1

                    # if all people pass (new circle start)
                    if passes == players_number - 1:
                        print("All people pass")
                        combination = 0
                        current_power = 0
                        passes = 0

                    else:
                        print("Current cards:", ' '.join(current_cards))

                    break
            
            # check if all choices are valid
            for card_number in userchoice:

                # invalid turn
                if card_number >= len(players_cards[current_player]):
                    print("Invalid card choice")
                    break

            # if turn is valid
            else:

                # cards that user want to play
                cards = []
                for card_number in userchoice:
                    cards.append(players_cards[current_player][card_number])

                if len(cards) == 1:
                    user_power = powers[cards[0]]
                
                elif len(cards) == 2:
                    if cards[0][0] == cards[1][0]:
                        user_power = max(powers[cards[0]], powers[cards[1]])
                    else:
                        print("Your choice is not a valid pair")
                        user_power = -1

                elif len(cards) == 3:
                    if cards[0][0] == cards[1][0] == cards[2][0]:
                        user_power = max(powers[cards[0]], powers[cards[1]], powers[cards[2]])
                    else:
                        print("Your choice is not a valid triple")
                        user_power = -1

                else:
                    print("Invalid number of cards chosen")
                    user_power = -1

                # invalid choice -- try another attempt
                if user_power == -1:
                    continue

                # no combination (start of the circle)
                if combination == 0:
                    print("\nPlayed cards:", ' '.join(cards))

                    combination = len(cards)
                    current_cards = cards
                    current_power = user_power

                    # remove the played cards from the hand
                    for card_number in userchoice:
                        del players_cards[current_player][card_number]

                    # finish the turn
                    passes = 0
                    break
                
                # check if it is a valid combination
                elif combination == len(cards):

                    # if valid choice
                    if user_power > current_power:
                        print("\nPlayed cards:", ' '.join(cards))

                        current_cards = cards
                        current_power = user_power

                        # remove the played cards from the hand
                        for card_number in userchoice:
                            del players_cards[current_player][card_number]

                        # finish the turn
                        passes = 0
                        break

                    # weaker combination
                    else:
                        print("Your card is not good enough to beat it, try again")
                
                # invalid combination
                else:
                    print("Invalid combination, current combination is", combination, "cards")
        else:
            print("Invalid card choice, try again")

    # check if the person won the game
    if not players_cards[current_player]:

        # define a winner
        winner = current_player

        # find a loser
        loser = 0
        for i in range(1, players_number):
            if len(players_cards[i]) > len(players_cards[loser]):
                loser = i
        break

    # next player turn
    current_player = (current_player + 1) % players_number

# result messages
print("\n\nResults!!!\n")
print(names[winner], "is winner!!")
print(names[loser], "just lost!")