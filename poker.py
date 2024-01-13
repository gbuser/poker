import itertools
import random
from collections import Counter
ranks = '23456789TJQKA'
suits = {'spades': '\u2660',
         'clubs': '\u2663',
         'hearts': '\u2665',
         'diamonds': '\u2666'}
n_kinds = {(4,1): "four of kind",
           (3,2): "full house",
           (3,1,1): "three of kind",
           (2,2,1): "two pairs",
           (2,1,1,1): "pair",
           (1,1,1,1,1): "single"}

def make_deck():
    return list(itertools.product(ranks, suits.values()))
def make_straights(ranks):
    straights = []
    ranks = ranks[-1] + ranks
    for index, rank in enumerate (ranks[:10]):
        straights.append(set(ranks[index:index + 5]))

    return straights
def order_ranks(ranks):
    rank_order = {}
    for index, rank in enumerate(ranks[-1::-1]):
        rank_order[rank] = index
    return rank_order

def sort_hand(hand):
    hand = sorted(hand, key=lambda x: (rank_order[x[0]]), reverse=False)
    return hand
def identify_hand(hand):
    ranks = []
    suits = []
    hand_type = ''
    hand = sort_hand(hand)
    high_card = hand[0][0]
    flush = straight = False
    for card in hand:
        rank, suit = card
        ranks.append(rank)
        suits.append(suit)
    if suits.count(suits[0]) == 5:
        flush = True
    if set(ranks) in straights:
        straight = True
    if flush and straight:
        return "straight flush", high_card
    if flush:
        return "flush", high_card
    if straight:
        return "straight", high_card
    rank_count = tuple(sorted(Counter(ranks).values(), reverse = True))
    counts = {'four': None,
              'three': None,
              'two': [],
              'one': []}
    for rank, count in Counter(ranks).items():
        if count == 4:
            counts['four'] = rank
        if count == 3:
            counts['three'] = rank
        if count == 2:
            counts['two'].append(rank)
        if count == 1:
            counts['one'].append(rank)
    hand_type = n_kinds[rank_count]
    match hand_type:
        case "four of a kind":
            high_card = counts['four']
        case "full house":
            high_card = (counts['three'])
        case "three of a kind":
            high_card = counts['three']
        case "two pairs":
            high_card = tuple(sorted(counts['two'], reverse = True))
        case "pair":
            high_card = counts['two']
        case "single":
            high_card = ranks[0]
    return hand_type, high_card



def deal_cards(n, deck):
    cards = []
    for i in range(n):
        cards.append(deck.pop())
    return cards
def print_hand(hand):
    string = ''
    for card in hand:
        string += f'{card[0]}{card[1]} '
    print(string)


deck = make_deck()
straights = make_straights(ranks)
rank_order = order_ranks(ranks)
random.shuffle(deck)
hand = deal_cards(5, deck)
hand = sort_hand(hand)
print(hand)
print_hand(hand)
hand_ID = (identify_hand(hand))
print(f'{hand_ID[0]}: {', '.join(hand_ID[1])}')