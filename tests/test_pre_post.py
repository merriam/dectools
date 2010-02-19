import dectools
from dectools import pre, post
from print_buffer import print_buffer
import types

p = print_buffer()
prnt = p.rint
printed = p.rinted


ok = "self.name and self.price >= 0 and Item.tax_rate >= 0"   # Item only in globals(), locals()
ok2 = "self.name and self.price >= 0 and self.tax_rate >= 0"  # does not need globals(), locals())

class Item(object):
    tax_rate = 0.10
    
    @post("3==3")
    @post("self.price == self.price * 2 * 0.5")
    @post("True")
    @post(ok, globals(), locals())
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    @pre(ok, globals(), locals())
    @post(ok2)
    @pre("adjustment < 0")
    def adjust_price(self, adjustment):
        self.price += adjustment
        
    @post(ok, globals(), locals())
    @pre(ok2)
    def get_taxes(self):
        return self.price * Item.tax_rate
    
    
p = Item("Dead Parrot", 1.00)
prnt("That's a ", p.name, "!")
prnt("OK.  I'll knock off half a quid.")
p.adjust_price(-0.5)
prnt("So that comes to", p.price , "plus tax of ", p.get_taxes())
prnt("Right.  Wrap it up.")

prnt("======================================")
prnt("All Finished")