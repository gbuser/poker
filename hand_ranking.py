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

def get_single(hand):
    return list(map(lambda x: rank_orders[x[0]], hand))

def make_tiers(hand_list, place, list_of_all_hands):
    sorted_list = sorted(hand_list, key=lambda x: (x[1]['tier0'], x[1]['tier1']))
    current = sorted_list[0][1]['tier1']
    ties = 0
    for item in sorted_list:
        ties += 1
        if item[1]['tier1'] != current:
            place += ties - 1
            ties = 1
            current = item[1]['tier1']
        item[1]['place'] = place
    place += 1
    list_of_all_hands += sorted_list
    print(f"{sorted_list[0]}")
    print(list_of_all_hands[-1])
    return place


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

place = 0

# STRAIGHT FLUSHES:
straight_flush_list = [(hand, {'tier0': 0, 'tier1': get_straight_high(hand)}) for hand in data["straight flush"]]
print("Straight flush:")
place = make_tiers(straight_flush_list, place, list_of_all_hands)

# FOUR OF A KIND:
four_list = [(hand, {'tier0': 1, 'tier1': get_n(hand)}) for hand in data["four kind"]]
print("Four of a kind:")
place = make_tiers(four_list, place, list_of_all_hands)

# FULL HOUSE:
full_list = [(hand, {'tier0':2, 'tier1':get_n(hand)}) for hand in data["full house"]]
print("Full house:")
place = make_tiers(full_list, place, list_of_all_hands)

# FLUSH:
flush_list = [(hand, {'tier0': 3, 'tier1': get_single(hand)}) for hand in data["flush"]]
print("Flush:")
place = make_tiers(flush_list, place, list_of_all_hands)

# STRAIGHT:
straight_list = [(hand, {'tier0': 4, 'tier1': get_straight_high(hand)}) for hand in data["straight"]]
print("Straight:")
place = make_tiers(straight_list, place, list_of_all_hands)

# THREE OF A KIND:
three_list = [(hand, {'tier0': 5, 'tier1': get_n(hand)}) for hand in data["three kind"]]
print("Three of a kind:")
place = make_tiers(three_list, place, list_of_all_hands)

# TWO PAIR:
two_pair_list = [(hand, {'tier0': 6, 'tier1': get_pairs(hand)}) for hand in data["two pair"]]
print("Two pairs:")
place = make_tiers(two_pair_list, place, list_of_all_hands)

# PAIR:
pair_list = [(hand, {'tier0': 7, 'tier1': get_pairs(hand)}) for hand in data["pair"]]
print("Pair:")
place = make_tiers(pair_list, place, list_of_all_hands)

# SINGLE:
single_list = [(hand, {'tier0': 8, 'tier1': get_single(hand)}) for hand in data["single"]]
print("Single:")
place = make_tiers(single_list, place, list_of_all_hands)

with open('all_hands_ranked.pickle' , 'wb') as file:  # store dict as file
    pickle.dump(list_of_all_hands, file)