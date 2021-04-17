import numpy as np
from Constants import *


class CommunityChest:
    def __init__(self):
        self._unused_deck = [GO, OLD_KENT_ROAD, IN_JAIL, NO_MOVE, NO_MOVE, NO_MOVE, NO_MOVE, NO_MOVE, NO_MOVE, NO_MOVE,
                             NO_MOVE, NO_MOVE, NO_MOVE, NO_MOVE, NO_MOVE, NO_MOVE]
        self._used_deck = []

    def pick_up_card(self):
        if len(self._unused_deck) == 0:
            self._unused_deck = self._used_deck
            self._used_deck = []
        picked_card = self._unused_deck[np.random.randint(len(self._unused_deck))]
        self._used_deck.append(picked_card)
        self._unused_deck.remove(picked_card)
        return picked_card
