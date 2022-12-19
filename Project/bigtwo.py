# Author: DarkLack0

import random

# use this function to sort by power
def takepower(elem):
    return powers[elem]

# check if cards is a straight
def straight(cards):
    cards.sort(key = takepower)
    card_powers = [(powers[cards[0]] - 1) // 4, (powers[cards[1]] - 1) // 4, (powers[cards[2]] - 1) // 4, (powers[cards[3]] - 1) // 4, (powers[cards[4]] - 1) // 4]
    
    if card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2:  # normal straight
        return powers[cards[4]]

    elif card_powers[0] + 10 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2: # Q K A 2 3
        return powers[cards[4]]

    elif card_powers[0] + 10 == card_powers[1] + 9 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2: # K A 2 3 4
        return powers[cards[4]]

    elif card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 9 == card_powers[4] - 10: # A 2 3 4 5
        return powers[cards[4]]

    elif card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 10: # 2 3 4 5 6
        return powers[cards[4]]

    # not a straight
    else:
        return 0

# check if cards is a flush
def flush(cards):
    
    if cards[0][1] == cards[1][1] == cards[2][1] == cards[3][1] == cards[4][1]:
        return powers[max(cards, key=takepower)]

    else:
        return 0

# check if cards is a full house
def full_house(cards):
    cards.sort(key = takepower)

    if cards[0][0] == cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0]:    # 3 3 3 4 4 and other
        return powers[cards[2]]

    elif cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]:  # 3 3 4 4 4 and other
        return powers[cards[4]]

    else:
        return 0

# check if cards is a four of a kind
def four_of_a_kind(cards):
    cards.sort(key = takepower)

    if cards[0][0] == cards[1][0] == cards[2][0] == cards[3][0]:        # 3 3 3 3 4 and other
        return powers[cards[3]]

    elif cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]:     # 3 4 4 4 4 and other
        return powers[cards[4]]

    else:
        return 0

# check if cards is a straight flush
def straight_flush(cards):

    if straight(cards) != 0 and flush(cards) != 0:
        return powers[max(cards, key=takepower)]

    else:
        return 0

powers = {  "3♦" : 1,  "3♣" : 2,  "3♥" : 3,  "3♠" : 4,
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
    name = input(F"Input name of player {i+1}: ")
    names.append(name)
    hand = [deck[j] for j in range(len(deck)) if j%4 == i]
    hand.sort(key = takepower)
    players_cards.append(hand)

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

        # show player and their deck
        print(F"\nPlayer: {names[current_player]}")
        print(' '.join(players_cards[current_player]))

        for i in range(len(players_cards[current_player])):
            print(i + 1, ' ' * (1-(i+1)//10), end = '')

        userinput = input("\n\nUse number below cards to play (or 0 - to pass): ").split()
        
        userchoice = [int(i) - 1 for i in userinput if i.isdigit()]
        userchoice.sort(reverse = True)

        if len(userchoice) == len(userinput):

            # empty string input (invalid)
            if not userchoice:
                print("Do not leave the space empty")
                continue

            # pass option
            elif userchoice[0] == -1:
                
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

                if len(cards) == 1:     # 1 card 
                    user_power = powers[cards[0]]
                
                elif len(cards) == 2:   # 2 cards (pair)
                    if cards[0][0] == cards[1][0]:
                        user_power = powers[max(cards, key=takepower)]
                    else:
                        print("Your choice is not a valid pair")
                        user_power = -1

                elif len(cards) == 3:   # 3 cards (triple)
                    if cards[0][0] == cards[1][0] == cards[2][0]:
                        user_power = powers[max(cards, key=takepower)]
                    else:
                        print("Your choice is not a valid triple")
                        user_power = -1
                
                elif len(cards) == 5:   # 5 cards combinations
                    
                    if straight_flush(cards) != 0:      # straight flush
                        user_power = straight_flush(cards) + 400

                    elif four_of_a_kind(cards) != 0:     # four of a kind
                        user_power = four_of_a_kind(cards) + 300

                    elif full_house(cards) != 0:         # full house
                        user_power = full_house(cards) + 200

                    elif flush(cards) != 0:              # flush
                        user_power = flush(cards) + 100

                    elif straight(cards) != 0:           # straight
                        user_power = straight(cards)

                    else:
                        print("Your choice is not a valid 5 cards combination")
                        user_power = -1

                else:       # invalid number of cards
                    print("Invalid number of cards ch# Author: DarkLack0

import random

# use this function to sort by power
def takepower(elem):
    return powers[elem]

# check if cards is a straight
def straight(cards):
    cards.sort(key = takepower)
    card_powers = [(powers[cards[0]] - 1) // 4, (powers[cards[1]] - 1) // 4, (powers[cards[2]] - 1) // 4, (powers[cards[3]] - 1) // 4, (powers[cards[4]] - 1) // 4]
    
    if card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2:  # normal straight
        return powers[cards[4]]

    elif card_powers[0] + 10 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2: # Q K A 2 3
        return powers[cards[4]]

    elif card_powers[0] + 10 == card_powers[1] + 9 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2: # K A 2 3 4
        return powers[cards[4]]

    elif card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 9 == card_powers[4] - 10: # A 2 3 4 5
        return powers[cards[4]]

    elif card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 10: # 2 3 4 5 6
        return powers[cards[4]]

    # not a straight
    else:
        return 0

# check if cards is a flush
def flush(cards):
    
    if cards[0][1] == cards[1][1] == cards[2][1] == cards[3][1] == cards[4][1]:
        return powers[max(cards, key=takepower)]

    else:
        return 0

# check if cards is a full house
def full_house(cards):
    cards.sort(key = takepower)

    if cards[0][0] == cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0]:    # 3 3 3 4 4 and other
        return powers[cards[2]]

    elif cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]:  # 3 3 4 4 4 and other
        return powers[cards[4]]

    else:
        return 0

# check if cards is a four of a kind
def four_of_a_kind(cards):
    cards.sort(key = takepower)

    if cards[0][0] == cards[1][0] == cards[2][0] == cards[3][0]:        # 3 3 3 3 4 and other
        return powers[cards[3]]

    elif cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]:     # 3 4 4 4 4 and other
        return powers[cards[4]]

    else:
        return 0

# check if cards is a straight flush
def straight_flush(cards):

    if straight(cards) != 0 and flush(cards) != 0:
        return powers[max(cards, key=takepower)]

    else:
        return 0

powers = {  "3♦" : 1,  "3♣" : 2,  "3♥" : 3,  "3♠" : 4,
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
    name = input(F"Input name of player {i+1}: ")
    names.append(name)
    hand = [deck[j] for j in range(len(deck)) if j%4 == i]
    hand.sort(key = takepower)
    players_cards.append(hand)

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

        # show player and their deck
        print(F"\nPlayer: {names[current_player]}")
        print(' '.join(players_cards[current_player]))

        for i in range(len(players_cards[current_player])):
            print(i + 1, ' ' * (1-(i+1)//10), end = '')

        userinput = input("\n\nUse number below cards to play (or 0 - to pass): ").split()
        
        userchoice = [int(i) - 1 for i in userinput if i.isdigit()]
        userchoice.sort(reverse = True)

        if len(userchoice) == len(userinput):

            # empty string input (invalid)
            if not userchoice:
                print("Do not leave the space empty")
                continue

            # pass option
            elif userchoice[0] == -1:
                
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

                if len(cards) == 1:     # 1 card 
                    user_power = powers[cards[0]]
                
                elif len(cards) == 2:   # 2 cards (pair)
                    if cards[0][0] == cards[1][0]:
                        user_power = powers[max(cards, key=takepower)]
                    else:
                        print("Your choice is not a valid pair")
                        user_power = -1

                elif len(cards) == 3:   # 3 cards (triple)
                    if cards[0][0] == cards[1][0] == cards[2][0]:
                        user_power = powers[max(cards, key=takepower)]
                    else:
                        print("Your choice is not a valid triple")
                        user_power = -1
                
                elif len(cards) == 5:   # 5 cards combinations
                    
                    if straight_flush(cards) != 0:      # straight flush
                        user_power = straight_flush(cards) + 400

                    elif four_of_a_kind(cards) != 0:     # four of a kind
                        user_power = four_of_a_kind(cards) + 300

                    elif full_house(cards) != 0:         # full house
                        user_power = full_house(cards) + 200

                    elif flush(cards) != 0:              # flush
                        user_power = flush(cards) + 100

                    elif straight(cards) != 0:           # straight
                        user_power = straight(cards)

                    else:
                        print("Your choice is not a valid 5 cards combination")
                        user_power = -1

                else:       # invalid number of cards
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

    # check if the person won the game# Author: DarkLack0

import random

# use this function to sort by power
def takepower(elem):
    return powers[elem]

# check if cards is a straight
def straight(cards):
    cards.sort(key = takepower)
    card_powers = [(powers[cards[0]] - 1) // 4, (powers[cards[1]] - 1) // 4, (powers[cards[2]] - 1) // 4, (powers[cards[3]] - 1) // 4, (powers[cards[4]] - 1) // 4]
    
    if card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2:  # normal straight
        return powers[cards[4]]

    elif card_powers[0] + 10 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2: # Q K A 2 3
        return powers[cards[4]]

    elif card_powers[0] + 10 == card_powers[1] + 9 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 2: # K A 2 3 4
        return powers[cards[4]]

    elif card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 9 == card_powers[4] - 10: # A 2 3 4 5
        return powers[cards[4]]

    elif card_powers[0] + 2 == card_powers[1] + 1 == card_powers[2] == card_powers[3] - 1 == card_powers[4] - 10: # 2 3 4 5 6
        return powers[cards[4]]

    # not a straight
    else:
        return 0

# check if cards is a flush
def flush(cards):
    
    if cards[0][1] == cards[1][1] == cards[2][1] == cards[3][1] == cards[4][1]:
        return powers[max(cards, key=takepower)]

    else:
        return 0

# check if cards is a full house
def full_house(cards):
    cards.sort(key = takepower)

    if cards[0][0] == cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0]:    # 3 3 3 4 4 and other
        return powers[cards[2]]

    elif cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]:  # 3 3 4 4 4 and other
        return powers[cards[4]]

    else:
        return 0

# check if cards is a four of a kind
def four_of_a_kind(cards):
    cards.sort(key = takepower)

    if cards[0][0] == cards[1][0] == cards[2][0] == cards[3][0]:        # 3 3 3 3 4 and other
        return powers[cards[3]]

    elif cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]:     # 3 4 4 4 4 and other
        return powers[cards[4]]

    else:
        return 0

# check if cards is a straight flush
def straight_flush(cards):

    if straight(cards) != 0 and flush(cards) != 0:
        return powers[max(cards, key=takepower)]

    else:
        return 0

powers = {  "3♦" : 1,  "3♣" : 2,  "3♥" : 3,  "3♠" : 4,
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
    name = input(F"Input name of player {i+1}: ")
    names.append(name)
    hand = [deck[j] for j in range(len(deck)) if j%4 == i]
    hand.sort(key = takepower)
    players_cards.append(hand)

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

        # show player and their deck
        print(F"\nPlayer: {names[current_player]}")
        print(' '.join(players_cards[current_player]))

        for i in range(len(players_cards[current_player])):
            print(i + 1, ' ' * (1-(i+1)//10), end = '')

        userinput = input("\n\nUse number below cards to play (or 0 - to pass): ").split()
        
        userchoice = [int(i) - 1 for i in userinput if i.isdigit()]
        userchoice.sort(reverse = True)

        if len(userchoice) == len(userinput):

            # empty string input (invalid)
            if not userchoice:
                print("Do not leave the space empty")
                continue

            # pass option
            elif userchoice[0] == -1:
                
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

                if len(cards) == 1:     # 1 card 
                    user_power = powers[cards[0]]
                
                elif len(cards) == 2:   # 2 cards (pair)
                    if cards[0][0] == cards[1][0]:
                        user_power = powers[max(cards, key=takepower)]
                    else:
                        print("Your choice is not a valid pair")
                        user_power = -1

                elif len(cards) == 3:   # 3 cards (triple)
                    if cards[0][0] == cards[1][0] == cards[2][0]:
                        user_power = powers[max(cards, key=takepower)]
                    else:
                        print("Your choice is not a valid triple")
                        user_power = -1
                
                elif len(cards) == 5:   # 5 cards combinations
                    
                    if straight_flush(cards) != 0:      # straight flush
                        user_power = straight_flush(cards) + 400

                    elif four_of_a_kind(cards) != 0:     # four of a kind
                        user_power = four_of_a_kind(cards) + 300

                    elif full_house(cards) != 0:         # full house
                        user_power = full_house(cards) + 200

                    elif flush(cards) != 0:              # flush
                        user_power = flush(cards) + 100

                    elif straight(cards) != 0:           # straight
                        user_power = straight(cards)

                    else:
                        print("Your choice is not a valid 5 cards combination")
                        user_power = -1

                else:       # invalid number of cards
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
            elif len(players_cards[i]) == len(players_cards[loser]) and max(players_cards[i], key=takepower) > max(players_cards[loser], key=takepower):
                loser = i
        break

    # next player turn
    current_player = (current_player + 1) % players_number

# result messages
print("\n\nResults!!!\n")
print(names[winner], "is winner!!")
print(names[loser], "just lost!")
    if not players_cards[current_player]:

        # define a winner
        winner = current_player

        # find a loser
        loser = 0
        for i in range(1, players_number):
            if len(players_cards[i]) > len(players_cards[loser]):
                loser = i
            elif len(players_cards[i]) == len(players_cards[loser]) and max(players_cards[i], key=takepower) > max(players_cards[loser], key=takepower):
                loser = i
        break

    # next player turn
    current_player = (current_player + 1) % players_number

# result messages
print("\n\nResults!!!\n")
print(names[winner], "is winner!!")
print(names[loser], "just lost!")osen")
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
            elif len(players_cards[i]) == len(players_cards[loser]) and max(players_cards[i], key=takepower) > max(players_cards[loser], key=takepower):
                loser = i
        break

    # next player turn
    current_player = (current_player + 1) % players_number

# result messages
print("\n\nResults!!!\n")
print(names[winner], "is winner!!")
print(names[loser], "just lost!")