# testing dec_tools

import dectools

def once(function):
    print "Just decorated", function.__name__

@dectools.call_once(once)
def hello():
    print "Hello"

@dectools.make_call_once
def once(function):
    """ Called only once,just as the function is decorated """
    print "just decorated", function.__name__
    
@once
def hello(name = "Charles"):
    print "Hello", name
    
@dectools.make_call_once
def once_with_message(function, message = "Compiling"):
    """ Called only once, with the message """
    print message, "in", function.__name__
    
@once_with_message("I am happy")
def bye():
    print "bye"
    
@once
@once_with_message()
def yes():
    print "yes"
    
@dectools.make_call_once
def print_message_once(function):
    """ print a message and the function name """
    print "in", function.__name__

@print_message_once
def print_hello_2(name=""):
    """ print Hello with optional name """
    print "Hello!", name, "!"
    
@once_with_message("Registering this meeting")
class Meeting(object):
    @once
    def good_morning(self):
        print "Good morning!"
    
    @once_with_message("Need to have people meet more")
    def meet(self):
        print "I don't know you."
    
m = Meeting()
m.good_morning()
m.meet()

def add_author(function):
    function.__author__ = "ME"

@call_once(add_author)
def think():
    print "THINK!"

def register(function, url):
    print "In a real world, this would register", function.__name__, "to the url", url
    
@call_once(register("foo.html"))
def foo():
    print "Foo!"




# This fails    
#@dectools.make_call_once
#def print_message(message, function, *args, **kwargs):
    #""" print a message and the function name """
    #print message, "in", function.__name__

     
     
        #assert code.co_argcount >= 3 and (
            #code.co_varnames[0:3] == ("function", "args", "kwargs")
            #), "New decorator must start with function, args, kwargs parameters."

            