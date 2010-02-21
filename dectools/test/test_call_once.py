# testing dec_tools

import dectools.dectools as dectools
from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted

prnt("testing @dectools.(make)?_call_if")
    
prnt("Testing the @dectools.call_once")

def add_author(function):
    function.__author__ = "ME"

@dectools.call_once(add_author)
def think():
    prnt("THINK!")

prnt("Call once returns the original function:", think.__name__)
printed("Call once returns the original function: think")

prnt("Now we have an attribute:", think.__author__)
printed("Now we have an attribute: ME")

def register(function, url):
    prnt("In a real world, this would register", function.__name__, "to the url", url)
    
@dectools.call_once(register, url="license.html")
def license():
    prnt("All your base belong to us!")
printed("In a real world, this would register license to the url license.html")
    

def once(function):
    prnt("Just decorated", function.__name__)

@dectools.call_once(once)
def hello():
    prnt("Hello")
printed("Just decorated hello")
prnt("Hello still works")
hello()
printed("Hello")

@dectools.call_once(once)
@dectools.call_once(once)
@dectools.call_once(register, "goodbye.html")
@dectools.call_once(register, url="done.html")
def goodbye():
    prnt("Goodbye!")
printed("In a real world, this would register goodbye to the url done.html", -4)
printed("In a real world, this would register goodbye to the url goodbye.html", -3) 
printed("Just decorated goodbye", -2)
printed("Just decorated goodbye")

goodbye()
printed("Goodbye!")
prnt("All Done")

