import random

def get_suit_name(char):
    assert(char == 'c' or char == 'd' or char == 's' or char == 'h')

    if char == 'c':
        return 'Club'
    if char == 'd':
        return 'Diamond'
    if char == 'h':
        return 'Heart'
    if char == 's':
        return 'Spade'

class Cardinal:
    North, East, South, West = range(4)

class Deck(object):
    def __init__(self):
        self.deck = [['c',1],['c',2],['c',3],
                     ['c',4],['c',5],['c',6],
                     ['c',7],['c',8],['c',9],
                     ['c',10],['c',11],['c',12],
                     ['c',13],

                     ['d',1],['d',2],['d',3],
                     ['d',4],['d',5],['d',6],
                     ['d',7],['d',8],['d',9],
                     ['d',10],['d',11],['d',12],
                     ['d',13],

                     ['h',1],['h',2],['h',3],
                     ['h',4],['h',5],['h',6],
                     ['h',7],['h',8],['h',9],
                     ['h',10],['h',11],['h',12],
                     ['h',13],

                     ['s',1],['s',2],['s',3],
                     ['s',4],['s',5],['s',6],
                     ['s',7],['s',8],['s',9],
                     ['s',10],['s',11],['s',12],
                     ['s',13]]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        
        assert(len(self.deck) == 52)

        north = []
        east = []
        south = []
        west = []
        self.shuffle()

        left = 52
        while left > 0:
            north.append(self.deck[left - 1])
            east.append(self.deck[left - 2])
            south.append(self.deck[left - 3])
            west.append(self.deck[left - 4])
            left -= 4
            
        return north, east, south, west

    def show(self):
        for card in self.deck:
            print card

class Player(object):
    def __init__(self, seat):
        self.hand = []
        self.score = 0
        self.seat = seat

    def get_seat(self):
        return self.seat

    def set_seat(self, seat):
        self.seat = seat

    def inc_score(self, inc):
        self.score += inc

    def get_score(self):
        return self.score

    def set_hand(self, hand):
        self.hand = sorted(hand, key=lambda p: p[0])

    def get_hand(self):
        return self.hand

    def show(self):
        spades = []
        hearts = []
        diamonds = []
        clubs = []

        for card in self.hand:
            if card[0] == 's':
                spades.append(card[1])
            if card[0] == 'h':
                hearts.append(card[1])
            if card[0] == 'd':
                diamonds.append(card[1])
            if card[0] == 'c':
                clubs.append(card[1])

        s = 'S: '
        for spade in sorted(spades):
            s += str(spade) + ', '

        h = 'H: '
        for heart in sorted(hearts):
            h += str(heart) + ', '

        d = 'D: '
        for diamond in sorted(diamonds):
            d += str(diamond) + ', '

        c = 'C: '
        for club in sorted(clubs):
            c += str(club) + ', '

        return (s + '\n' + h + '\n' + d + '\n' + c)

    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return True
        else:
            return False

class Hearts(object):
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.players = [Player(Cardinal.North),  Player(Cardinal.East),
                        Player(Cardinal.South),  Player(Cardinal.West)]

    def deal(self):
        self.players[0].hand, self.players[1].hand, self.players[2].hand, self.players[3].hand  =  self.deck.deal()

    def get_player(self, p):
        assert(p >= 0 and p <= 3)
        return self.players[p]

    def score_trick(self, cards_played):
        lead_suit = cards_played[0][0]
        max = 0
        points = 0

        print lead_suit

        for card in cards_played:
            print card
            if card[0] == lead_suit and (card[1] > max or card[1] == 1):
                if card[1] == 1:
                    max = 100 
                else: 
                    max = card[1]
                loser = card[2] # this index holds who played trick
            if card[0] == 's' and card[1] == 12: # queen of spades
                points += 13
            if card[0] == 'h':
                points += 1

        self.players[loser].inc_score(points)

    def game_over(self):
        for player in self.players:
            if player.get_score() >= 100:
                print player.get_score()
                return True

        return False

    def get_score(self):
        score = 'N: ' + str(self.players[0].get_score()) + ' E: ' + str(self.players[1].get_score()) + ' S: ' + str(self.players[2].get_score()) + ' W: ' + str(self.players[3].get_score())

        return score
