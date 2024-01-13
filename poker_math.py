import itertools
import pickle
from collections import Counter
ranks = '23456789TJQKA'
suits = {'spades': '\u2660',
         'clubs': '\u2663',
         'hearts': '\u2665',
         'diamonds': '\u2666'}
# suit_order for hand sorting
suit_order = {suits['spades']:0,
              suits['hearts']: 1,
              suits['diamonds']: 2,
              suits['clubs']: 3}
hand_dict = {'straight flush': set(),
             "four kind": set(),
             "full house": set(),
             "flush": set(),
             "straight": set(),
             "three kind": set(),
             "two pair": set(),
             "pair": set(),
             "single": set(),
             "all": set()}
def order_ranks(ranks):
    # assign a numeric rank order for hand sorting
    rank_dict = {}
    for index, rank in enumerate(ranks[-1::-1]):
        rank_dict[rank] = index
    return rank_dict
rank_order = order_ranks(ranks)
def make_straights(ranks):
    # generate a list of sets of ranks that are straights
    ranks = ranks[-1] + ranks
    straights = []
    for n in range(10):
        straights.append(set(ranks[n: n + 5]))
    return straights
def parse_hand(hand):
    # takes a hand and returns a tuple of
    # 0: a set of ranks for straight matching
    # 1: a sorted tuple of rank distribution for n-of-a kind matching
    # 2: a tuple of suit distribution for flush matching
    ranks = []
    suits = []
    for card in hand:
        rank, suit = card
        ranks.append(rank)
        suits.append(suit)
    rank_count = Counter(ranks)
    suit_count = Counter(suits)
    rank_list = sorted(rank_count.values(), reverse = True)
    rank_tuple = tuple([n for n in rank_list])
    suit_tuple = tuple([s for s in suit_count.values()])
    return (set(ranks), rank_tuple, suit_tuple)

deck = list(itertools.product(ranks, suits.values()))
all_hands = set(itertools.combinations(deck, 5))
all_hands = {tuple(sorted(hand, key=lambda x: (rank_order[x[0]], suit_order[x[1]]), reverse=False)) for hand in all_hands}
#sorts each hand so that order need not be a concern

straights = make_straights(ranks)
flushes = set(hand for hand in all_hands if parse_hand(hand)[2] == (5,))
straights = set(hand for hand in all_hands if set(parse_hand(hand)[0]) in straights)
not_straight_or_flush = all_hands - flushes - straights
straight_flushes = flushes.intersection(straights)
flushes = flushes - straight_flushes
straights = straights - straight_flushes

for hand in not_straight_or_flush:
    # populate the hand_dict. this prolly should have been done previously
    rank_tuple = parse_hand(hand)[1]
    match rank_tuple:
        case (4,1):
            hand_dict['four kind'].add(hand)
        case(3,2):
            hand_dict['full house'].add(hand)
        case (3,1,1):
            hand_dict['three kind'].add(hand)
        case (2,2,1):
            hand_dict['two pair'].add(hand)
        case (2,1,1,1):
            hand_dict['pair'].add(hand)
        case (1,1,1,1,1):
            hand_dict['single'].add(hand)
hand_dict['straight flush'] = straight_flushes
hand_dict['straight'] = straights
hand_dict['flush'] = flushes
hand_dict['all'] = all_hands
for key in hand_dict:
    print(f'{key}: {len(hand_dict[key])}')

with open('hands.pickle' , 'wb') as file:  # store dict as file
    pickle.dump(hand_dict, file)
