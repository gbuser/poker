import poker
print('\nBegin test module:\n')
suit_symbols = {'s': '\u2660',
                'c': '\u2663',
                'h': '\u2665',
                'd': '\u2666'}
def translate(hand):

    for key, value in suit_symbols.items():
        hand = hand.replace(key, value)
    print(hand)
    hand = hand.split()
    hand = [(x[0], x[1:]) for x in hand]
    return hand

hands = ['As Ks Qs Js Ts',
         'Qs As Ts Js Ks',
         'As 8s 7s 5s 3s',
         'Ks Kd Kc 8d 8s',
         'Ks Ks 8d 8s Kd',
         'Ks Kd 8d Kc Kh',
         '8s 8d 6s 7d 8h',
         '5s Ts 7d 5d Tc',
         '6s 5d Qc Qs Ah',
         'As Kd Qc 6h 7d',
         ]
for hand in hands:
    hand = translate(hand)
    hand_ID = (poker.identify_hand(hand))
    print(f'{hand_ID[0]}: {', '.join(hand_ID[1])}\n')

