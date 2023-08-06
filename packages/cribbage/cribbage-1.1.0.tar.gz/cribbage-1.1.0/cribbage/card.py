from itertools import combinations
from random import shuffle
import sys


class Card:
    """A playing card"""

    suits = "♢♣♡♠"
    suits_ascii = "dchs"
    ranks = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
    vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
    run_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] * 4

    def __init__(self, index=None):
        self.index = index
        self.value = self.vals[index]
        self.run_val = self.run_vals[index]

        self._rank = self.get_rank()
        self._suit = self.get_suit()

    def get_rank(self):
        return self.index % 13

    def get_suit(self):
        return self.index // 13

    def __repr__(self):
        rank = self.ranks[self.get_rank()]
        suit = self.suits[self.get_suit()]
        return "{}{}".format(rank, suit)

    @property
    def ascii_str(self):
        rank = self.ranks[self.get_rank()]
        suit = self.suits_ascii[self.get_suit()]
        self._ascii_str = "{}{}".format(rank, suit)
        return self._ascii_str

    @property
    def rank(self):
        return self.ranks[self._rank]

    @property
    def suit(self):
        return self.suits[self._suit]

    def __add__(self, other):
        return self.value + other.value

    def __radd__(self, other):
        return self.value + other.value

    def __eq__(self, other):
        return self.index == other.index


class Deck:
    """Deck of cards"""

    def __init__(self, shuffled=True):
        self.cards = [Card(n) for n in range(52)]
        if shuffled:
            shuffle(self.cards)

    def draw(self, n=1):
        result = []
        for i in range(n):
            result.append(self.cards.pop())
        return result


def card_from_str(input_str):
    """Create a Card instance from a string"""

    deck = Deck()
    cards = list(deck.draw(52))

    for card in cards:
        if card.ascii_str == input_str:
            return card

    raise ValueError(f'"{input_str}" isn\'t recognized as a card. Expected something like "Qs", "6d", "Jh"')


def hand_from_str(input_str):
    """Create a hand from a string like "Ad 2d 5d 5h 10d"

    Parameters
    ----------
    input_str: str
        A string like "Ad 2d 5d 5h 10d" specifying five cards, with the 
        turn card as the fifth card

    Returns
    -------
    hand: list of Card
        Four cards 

    turn_card: Card
    """

    hand = list(map(card_from_str, input_str.split()))
    return hand[:-1], hand[-1]
