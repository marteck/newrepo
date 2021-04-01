from random import shuffle


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def card_value(self):
        if self.rank in ["Ten", "Jack", "Queen", "King"]:
            return 10
        else:
            return [" ", "Ace", "Deuce", "Three", "Four", "Five", "Six", "Seven", "Eight",
                    "Nine"].index(self.rank)

    def get_rank(self):
        return self.rank

    def __str__(self):
        return '{} {},'.format(self.rank, self.suit)


class Deck:
    def __init__(self):
        ranks = ["Deuce", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                 "Jack", "Queen", "King", "Ace"]
        suits = ["\u2666", "\u2660", "\u2665", "\u2663"]
        self.cards = [Card(r, s) for r in ranks for s in suits]
        shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def new_4deck(self):
        return self.cards * 4


class Hand:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        points = 0
        ace = 0
        for card in self.cards:
            points += card.card_value()
            if card.get_rank() == "Туз":
                ace += 1
        if points + ace * 10 <= 21:
            points += ace * 10
        return points

    def __str__(self):
        message = "{0} has:".format('{}'.format(self.name))
        for card in self.cards:
            message += str(card) + " "
        return message


