import dectools.dectools as dectools
from print_buffer import print_buffer
p = print_buffer()
prnt = p.rint
printed = p.rinted

prnt("Testing the @dectools.make_call_if decorator")
prnt("==================")

prnt("*No additonal parameters...")

@dectools.make_call_if
def check_security(function, args, kwargs):
    prnt("I trust you to run function", function.__name__)
    return True

@check_security
def add_two(first, second):
    prnt("Adding", first, "and", second)
    return first + second

result = add_two(1, 2)
printed("I trust you to run function add_two", back=-2)
printed("Adding 1 and 2")

prnt("1+2=", result)
printed("1+2= 3")
prnt("==================")

prnt("Example storing data in the function itself.  Watch out for __slots__")
@dectools.make_call_if
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


@limit(2)
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
prnt("==================")

prnt("*Extra parameters checked/ripped by the decorator")
@dectools.make_call_if
def security_level(function, args, kwargs, level):
    prnt("You are level", level)
    if level == "admin":
        return True
    elif "override_security" in kwargs:
        del kwargs['override_security']
        return True
    else:
        return False

@security_level("admin")
def add_three(first, second, third):
    prnt("adding", first, "+", second, "+", third)
    return first + second + third

result = add_three(1, 2, 3)
prnt("1+2+3 =", result)

@security_level("user")
def subtract_two(first, second):
    prnt("subtracting ", first, "-", second)
    return first - second

result = subtract_two(3, 2)
prnt("3-2=", result)

prnt("*ripping out an argument in passing")

@security_level("user")
def one():
    prnt("one")

@security_level("user")
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

prnt("==================")
prnt("*Example of relying on a global")
features = ["general", "print", "email", "twitter"]

@dectools.make_call_if
def is_feature_installed(function, args, kwargs, feature="general"):
    global features
    prnt("checking feature", feature)
    if feature in features:
        features.remove(feature)
        return True
    else:
        return False

@is_feature_installed()
def general_stuff():
    prnt("general stuff")
    
general_stuff()
printed("checking feature general", -2)
printed("general stuff")
general_stuff()
printed("checking feature general")

@is_feature_installed("facebook")
def post_to_facebook(account, password):
    prnt("posting now")
    
post_to_facebook("me", "password")
printed("checking feature facebook")
prnt("Now update the global")
features = ["general", "print", "email", "twitter", "facebook"]
post_to_facebook("you", "123")
printed("checking feature facebook", -2)
printed("posting now")

prnt("==================")
prnt("Fun with bad usage")
@is_feature_installed
def forgot_to_use_parens_there():
    pass
    
try:
    forgot_to_use_parens_there()
except TypeError as te:
    prnt(te[0])
    assert "parenthesis" in te[0]
    prnt("At least there is a hint.")
printed("At least there is a hint.")

try:
    @dectools.call_if(is_feature_installed, feature = "facebook")
    def it_is_a_decorator_not_a_mold():
        pass
except AssertionError as ae:
    prnt(ae[0])
    assert "already a decorator" in ae[0]
    prnt("At least there is a hint.")
printed("At least there is a hint.")
    

try:
    @check_security()
    def that_takes_no_parameters():
        pass
except TypeError as te:
    prnt(te[0])
    assert "parenthesis" in te[0]
    prnt("At least there is a hint.")
printed("At least there is a hint.")

try:
    @check_security('f')
    def that_takes_no_parameters():
        pass
except AssertionError as ae:
    prnt(ae[0])
    assert "type" in ae[0]
    prnt("Not a good hint I grant.")
    prnt("At least there is a hint.")
printed("At least there is a hint.")

prnt("All done")
