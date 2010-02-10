import dectools
import inspect
import traceback

def _dict_as_called(function, args, kwargs):
    """ return a dict of all the args and kwargs as the keywords they would
    be received in a real function call.  """

    names, args_name, kwargs_name, defaults = inspect.getargspec(function)
    
    # assign basic args
    params = {}
    if args_name:
        basic_arg_count = len(names)
        params.update(zip(names[:], args))  # zip stops at shorter sequence
        params[args_name] = args[basic_arg_count:]
    else:
        params.update(zip(names, args))    
    
    # assign kwargs given
    if kwargs_name:
        params[kwargs_name] = {}
        for kw, value in kwargs.iteritems():
            if kw in names:
                params[kw] = value
            else:
                params[kwargs_name][kw] = value
    else:
        params.update(kwargs)
    
    # assign defaults
    if defaults:
        for pos, value in enumerate(defaults):
            if names[-len(defaults) + pos] not in params:
                params[names[-len(defaults) + pos]] = value
            
    # check we did it correctly.  Each param and only params are set
    assert set(params.iterkeys()) == (set(names)|set([args_name])|set([kwargs_name])
                                      )-set([None])
    
    return params

def pre(function, args, kwargs, expression_string):
    new_locals = _dict_as_called(function, args, kwargs)  # parameters as if called.
    assert eval(expression_string, globals(), new_locals), "Precondition Failed in " + function.__name__ + ": " + expression_string
    return function(*args, **kwargs)

def post(function, args, kwargs, expression_string):
    """ post condition test.  Test must pass even if an exception was thrown in 
    the function. """
    try:
        new_locals = _dict_as_called(function, args, kwargs)  # parameters as if called.
        retval = function(*args, **kwargs)
    except:        
        assert eval(expression_string, globals(), new_locals), ("After Unhandled Exception, " 
                "post-condition failed in " + function.__name__ + "\n" +
                "post-condition expression: " + expression_string + "\n" +
                "exception traceback: " + traceback.format_exc())
        raise
    else:
        assert eval(expression_string, globals(), new_locals), (
                "Post-condition failed in " + function.__name__ + "\n" + 
                "post-condition expression: " + expression_string)
    return retval



prec = dectools.make_call_instead(pre)
postc = dectools.make_call_instead(post)
ok = "self.name and self.price >= 0 and Item.tax_rate >= 0"
class Item(object):
    tax_rate = 0.10
    
    @postc(ok)        
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    @prec(ok)
    #@postc(ok)
    def adjust_price(self, adjustment):
        self.price += adjustment
        
    @postc(ok)
    @prec(ok)
    def get_taxes(self):
        return self.price * Item.tax_rate
    
    
p = Item("Dead Parrot", 1.00)
print "That's a ", p.name, "!"
print "OK.  I'll knock off half a quid."
p.adjust_price(-0.5)
print "So that comes to", p.price , "plus tax of ", p.get_taxes()
print "Right.  Wrap it up."















def add(first, second=2, third=3):
    pass

p = _dict_as_called(add, (1, 2, 3), {})
assert (1, 2, 3) == (p['first'], p['second'], p['third'])
p = _dict_as_called(add, (1,), {})
assert (1, 2, 3) == (p['first'], p['second'], p['third'])
p = _dict_as_called(add, (10,), {'third':30})
assert (10, 2, 30) == (p['first'], p['second'], p['third'])
p = _dict_as_called(add, (10, 20), {})
assert (10, 20, 3) == (p['first'], p['second'], p['third'])
p = _dict_as_called(add, (10, 20), {'third': 30})
assert (10, 20, 30) == (p['first'], p['second'], p['third'])
p = _dict_as_called(add, (10,), {'second': 20})
assert (10, 20, 3) == (p['first'], p['second'], p['third'])

def annoy(first, second=2, third=3, *args, **kwargs):
    pass

p = _dict_as_called(annoy, (1, 2, 3), {})
assert (1, 2, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = _dict_as_called(annoy, (1,), {})
assert (1, 2, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = _dict_as_called(annoy, (10,), {'third':30})
assert (10, 2, 30, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = _dict_as_called(annoy, (10, 20), {})
assert (10, 20, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = _dict_as_called(annoy, (10, 20), {'third': 30})
assert (10, 20, 30, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = _dict_as_called(annoy, (10,), {'second': 20})
assert (10, 20, 3, (), {}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])

p = _dict_as_called(annoy, (1, 2, 3, 4), {'fourth':4})
assert (1, 2, 3, (4,), {'fourth':4}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])
p = _dict_as_called(annoy, (1, 2, 3, 4, '5'), {'fourth':4, 'sixth':6})
assert (1, 2, 3, (4, '5'), {'fourth':4, 'sixth': 6}) == (p['first'], p['second'], p['third'], p['args'], p['kwargs'])

print "OK!"
    
pre(add, (1,2,3), {}, "third == 3")
sixty = 60
pre(add, (1,), {}, "first == 1 and sixty == 60")



@dectools.call_instead(pre, "count >= 0 and count <= 5")
def echo(a,b):
    print a,b
count = 1
echo(1,3)
count = 10
try:
    echo(2,3)
except AssertionError:
    pass
else:
    print "Failed!"    

