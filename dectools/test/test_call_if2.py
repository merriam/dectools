import dectools.dectools as dectools

from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted

prnt("Testing call_if")
def yes(function, args, kwargs):
    return True

def no(function, args, kwargs):
    return False

@dectools.call_if(yes)
def yes_sir():
    prnt("Sir!  Yes, Sir!")

@dectools.call_if(no)
def no_sir():
    prnt("Sir!  No, sir!")
    
yes_sir()
no_sir()
printed("Sir!  Yes, Sir!") 

prnt("Notice when binding happens")
      
def hundreds(function, args, kwargs, number):
    """ Decorator for True iff is an even number of hundreds """
    return number == round(round(number,-2))
    
sixty = 60

@dectools.call_if(hundreds, sixty)
def not_happening():
    prnt("Nope")

sixty = 100
@dectools.call_if(hundreds, sixty)
def is_happening():
    prnt("Sometimes, constants lie.")

not_happening()
is_happening()
p.rinted_lines("""Notice when binding happens
Sometimes, constants lie.""")

prnt("All done.")
