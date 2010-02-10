import dectools
from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted

prnt("Testing the @dectools.call_instead decorator")

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
def add_two(first, second):
    prnt("Adding", first, "and", second)
    return first + second

printed("Testing the @dectools.call_instead decorator")  # nothing else.

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
    In: 3
    Keywords: ( second: 4 )
Adding 3 and 4
    Out: 7""")