import dectools.dectools as dectools
from dectools.dectools import pre, post
from print_buffer import print_buffer
import types

p = print_buffer()
prnt = p.rint
printed = p.rinted


prnt("Now, let's add invariants but just with self and no locals(), globals()")
import random

@dectools.invariant
class Deck(object):
    def __init__(self, cards = 52, players=2, piles=0):
        self.cards = cards
        self.deck = range(cards)
        random.shuffle(self.deck)
        self.discards = []
        self.players = [list() for player in range(players)]
        self.tableau = [list() for player in range(players)]
        self.piles = [list() for pile in range(piles)]
        
    def _invariant(self):
        print "testing"
        assert self._all_cards_accounted_for()
        assert len(self.players) < 99
        
    def _all_cards_accounted_for(self):
        """ Avoid recursion.  Make me private (start with underscore). """
        all_cards = self.deck + self.discards + sum(self.players + self.tableau + self.piles, [])
        one_each = set(all_cards) == set(range(self.cards))
        return len(all_cards) == self.cards and one_each
        
    def draw(self, destination, cards_to_draw = 1):
        assert cards_to_draw <= len(self.deck) + len(self.discards), "Cannot draw that many!"
        if cards_to_draw <= len(self.deck):
            destination.extend(self.deck[:cards_to_draw])
            self.deck = self.deck[cards_to_draw:]
        else:
            more_to_draw = cards_to_draw - len(self.deck)
            destination.extend(self.deck[:])
            self.deck, self.discards = self.discards, []
            random.shuffle(self.deck)
            self.draw(destination, more_to_draw)
            
    def deal(self, cards_per_player):
        for player in self.players:
            self.draw(player, cards_per_player)
                
def bad_assert(string, the_globals, the_locals):
    try:
        eval(string, the_globals, the_locals)
    except AssertionError:
        pass
    else:
        assert False, "Failed"
        
d = Deck(players=2, cards=20)
d.deal(5)
d.deal(1)
d.deal(1)
d.players[0][0] = d.players[1][0]
bad_assert("d.draw(d.players[0])", globals(), locals())
bad_assert("Deck(players=100, cards=200)", globals(), locals())

prnt("======================================")

@dectools.invariant
class numbers:
    def __init__(self):
        self.num1 = 4
        self.num2 = 8
        
    def _invariant(self):
        assert self.total() < 20
    
    def total(self):
        return self.num1 + self.num2
    
n = numbers()
prnt(n.total())
n.num1 = 39
bad_assert("n.total()", globals(), locals())
prnt("All Finished")

