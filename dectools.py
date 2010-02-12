# Welcome to reading this code.  It can be a bit tricky, with lots of function
# returns function of function of function types of stuff.   I have tried to 
# keep names clear and following simple examples.  
# 
# When I wrote this software, it came together like a Russian matryoshka doll.
# I wrote one function, call_once().  When it worked, I wrote a second function,
# looked for repeated code, and rewrote the differenes into another function.
#  
# So a "decorator" is a generic term.  A "concrete decorator" takes one parameter,
# a function, and returns one parameter, the replacement function.  A "decorator 
# mold" is a function follows a pattern in the parameters it takes, and performs 
# some action.  It is usually used by some sort of "stamper", to call it instead.

import types
import decorator
doc_new_warning = "(decorated by dectools.  see __decorators__ and __decorator_chain__)\n"

def _get_history_attributes(changed, model, explanations = None, chain = None):
    """ return tuple of new doc, chain, and explanations taking into account the
        current values in model, and maybe changed. """
    chain = chain or []
    explanations = explanations or []
    old_doc = getattr(model, "__doc__", None) or ""
    
    if hasattr(model, "__decorators__") and hasattr(model, "__decorator_chain__"):
        doc = old_doc
        explanations = model.__decorators__ + explanations
        chain = model.__decorator_chain__ + chain
    else:
        doc =  doc_new_warning + old_doc
        explanations = explanations
        chain = [model] + chain
    return (doc, explanations, chain)

def mimic_only_attributes(changed, model, explanations = None, chain = None):
    """ Make the changed function have the same signature as the model function.
        Add some neat history attributes. Return the changed function. """
    assert type(changed) == type(model)
    (doc, explanations, chain) = _get_history_attributes(changed, model, 
                                                        explanations, chain)
    changed.__name__ = model.__name__
    changed.__doc__ = doc
    changed.__decorators__ = explanations
    changed.__decorator_chain__ = chain
    return changed

def mimic_signature_after_basics(changed, model, explanations, chain, number_of_basic_args):
    """ Make the changed function have the same signature as the model, except
        that the first number_of_basic_args arguments of the model are missing.
        Add some neat history attributes.  Return a new changed function. """
    assert type(changed) == type(model)
    (doc, explanations, chain) = _get_history_attributes(changed, model, 
                                                        explanations, chain)
    f = decorator.FunctionMaker(model, doc=doc)
    args = f.signature.split(", ")
    f.signature = ", ".join(args[number_of_basic_args:])
    source = """
def %(name)s(%(signature)s):
    return f(%(signature)s)"""
    new_func = f.make(source, dict(f=changed), addsource=True, 
                      __decorators__ = explanations, __decorator_chain__ = chain)    
    return new_func

    
def mimic_signature(changed, model, explanations = None, chain = None):
    """ Make the changed function have the same signature as the model function.
        Add some neat history attributes.  Return a new changed function.
    """
    assert type(changed) == type(model)
    (doc, explanations, chain) = _get_history_attributes(changed, model, 
                                                        explanations, chain)
    f = decorator.FunctionMaker(model, doc=doc)
    source = """
def %(name)s(%(signature)s):
    return f(%(signature)s)"""
    new_func = f.make(source, dict(f=changed), addsource=True, 
                      __decorators__ = explanations, __decorator_chain__ = chain)    
    return new_func
    
    
def _assert_function_takes_parameters(a_function, number_of_parameters):
    """ Assert that function's current signature starts with exactly 
        number_of_parameters of (function or klass, args and kwargs.  
    """
    assert a_function.__class__ == types.FunctionType
    code = a_function.__code__
    has_function = code.co_argcount > 0 and code.co_varnames[0] in ("klass", "function")
    has_args = code.co_argcount > 1 and code.co_varnames[1] == "args"
    has_kwargs = code.co_argcount > 2 and code.co_varnames[2] == "kwargs"
    dec_name = "Decorator " + a_function.__name__ + "() parameters "
    if number_of_parameters == 0:
        assert not has_function, dec_name + "should not start with 'function' or 'klass'."
    elif number_of_parameters == 1:
        assert has_function and not has_args and not has_kwargs, \
               dec_name + "should start with 'function' but not 'args' or 'kwargs'."
    elif number_of_parameters == 3:
        if not (has_function and has_args and has_kwargs):
            err_msg = dec_name + "should start with 'function', 'args', and 'kwargs'."
            if hasattr(a_function, "__decorators__"):
                err_msg += "\n%(n)s is already a decorator.  See %(n)s.__decorators__" \
                        % dict(n = a_function.__name__)
            assert False, err_msg
    else:
        assert False, "number_of_parameters makes no sense."

def call_once(once_function, *once_args, **once_kwargs):
    """ This decorator calls once_function after calling the function it decorates.

        When decorating hello_function, this function returns an intermediate 
        function that takes hello_function as its argument, calls once_function
        with hello_function, and the once_function arguments as paraemters, and
        then returns an unchanged hello_function.
        
        @call_once(once_function, "Compiling", indent=3)
        def hello():
            print "Hello"
        
        does the same as
        def hello():
            print "Hello"
        once_function(hello, "Compiling", indent=3)
    """
    # assert that instead_function ends takes a parameter named "function" or "klass",
    # but not the args and kwargs.   
    _assert_function_takes_parameters(once_function, 1)
    def decorator_to_call_once_function(hello_function):
        """  Decorator.  When applied (compile time), it calls once_function once and 
             then returns the original function.  That is, no effect except at 
             the decoration (compile) time. """
        once_function(hello_function, *once_args, **once_kwargs)
        return hello_function
    return decorator_to_call_once_function
    
def call_with_stamper(stamper_function, user_mold, user_args, user_kwargs):
    assert (type(user_args) == types.TupleType and 
            type(user_kwargs) == types.DictType), (
            "Did not receive correct types.  Did you leave off () when using @" + 
            user_mold.__name__ + "()?")
    
    _assert_function_takes_parameters(user_mold, 3)
    # this used to be called did_you_misuse_parenthesis_when_using_your_decorator()
    def did_you_misuse_parenthesis_when_using_your_decorator(hello_function):
        assert callable(hello_function), ("Wrong type.  Did you forget () when using " 
                    + user_mold.__name__ + "()")
        hello_decorated_by_stamper = stamper_function(user_mold, user_args, user_kwargs,
                                        hello_function)
        new_explanation = "decorated by the %s stamper\n  using the %s(%s) mold" % (
            stamper_function.__name__, user_mold.__name__, 
            ", ".join([repr(i) for i in user_args] +
                      [(str(k)+" = "+repr(v)) for k, v in user_kwargs.iteritems()]))
        new_functions = [ stamper_function, user_mold]
        hello_decorated_by_stamper = mimic_signature(hello_decorated_by_stamper, hello_function, 
                                        new_explanation, new_functions)
        return hello_decorated_by_stamper
    did_you_misuse_parenthesis_when_using_your_decorator.__name__ = "stamp_with_" + user_mold.__name__
    did_you_misuse_parenthesis_when_using_your_decorator.__doc__ = ("concrete decorator that stamps a function " + 
            "with " + user_mold.__name__ + " and " + stamper_function.__name__)
    return did_you_misuse_parenthesis_when_using_your_decorator

def call_instead_stamper(user_mold, user_args, user_kwargs, hello_function):
    """ stamper function of call_instead and make_call_instead decorators """
    def hello_decorated_by_stamper(*hello_args, **hello_kwargs):
        ret_val = user_mold(hello_function, hello_args, hello_kwargs,
                                *user_args, **user_kwargs)
        return ret_val
    return hello_decorated_by_stamper

def call_before_stamper(user_mold, user_args, user_kwargs, hello_function):
    def hello_decorated_by_stamper(*hello_args, **hello_kwargs):
        user_mold(hello_function, hello_args, hello_kwargs,
                                *user_args, **user_kwargs)
        ret_val = hello_function(*hello_args, **hello_kwargs)
        return ret_val
    return hello_decorated_by_stamper

def call_after_stamper(user_mold, user_args, user_kwargs, hello_function):
    def hello_decorated_by_stamper(*hello_args, **hello_kwargs):
        ret_val = hello_function(*hello_args, **hello_kwargs)
        user_mold(hello_function, hello_args, hello_kwargs,
                                *user_args, **user_kwargs)
        return ret_val
    return hello_decorated_by_stamper

def call_if_stamper(user_mold, user_args, user_kwargs, hello_function):
    def hello_decorated_by_stamper(*hello_args, **hello_kwargs):
        if user_mold(hello_function, hello_args, hello_kwargs,
                                *user_args, **user_kwargs):
            ret_val = hello_function(*hello_args, **hello_kwargs)
        else:
            ret_val = None
        return ret_val
    return hello_decorated_by_stamper

def call_instead(user_mold, *user_args, **user_kwargs):
    return call_with_stamper(call_instead_stamper, user_mold, user_args, user_kwargs)

def call_before(user_mold, *user_args, **user_kwargs):
    return call_with_stamper(call_before_stamper, user_mold, user_args, user_kwargs)

def call_after(user_mold, *user_args, **user_kwargs):
    return call_with_stamper(call_after_stamper, user_mold, user_args, user_kwargs)

def call_if(user_mold, *user_args, **user_kwargs):
    return call_with_stamper(call_if_stamper, user_mold, user_args, user_kwargs)

def stamp_into_decorator(stamper, user_mold, number_of_basic_args = 3):
    """ 
    This factory a stamper and user_mold and returns 
    a new decorator that wraps the user_mold in the functionality
    of the stamper.  This returned_function may be a concrete decorator or not.
    
    The user_mold, not meant to be a concrete decorator, takes some number 
    of basic arguments in (function, args, kwargs) and maybe more.  If it takes
    only the basic arguments, a concrete decorator is returned that is used like
    "@user_mold".  If it takes more, an intermediate function is returned so
    that it can be used like "@user_mold(user_param1)".  The intermediate 
    function then returns a concrete decorator.  
    
    When this new decorator is used to decorate a hello_function, the 
    function returned by the stamper is returned instead.                
   
    user_mold = a function that will be used as a decorator.
    """
    
    # check inputs.  Helps catch misuse.
    assert number_of_basic_args in (0, 1, 3)
    assert type(stamper) in (types.ClassType, types.FunctionType) 
    assert type(user_mold) in (types.ClassType, types.FunctionType)
    _assert_function_takes_parameters(user_mold, number_of_basic_args)
    
    additional_arguments = user_mold.__code__.co_argcount > number_of_basic_args
    if not additional_arguments:
        # user_mold has no additional arguments.  It will be used like:
        #    @user_mold
        #    def hello(name):  ...
        # so the returned_function:
        #     1.  Is a concrete decorator (function in, function out), which is not
        #         the signature of user_mold or stamper.
        #     2.  Directs the stamper to call the user_mold function appropriately
        #         when used as decorator.
        #     3.  Has the __name__, __doc__ 
        returned_function = stamper(user_mold) 
            # args and kwargs are optional when calling stamper
            
        explanations = ["decorator mold " + user_mold.__name__ + " was stamped\n" +
                        "by " + stamper.__name__ + " and is now a concrete decorator."]
        chain = [user_mold, stamper]
        returned_function = mimic_only_attributes(returned_function, user_mold, 
                                                  explanations, chain)
        return returned_function
    else:
        # user_mold has extra arguments, so
        # it will be used like:  @print_message("compiling", indention=2)
        # In this case, the returned_function is called to get the 
        # concrete decorator. 
        def returned_function(*user_args, **user_kwargs):
            return stamper(user_mold, *user_args, **user_kwargs)
        explanations = ["decorator mold " + user_mold.__name__ + " was stamped\n" +
                        "by " + stamper.__name__ + " and is now a function\n"
                        "that returns a concrete decorator."]
        chain = [user_mold, stamper]
        returned_function = mimic_signature_after_basics(returned_function, 
                    user_mold, explanations, chain, number_of_basic_args)
        return returned_function


def make_call_once(once_function):
    return stamp_into_decorator(call_once, once_function, number_of_basic_args=1)

def make_call_instead(instead_function):
    return stamp_into_decorator(call_instead, instead_function)
        
def make_call_before(before_function):
    return stamp_into_decorator(call_before, before_function)

def make_call_after(after_function):
    return stamp_into_decorator(call_after, after_function)

def make_call_if(if_function):
    return stamp_into_decorator(call_if, if_function)

def general_logging_function(function, args, kwargs, before_string_function , after_string_function):
    # TODO add a log_output parameter, which acts like a file handler, or takes a string
    before_string = function.__name__ + ": called with args:" + str(args) + str(kwargs)
    print before_string
    try:
        ret_val = function(*args, **kwargs)
    except:
        import sys
        after_string = function.__name__ + ": Exception: " + str(sys.exc_info())
        print after_string
        raise
    else:
        after_string = function.__name__ + ": returned value:" + str(ret_val)
        print after_string
        return ret_val



@make_call_instead
def log_verbose(function, args, kwargs, output_function = None):
    """ Log call, arguments, and return value or exception to a output_function 
    that takes a string, or to stdout if no output_function is provided.  """

    # prnt = a function to print
    def p(string):
        """ Just a print function """
        print string
    prnt = output_function if output_function else p

    before_string = ">" + function.__name__ + " called with args:" + str(args) + str(kwargs)
    prnt(before_string)

    try:
        ret_val = function(*args, **kwargs)
    except:
        import sys
        after_string = "!" + function.__name__ + " exception: " + str(sys.exc_info())
        prnt(after_string)
        raise
    else:
        after_string = "<" + function.__name__ + " returned value:" + str(ret_val)
        prnt(after_string)
        return ret_val
        