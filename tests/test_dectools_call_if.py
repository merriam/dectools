import dectools
from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted

prnt("Testing the @dectools.call_if decorator")

prnt("*No additonal parameters...")
def check_security(function, args, kwargs):
    prnt("I trust you to run function", function.__name__)
    return True

@dectools.call_if(check_security)
def add_two(first, second):
    prnt("Adding", first, "and", second)
    return first + second

result = add_two(1, 2)
printed("I trust you to run function add_two", back=-2)
printed("Adding 1 and 2")

prnt("1+2=", result)
printed("1+2= 3")

prnt("Example storing data in the function itself.  Watch out for __slots__")
def limit(function, args, kwargs, maximum_calls=10):
    """ You may only call some number of times """
    if hasattr(function, "__limit_calls__"):
        called = function.__limit_calls__ + 1
    else:
        called = 1
    function.__limit_calls__ = called
    if called > maximum_calls:
        prnt("calls exceeded. denied.")
        return False
    else:
        prnt("called", called, "times. ", maximum_calls - called, "remaining.")
        return True


@dectools.call_if(limit, 2)
def hello():
    prnt("hello")
    
hello()
printed("called 1 times.  1 remaining.", back=-2)
printed("hello")
hello()
printed("called 2 times.  0 remaining.", back=-2)
printed("hello")
hello()
printed("calls exceeded. denied.")
hello()
printed("calls exceeded. denied.")

    


prnt("*Extra parameters")
def security_level(function, args, kwargs, level):
    prnt("You are level", level)
    if level == "admin":
        return True
    elif "override_security" in kwargs:
        del kwargs['override_security']
        return True
    else:
        return False

@dectools.call_if(security_level, "admin")
def add_three(first, second, third):
    prnt("adding", first, "+", second, "+", third)
    return first + second + third

result = add_three(1, 2, 3)
prnt("1+2+3 =", result)

@dectools.call_if(security_level, "user")
def subtract_two(first, second):
    prnt("subtracting ", first, "-", second)
    return first - second

result = subtract_two(3, 2)
prnt("3-2=", result)

prnt("*ripping out an argument in passing")
@dectools.call_if(security_level, "user")
def one():
    prnt("one")
    
@dectools.call_if(security_level, "user")
def two(**kwargs):
    assert not kwargs
    prnt("You are new number 2.")

one()
printed("You are level user")
prnt("meaning it failed security and did not print one")
try:
    one(override_security=True)
except TypeError:
    prnt("I used to be able to do that - Now I use signature preserving functions.")
    prnt("one() takes no parameters")
printed("one() takes no parameters")

two(override_security=True)
printed("You are new number 2.")
prnt("That can work however, because two() takes arbitrary parameters.")
prnt("meaning the decorator took a parameter from the call, acted on it, and removed it from the call.")

prnt("*Example of relying on a global")
features = ["general", "print", "email", "twitter"]

def is_feature_installed(function, args, kwargs, feature="general"):
    global features
    prnt("checking feature", feature)
    if feature in features:
        features.remove(feature)
        return True
    else:
        return False

@dectools.call_if(is_feature_installed)
def general_stuff():
    prnt("general stuff")
    
general_stuff()
printed("checking feature general", -2)
printed("general stuff")
general_stuff()
printed("checking feature general")

@dectools.call_if(is_feature_installed, "facebook")
def post_to_facebook(account, password):
    prnt("posting now")

post_to_facebook("me", "password")
printed("checking feature facebook")
prnt("Now update the global")
features = ["general", "print", "email", "twitter", "facebook"]
post_to_facebook("you", "123")
printed("checking feature facebook", -2)
printed("posting now")

prnt("All done")

