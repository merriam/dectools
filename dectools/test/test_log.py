# test logging functions

import dectools.dectools as dectools

from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted
printed_lines = p.rinted_lines

prnt("Testing logging with simple calls")

@dectools.logging(output=prnt) 
def greetings(name='Charles'):
    """ Print a greeting. """
    prnt("Hello, ", name)

greetings('bob')
printed_lines("""greetings: called with args:('bob',){}
Hello,  bob
greetings: returned value:None""")
greetings()
printed_lines("""greetings: called with args:('Charles',){}
Hello,  Charles
greetings: returned value:None""")

prnt("Now, output to our own prnt function")
@dectools.logging(prnt)  # Notice the hard-to-debug error is I call without parens.
def greetings2(name='Charles'):
    """ Print a greeting. """
    prnt("Hello, ", name)

greetings2('bob')
printed_lines("""greetings2: called with args:('bob',){}
Hello,  bob
greetings2: returned value:None""")

prnt("Testing Verbose")

@dectools.logging(output=prnt, before=None, after=lambda f,a,kw,e,r: ":"+f.__name__)
def div1(top, bottom=1):
    return top / float(bottom)

try:
    div1(3,0)
except ZeroDivisionError:
    printed(":div1")
    prnt("We printed.")
else:
    assert False


div1(4, bottom=2)
prnt(":div1")

prnt("All done")