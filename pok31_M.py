import numpy as np
import time

n_players = 4
current_player = 1

ACTION_DRAW = 0
ACTION_PICK = 1
ACTION_KNOCK = 2

# shuffle cards
cards = []
sorted_card = []
suits = ["spade", "heart", "diamond", "club"]
#suits = ['♠', '♦', '♥', '♣']
numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
for number in numbers:
    for suit in suits:
        cards.append((suit, number))
sorted_card = cards.copy()
np.random.shuffle(cards)

# distribute cards
card_on_hands = []
for i in range(n_players):
    card_on_hand = []
    card_on_hand.append(cards.pop(0))
    card_on_hand.append(cards.pop(0))
    card_on_hand.append(cards.pop(0))
    card_on_hands.append(card_on_hand)

# assign trash
trash = []
trash.append(cards.pop(0))

def card_value(card_number):
    if card_number == "A":
        return 11
    elif card_number in ["J", "Q", "K"]:
        return 10
    return int(card_number)

def cal_score(card_on_hand):
    if card_on_hand[0][1] == card_on_hand[1][1] == card_on_hand[2][1]:
        return 30.5
    scores = {k: 0 for k in suits}
    for suit in suits:
        scores[suit] = sum([card_value(x[1]) for x in card_on_hand if x[0] == suit])
    return max(scores.values())

def cal_four_card(hand,temp):
    sco = []
    for i in range(4) :
        hand.append(temp)
        temp = hand.pop(0)
        sco.append(cal_score(hand))
    return sco

def choose_action(player_index, allow_knock):
    
    unshown_cards = cards
    for i in range(n_players):
        if i != player_index:
            unshown_cards = unshown_cards + card_on_hands[i]  # can not use +=
    
    card_trash = trash[len(trash)-1]
    hand = card_on_hands[player_index]

    h0 = 31 - cal_score(hand)

    temp = card_trash
    h1 = 31 - max(cal_four_card(hand,temp))
    
    temp_h2 = 0 
    for x in unshown_cards :
        temp_h2 = temp_h2 + (31 - max(cal_four_card(hand,x)))
    h2 = temp_h2/len(unshown_cards)

    if (round < 9):
        h_criteria = 31 - (24+round*0.5)
    else:
        h_criteria = 31 - 28
    if allow_knock:
        if (h0 < h_criteria) or (h0 <= h1 and h0 <= h2):
            action = ACTION_KNOCK
        elif(h1 < h2):
            action = ACTION_PICK
        else:
            action = ACTION_DRAW 
    else:
        if(h1 < h2):
            action = ACTION_PICK
        else:
            action = ACTION_DRAW 
    return action

def mySort(e):
    return numbers.index(e[1])

def discard_card(player_index,temp):
    card_on_hands[player_index].append(temp)
    card_on_hands[player_index].sort(key=mySort)
    temp = card_on_hands[player_index].pop(3)
    sco_all = cal_four_card(card_on_hands[player_index],temp)
    card_on_hands[player_index].append(temp)
    chosen_card_index = np.argmax(sco_all)
    trash.append(card_on_hands[player_index].pop(chosen_card_index))

print("\n----------------------------- GAME START -----------------------------")
round = 0
final_round = 100000
while round <= final_round and cards:
    
    player_index = current_player-1
    allow_knock = (final_round == 100000)
    
    print("\nRound",round+1,": player {} ".format(current_player))
    print("   Card on hand : ",end="")
    for i in card_on_hands[player_index]:
        print("<",i[0],i[1],">  ",end="")
    print("\n   Trash : <",trash[len(trash)-1][0],trash[len(trash)-1][1],">")
    print("   The number of cards remaining in the deck : ",len(cards))
    print("   Action : ",end="")
    action = choose_action(player_index, allow_knock)
    
    if action == ACTION_DRAW:
        temp = cards.pop(0)
        discard_card(player_index,temp)
        print("Draw card from deck <",temp[0],temp[1],">")
    elif action == ACTION_PICK:
        temp = trash.pop()
        discard_card(player_index,temp)
        print("Pick card from trash <",temp[0],temp[1],">")
    elif action == ACTION_KNOCK:
        final_round = round + (n_players - 1)
        print("Knock!!!")

    print("   Discarded card : <",trash[len(trash)-1][0],trash[len(trash)-1][1],">")
    print("   Card on hand : ",end="")
    for i in card_on_hands[player_index]:
        print("<",i[0],i[1],">  ",end="")
    print("")
    current_player = (current_player % n_players) + 1
    round += 1
    #time.sleep(0.5)
    
scores = [cal_score(x) for x in card_on_hands]
max_score_player_name = np.argmax(scores) + 1


print("\n------------------------------ GAME END ------------------------------\n")
for i in range(4):
    print("   Player",i+1,": score",scores[i],": ",end="")
    for j in card_on_hands[i]:
        print("<",j[0],j[1],"> ",end="")
    print(" ")
print("\n                *** Winner : Player",max_score_player_name,end="")
for i in range(max_score_player_name,4) :
    if scores[max_score_player_name-1] == scores[i] :
        print(" , Player",i+1,end="")
print(" ***")
print("----------------------------------------------------------------------")
