import dectools.dectools as dectools
from dectools.dectools import pre, post
from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted

prnt("Testing an internal function:  _dict_as_called")
prnt("Checking simple function with default arguments")

def add(first, second=2, third=3):
    pass

p = dectools._dict_as_called(add, (1, 2, 3), {})
assert (1, 2, 3) == (p['first'], p['second'], p['third'])
p = dectools._dict_as_called(add, (1,), {})
assert (1, 2, 3) == (p['first'], p['second'], p['third'])
p = dectools._dict_as_called(add, (10,), {'third':30})
assert (10, 2, 30) == (p['first'], p['second'], p['third'])
p = dectools._dict_as_called(add, (10, 20), {})
assert (10, 20, 3) == (p['first'], p['second'], p['third'])
p = dectools._dict_as_called(add, (10, 20), {'third': 30})
assert (10, 20, 30) == (p['first'], p['second'], p['third'])
p = dectools._dict_as_called(add, (10,), {'second': 20})
assert (10, 20, 3) == (p['first'], p['second'], p['third'])

prnt("Checking function with arbitrary arguments.")

def annoy(first, second=2, third=3, *args, **kwargs):
    pass

p = dectools._dict_as_called(annoy, (1, 2, 3), {})
assert (1, 2, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoy, (1,), {})
assert (1, 2, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoy, (10,), {'third':30})
assert (10, 2, 30, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoy, (10, 20), {})
assert (10, 20, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoy, (10, 20), {'third': 30})
assert (10, 20, 30, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoy, (10,), {'second': 20})
assert (10, 20, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])

p = dectools._dict_as_called(annoy, (1, 2, 3, 4), {'fourth':4})
assert (1, 2, 3, (4,), {'fourth':4}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoy, (1, 2, 3, 4, '5'), {'fourth':4, 'sixth':6})
assert (1, 2, 3, (4, '5'), {'fourth':4, 'sixth': 6}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])


prnt("And now the munging with signature preservation removes much value.")

@dectools.make_call_if
def always_true(function, args, kwargs):
    return True

@always_true
def annoying(first, second=2, third=3, *args, **kwargs):
    pass
 
p = dectools._dict_as_called(annoying, (1,), {})
assert (1, 2, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoying, (1, 2, 3), {})
assert (1, 2, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoying, (1,), {})
assert (1, 2, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoying, (10,), {'third':30})
assert (10, 2, 30, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoying, (10, 20), {})
assert (10, 20, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoying, (10, 20), {'third': 30})
assert (10, 20, 30, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoying, (10,), {'second': 20})
assert (10, 20, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])

p = dectools._dict_as_called(annoying, (1, 2, 3, 4), {'fourth':4})
assert (1, 2, 3, (4,), {'fourth':4}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = dectools._dict_as_called(annoying, (1, 2, 3, 4, '5'), {'fourth':4, 'sixth':6})
assert (1, 2, 3, (4, '5'), {'fourth':4, 'sixth': 6}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])


prnt("OK!")

