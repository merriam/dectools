import dectools
from dectools import pre, post
from print_buffer import print_buffer
import types

p = print_buffer()
prnt = p.rint
printed = p.rinted


prnt("Now, let's add invariants but just with self and no locals(), globals()")
import random

def _public_methods(cls):
    """ list of public methods in the cls """
    methods = [item for item in dir(cls) if item[0] != '_' and 
        type(getattr(cls, item)) == types.UnboundMethodType]
    return methods

@dectools.make_call_instead
def _call_invariant(function, args, kwargs):
 
    """ Call _invariant on one method, before and after.  Avoid the infinite
         recursion problem.  """
    
    # get self
    assert function.__code__.co_varnames[0] == 'self'
    self = args[0] if args else kwargs['self']
    # No, I have never seen a default argument for self.

    if function.__name__ != '__init__':
        if not hasattr(self, '_invariant_recursion'):
            self._invariant_recursion = True       
            self._invariant()        # pre
            del self._invariant_recursion

    try:
        return_val = function(*args, **kwargs)
    except:
        if not hasattr(self, '_invariant_recursion'):
            self._invariant_recursion = True       
            self._invariant()        # pre
            del self._invariant_recursion
        raise
    if not hasattr(self, '_invariant_recursion'):
        self._invariant_recursion = True       
        self._invariant()        # pre
        del self._invariant_recursion
    return return_val        
    
def invariant(cls):
    """ Decorate __init__ and each public method to call _invariant(). """
    for method in _public_methods(cls) + ['__init__']:
        func = getattr(cls, method).__func__
        func = _call_invariant(func)
        setattr(cls, method, func)
    return cls

@invariant
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

@invariant
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

