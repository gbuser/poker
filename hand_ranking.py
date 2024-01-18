import pickle

ranks = '23456789TJQKA'
rank_orders = {}
hand_type_order = {}
hand_ranks = {}
list_of_all_hands = []

# pickled data is a dict with hand_type as keys, values are a list of all hands of this type
# each hand has been internally sorted so that card order is not relevant
file = "hands.pickle"
data = open(file, 'rb')
data = pickle.load(data)

def get_straight_high(hand):
    # takes a hand which is a straight and returns the rank order of the high card
    # cards have already been sorted by rank
    if hand[0][0] == 'A' and hand[1][0] == '5':  # special case of A2345 here high card is 5
        return rank_orders['5']
    else:
        return rank_orders[hand[0][0]]

def get_n(hand):
    pairs = set()
    singles = []
    ranks = [card[0] for card in hand]
    ranks = sorted(ranks, key= lambda x: ranks.count(x), reverse = True)
    return rank_orders[ranks[0]]

def get_pairs(hand):
    ranks = [rank_orders[card[0]] for card in hand]
    ranks = sorted(ranks, key = lambda x: (ranks.count(x), -1 * x), reverse = True)
    if len(set(ranks)) == 3:  # two pairs
        return ([ranks[0], ranks[2]], [ranks[4]])
    if len(set(ranks)) == 4:  # one pair
        return ([ranks[0]], ranks[2:])


hand_types = list(data.keys())[:-1]  # data includes an 'all' key which is all hands, not wanted here
for index, rank in enumerate(ranks[-1::-1]):  # set rank orders: A = 0, K = 1...
    rank_orders[rank] = index
for index, hand_type in enumerate(data.keys()):  # set hand_type order: straight flush = 0, four kind = 1...
    hand_type_order[hand_type] = index
for key in data:  # sanity check:  print number of hands of each type
    print(f'{key}: {len(data[key])}')
hand_sort_dict = {"straight flush": get_straight_high,  # not yet implemented
                  "four kind": get_n,
                  "full house": get_n,
                  "flush": 'tbd',
                  "straight": get_straight_high,
                  "three kind": get_n,
                  "two pair": get_pairs,
                  "pair": get_pairs,
                  "single": 'tbd'}

# STRAIGHT FLUSHES:
straight_flush_list = [(hand, {'tier0': 0, 'tier1': get_straight_high(hand)}) for hand in data["straight flush"]]
sorted_sf = sorted(straight_flush_list, key=lambda x: (x[1]['tier0'], x[1]['tier1']))
place = 0
for item in sorted_sf:
    if item[1]['tier1'] > place:
        place += 1
    item[1]['place'] = place
list_of_all_hands += sorted_sf
print(f"Straight flush:\n{sorted_sf[0]}")
print(list_of_all_hands[-1])

# FOUR OF A KIND:
four_list = [(hand, {'tier0': 1, 'tier1': get_n(hand)}) for hand in data["four kind"]]
sorted_four = sorted(four_list, key=lambda x: (x[1]['tier0'], x[1]['tier1']))

place = 10
current = sorted_four[0][1]['tier1']
for item in sorted_four:
    if item[1]['tier1'] != current:
        place += 1
        current = item[1]['tier1']
    item[1]['place'] = place
list_of_all_hands += sorted_four
print(f"Four of a kind:\n{sorted_four[0]}")
print(list_of_all_hands[-1])

# FULL HOUSE:
full_list = [(hand, {'tier0':2, 'tier1':get_n(hand)}) for hand in data["full house"]]
sorted_full = sorted(full_list, key = lambda x: (x[1]['tier0'], x[1]['tier1']))
place = 23
current = sorted_full[0][1]['tier1']
for item in sorted_full:
    if item[1]['tier1'] != current:
        place += 1
        current = item[1]['tier1']
    item[1]['place'] = place
list_of_all_hands += sorted_full
print(f"Full house:\n{sorted_full[0]}")
print(list_of_all_hands[-1])

# FLUSH:
flush_list = [(hand, {'tier0': 3, 'tier1': list(map(lambda x: rank_orders[x[0]], hand))}) for hand in data["flush"]]
sorted_flush = sorted(flush_list, key = lambda x: (x[1]['tier0'], x[1]['tier1']))
place = 36
current = sorted_flush[0][1]['tier1']
for item in sorted_flush:
    if item[1]['tier1'] != current:
        place += 1
        current = item[1]['tier1']
    item[1]['place'] = place
list_of_all_hands += sorted_flush
print(f"Flush:\n{sorted_flush[0]}")
print(list_of_all_hands[-1])


# STRAIGHT:
straight_list = [(hand, {'tier0': 4, 'tier1': get_straight_high(hand)}) for hand in data["straight"]]
sorted_straight = sorted(straight_list, key = lambda x: (x[1]['tier0'], x[1]['tier1']))
place = 1313
current = sorted_straight[0][1]['tier1']
for item in sorted_straight:
    if item[1]['tier1'] > current:
        place += 1
        current = item[1]['tier1']
    item[1]['place'] = place
list_of_all_hands += sorted_straight
print(f"Straight:\n{sorted_straight[0]}")
print(list_of_all_hands[-1])

# THREE OF A KIND:
three_list = [(hand, {'tier0': 5, 'tier1': get_n(hand)}) for hand in data["three kind"]]
sorted_three = sorted(three_list, key = lambda x: (x[1]['tier0'], x[1]['tier1']))
place = 1323
current = sorted_three[0][1]['tier1']
for item in sorted_three:
    if item[1]['tier1'] > current:
        place += 1
        current = item[1]['tier1']
    item[1]['place'] = place
list_of_all_hands += sorted_three
print(f"Three of a kind:\n{sorted_three[0]}")
print(list_of_all_hands[-1])

# TWO PAIR:
two_pair_list = [(hand, {'tier0': 6, 'tier1': get_pairs(hand)}) for hand in data["two pair"]]
sorted_two_pair = sorted(two_pair_list, key = lambda x: (x[1]['tier0'], x[1]['tier1']))
place = 1336
current = sorted_two_pair[0][1]['tier1']
for item in sorted_two_pair:
    if item[1]['tier1'] > current:
        place += 1
        current = item[1]['tier1']
    item[1]['place'] = place
list_of_all_hands += sorted_two_pair
print(f"Two pairs:\n{sorted_two_pair[0]}")
print(list_of_all_hands[-1])

# PAIR:
pair_list = [(hand, {'tier0': 7, 'tier1': get_pairs(hand)}) for hand in data["pair"]]
sorted_pair = sorted(pair_list, key = lambda x: (x[1]['tier0'], x[1]['tier1']))
place = 2194
current = sorted_pair[0][1]['tier1']
for item in sorted_pair:
    if item[1]['tier1'] != current:
        place += 1
        current = item[1]['tier1']
    item[1]['place'] = place
list_of_all_hands += sorted_pair
print(f"Pair:\n{sorted_pair[0]}")
print(list_of_all_hands[-1])

# SINGLE:
single_list = [(hand, {'tier0': 8, 'tier1': list(map(lambda x: rank_orders[x[0]], hand))}) for hand in data["single"]]
sorted_single = sorted(single_list, key = lambda x: (x[1]['tier0'], x[1]['tier1']))
place = 5054
current = sorted_single[0][1]['tier1']
for item in sorted_single:
    if item[1]['tier1'] != current:
        place += 1
        current = item[1]['tier1']
    item[1]['place'] = place
list_of_all_hands += sorted_single
print(f"High card:\n{sorted_single[0]}")
print(list_of_all_hands[-1])

with open('all_hands_ranked.pickle' , 'wb') as file:  # store dict as file
    pickle.dump(list_of_all_hands, file)