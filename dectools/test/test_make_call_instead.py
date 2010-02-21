import dectools.dectools as dectools
from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted

prnt("Testing the @dectools.call_instead decorator")

prnt("Testing identity")

@dectools.make_call_instead
def identity(function, args, kwargs):
    prnt("Identity of", function.__name__)
    ret_value = function(*args, **kwargs)
    return ret_value

@identity
def add_three(first, second, third = 3):
    """ Add three numbers """
    total = first + second + third
    prnt("add_three total is", total)
    return total

printed("Testing identity")
prnt("Name is", add_three.__name__)
printed("Name is add_three")
prnt("Arguments are", add_three.__code__.co_varnames)
printed("Arguments are ('first', 'second', 'third')")
prnt("Defaults are", add_three.func_defaults)
printed("Defaults are (3,)")
prnt("Doc may have changed:\n", add_three.func_doc) 
prnt("But does it work?")
t = add_three(10, 20, 30)
printed("Identity of add_three", -2)
printed("add_three total is 60")

prnt("----------")
prnt("Testing the minor_trace decorator") 

@dectools.make_call_instead
def minor_trace(function, args, kwargs, prompt=">", indent=None):
    if indent is None:
        indent = len(prompt)
    prnt(prompt, "Function:", function.__name__)
    prnt(" " * indent, "In:", ",".join([str(arg) for arg in args]))
    prnt(" " * indent, "Keywords: (", ",".join(
               str(key) + ": "+ str(value) for key, value in kwargs.iteritems()), ")")
    ret_value = function(*args, **kwargs)
    prnt(" " * indent, "Out:", str(ret_value))
    return ret_value

@minor_trace(">>>", indent=3)
def add_two(first, second=2):
    prnt("Adding", first, "and", second)
    return first + second

printed("Testing the minor_trace decorator")  # nothing else.
prnt("Name is", add_two.__name__)
printed("Name is add_two")
prnt("Arguments are", add_two.__code__.co_varnames)
printed("Arguments are ('first', 'second')")
prnt("Defaults are", add_two.func_defaults)
printed("Defaults are (2,)")
prnt("Doc may have changed:\n", add_two.func_doc)
assert 'see __decorators__' in add_two.func_doc
prnt("And it has notes:\n", add_two.__decorators__)
assert 'minor_trace(' in "".join(add_two.__decorators__)
prnt("And a chain:", add_two.__decorator_chain__)

prnt("And look at minor_trace itself")
prnt("Name is", minor_trace.__name__)
printed("Name is minor_trace")
prnt("Arguments are", minor_trace.__code__.co_varnames)
printed("Arguments are ('prompt', 'indent')")
prnt("Defaults are", minor_trace.func_defaults)
printed("Defaults are ('>', None)")
prnt("Doc may have changed:\n", minor_trace.func_doc)
assert 'see __decorators__' in minor_trace.func_doc
prnt("And it has notes:\n", "".join(minor_trace.__decorators__))
assert 'minor_trace' in "".join(minor_trace.__decorators__)
prnt("And a chain:", minor_trace.__decorator_chain__)

prnt("Sort of.  Notice that I capture more as received than as called.")
add_two(1, 2)
p.rinted_lines(\
""">>> Function: add_two
    In: 1,2
    Keywords: (  )
Adding 1 and 2
    Out: 3""")
add_two(3, second=4)
p.rinted_lines(\
""">>> Function: add_two
    In: 3,4
    Keywords: (  )
Adding 3 and 4
    Out: 7""")
add_two(10)
p.rinted_lines(\
""">>> Function: add_two
    In: 10,2
    Keywords: (  )
Adding 10 and 2
    Out: 12""")
prnt("I can write a trace() that destroys the signatures and captures the way the")
prnt("function is called, or I can preserve the signatures and lose the information.")
prnt("I can only pick one.")

prnt("All done")
