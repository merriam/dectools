# test logging functions

import dectools

from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted

prnt("Testing Verbose")
@dectools.log_verbose
def div1(top, bottom=1):
    return top / float(bottom)

div1(4, bottom=2)
div1(2)
div1(3,0)

@dectools.log_verbose
def greetings(name='Charles'):
    print "Hello, ", name

    
@log_verbose
def add(first, second=0, third=0):
    return first + second + third

hello('bob')
hello()
add(third=3, second=2, first=1)






def div2(top, bottom=1):
    return top / float(bottom)

def div3(top, bottom=1):
    return top / float(bottom)

def div4(top, bottom=1):
    return top / float(bottom)

def div5(top, bottom=1):
    return top / float(bottom)

