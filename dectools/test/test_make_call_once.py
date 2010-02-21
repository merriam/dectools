# testing dec_tools

import dectools.dectools as dectools

from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted
    
prnt("Testing the @dectools.make_call_once")
prnt("With once taking no arguments.")

@dectools.make_call_once
def once(function):
    """ Called only once,just as the function is decorated """
    prnt("just decorated function/class", function.__name__)
    
prnt("Name of function once is:", once.__name__)
printed("Name of function once is: once")
prnt("Function once:", once)

@once
def hello(name = "Charles"):
    prnt("Hello", name)

printed("just decorated function/class hello")
hello()
printed("Hello Charles")
hello("Bob")
printed("Hello Bob")

prnt("With once taking arguments.")

    
@dectools.make_call_once
def once_with_message(function, message = "Compiling"):
    """ Called only once, with the message """
    prnt(message, "at function", function.__name__)
    
@once_with_message("I am happy being called")
def bye():
    prnt("bye")
printed("I am happy being called at function bye") 
bye()
printed("bye")
    
@once
@once_with_message()
def yes():
    prnt("yes")
printed("Compiling at function yes", back=-2)
printed("just decorated function/class yes")
prnt("==========")

@dectools.make_call_once
def print_message_once(function):
    """ print a message and the function name """
    prnt("in", function.__name__)

@print_message_once
def print_hello_2(name=""):
    """ print Hello with optional name """
    prnt("Hello!", name, "!")
printed("in print_hello_2")
    
@once_with_message("Registering this class")
class Meeting(object):
    @once
    def good_morning(self):
        prnt("Good morning!")
    
    @once_with_message("Need to have people meet more")
    def meet(self):
        prnt("I don't know you.")
        
printed("just decorated function/class good_morning", back=-3)
printed("Need to have people meet more at function meet", back=-2)
printed("Registering this class at function Meeting")
    
m = Meeting()
m.good_morning()
printed("Good morning!")
m.meet()
printed("I don't know you.")

prnt("All Done")

#try:
#    @dectools.make_call_once
#    def print_message(message, function, *args, **kwargs):
#        print "Hi"
#except:
# This fails    
#@dectools.make_call_once
#def print_message(message, function, *args, **kwargs):
    #""" print a message and the function name """
    #print message, "in", function.__name__

     
     
        #assert code.co_argcount >= 3 and (
            #code.co_varnames[0:3] == ("function", "args", "kwargs")
            #), "New decorator must start with function, args, kwargs parameters."

"""            
        This is roughly equivalent to:
        >>> def once_function(function):
        ...     print "called once_function while compiling", function.__name__
        ... 
        >>> once_function_decorator = dectools.make_call_once(once_function)
        >>> def hello_function():
        ...     print "hello"
        ... 
        >>> new_hello_function = once_function_decorator(hello_function)
        called once_function while compiling hello_function
        >>> hello_function == new_hello_function
        True
        >>>         
"""