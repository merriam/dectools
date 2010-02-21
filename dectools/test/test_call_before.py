# testing @dectools.(make)?_call_(before/after/instead)
import dectools.dectools as dectools
from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted
    
prnt("testing @dectools.(make)?_call_(before/after/instead)")

prnt("Testing the @dectools.make_call_before")
@dectools.make_call_before
def a_call_before_decorator(function, args, kwargs, message):
    prnt("I'm being called before", function.__name__, "!", message)
    return False # return value doesn't matter

@a_call_before_decorator("Yahoo!")
def hello_everyone(names):
    prnt("Hello everybody.  So nice to see you")
    for name in names:
        prnt("Hello to", name + ".  So nice to see you too!")

hello_everyone(["Andrew", "David"])

p.rinted_lines("""Testing the @dectools.make_call_before
I'm being called before hello_everyone ! Yahoo!
Hello everybody.  So nice to see you
Hello to Andrew.  So nice to see you too!
Hello to David.  So nice to see you too!""")

prnt("Testing make_call_before/make_call_after/make_call_instead mixed.")
prnt("make_call_before/make_call_after order doesn't matter")

@dectools.make_call_before
def before_no_args(function, args, kwargs):
    prnt("Called before..")
    
@dectools.make_call_after
def after_no_args(function, args, kwargs):
    prnt("Called after.")
    
@dectools.make_call_instead
def during_no_args(function, args, kwargs):
    prnt("Called during...")
    
@before_no_args
@after_no_args
@during_no_args
def i_will_call_you():
    prnt("so do not call me.")

i_will_call_you()
p.rinted_lines("""Testing make_call_before/make_call_after/make_call_instead mixed.
make_call_before/make_call_after order doesn't matter
Called before..
Called during...
Called after.""")

prnt("Now we do it again, but without using the make_call_* routines.")
prnt("Testing the @dectools.call_before")
def a_call_before_function(function, args, kwargs, message):
    prnt("I'm being called before", function.__name__, "!", message)
    return False # return value doesn't matter

@dectools.call_before(a_call_before_function, "Yahoo!")
def hello_everyone_again(names):
    prnt("Hello everybody.  So nice to see you")
    for name in names:
        prnt("Hello to", name + ".  So nice to see you too!")

hello_everyone_again(["Andrew", "David"])

p.rinted_lines("""Testing the @dectools.call_before
I'm being called before hello_everyone_again ! Yahoo!
Hello everybody.  So nice to see you
Hello to Andrew.  So nice to see you too!
Hello to David.  So nice to see you too!""")

prnt("Testing call_before/call_after/call_instead mixed.")

def before_again(function, args, kwargs):
    prnt("Called before..")
    
def after_again(function, args, kwargs):
    prnt("Called after.")
    
def during_again(function, args, kwargs):
    prnt("Called during...")
    
@dectools.call_after(after_again)
@dectools.call_before(before_again)
@dectools.call_instead(during_again)
def i_will_call_you_again():
    prnt("so do not call me.")

i_will_call_you_again()
p.rinted_lines("""Testing call_before/call_after/call_instead mixed.
Called before..
Called during...
Called after.""")

prnt("If call_instead does not call the original function, then order matters.")
@dectools.call_after(after_again)
@dectools.call_instead(during_again)
@dectools.call_before(before_again)
def i_will_not_call_you_again():
    prnt("Have a nice day!")
    
i_will_not_call_you_again()

p.rinted_lines("""If call_instead does not call the original function, then order matters.
Called during...
Called after.""")

prnt("My call_instead(during_again) overwrote my decorated by call_before(before_again)!")

prnt("All done.")
