# test logging functions

import dectools

from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted

prnt("Testing log_verbose with simple calls")

prnt("First, output to stdout")
@dectools.log_verbose()  # Notice the hard-to-debug error is I call without parens.
def greetings(name='Charles'):
    """ Print a greeting. """
    prnt("Hello, ", name)

greetings('bob')
greetings()

prnt("Now, output to our own prnt function")
@dectools.log_verbose(prnt)  # Notice the hard-to-debug error is I call without parens.
def greetings2(name='Charles'):
    """ Print a greeting. """
    prnt("Hello, ", name)

greetings2('bob')
greetings2()


prnt("Testing Verbose")
@dectools.log_verbose()
def div1(top, bottom=1):
    return top / float(bottom)

div1(4, bottom=2)
div1(2)
try:
    div1(3,0)
except ZeroDivisionError:
    pass
else:
    assert False

    
@dectools.log_verbose()
def add(first, second=0, third=0):
    return first + second + third


add(third=3, second=2, first=1)






def div2(top, bottom=1):
    return top / float(bottom)

def div3(top, bottom=1):
    return top / float(bottom)

def div4(top, bottom=1):
    return top / float(bottom)

def div5(top, bottom=1):
    return top / float(bottom)

