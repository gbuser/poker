import itertools
import random
from collections import Counter
import pickle
path = "hand_dict.pickle"
file = open(path, 'rb')
# data now a dict of hands each with dict of tier0, tier1, place
data = pickle.load(file)
file.close()

ranks = '23456789TJQKA'
rank_order = {rank:value for value, rank in enumerate(ranks[-1::-1])}
#print(rank_order)
hand_to_rank = {"straight flush": 0,
              "four of a kind": 1,
              "full house": 2,
              "flush": 3,
              "straight": 4,
              "three of a kind": 5,
              "two pairs": 6,
              "pair": 7,
              "single": 8}
rank_to_hand = {k:v for v, k in hand_to_rank.items()}
suits = {'s': {'symbol': '\u2660',
               'order' : 0,
               'full_name': 'spades'},
         'h': {'symbol': '\u2665',
               'order': 1,
               'full_name': 'hearts'},
         'd': {'symbol': '\u2666',
               'order': 2,
               'full_name': 'diamonds'},
         'c': {'symbol': '\u2663',
               'order': 3,
               'full_name': 'clubs'}}
suit_order = {suits[key]['symbol']: suits[key]['order'] for key in suits}

#print(suit_order)
def make_deck():
    deck =  list(itertools.product(ranks, suits.keys()))
    deck = [(rank, suits[suit]['symbol']) for rank, suit in deck]
    return deck

class Card():
    def __init__(self, rank, suit, image=None):
        self.rank = rank
        self.suit = suit
        self.image = image

def deal_cards(n, deck):
    cards = []
    for i in range(n):
        cards.append(deck.pop())
    return cards

def sort_hand(hand):
    hand = sorted(hand, key=lambda x: ((rank_order[x[0]], suit_order[x[1]])), reverse=False)
    return tuple(hand)


def translate(hand):
    # takes hand string in 'ks ad 8c th 3s' format and returns tuple with suit symbols
    hand = hand.split()
    hand = tuple([(x[0].upper(), suit_symbols[x[1]]) for x in hand])
    return hand

def string_hand(hand):
    string = ''
    for card in hand:
        string += f'{card[0]}{card[1]} '
    return (string)

#deck = (make_deck())
#random.shuffle(deck)
#hand = (deal_cards(5, deck))
#hand = sort_hand(hand)
#print(hand)
#print(f'{rank_to_hand[(data[hand]['tier0'])]}, this hand ranks: {data[hand]['place']:,}th')