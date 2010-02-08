# Welcome to reading this code.  It can be a bit tricky, with lots of function
# returns function of function of function type of stuff.   I have tried to 
# keep names clear and following simple examples.

import types

class _Sentinal_Parameter: 
    pass
# A handy parameter passed internally to keep down accidental misuse
# TODO:  see if I can figure out how to use this to keep down accidents in usage

def mimic(changed, look_like):
    """ Make the changed function have the same name as the look_like function.
    TODO:  copy over the signature, defaults, etc.
    TODO:  describe and test log of decorator changes.
    """
    assert type(changed) == type(look_like)
    
    changed.__name__ = look_like.__name__
    
    if not hasattr(changed, "__decorators__"):
        changed.__decorators__ = [look_like]
    changed.__decorators__.append(changed)        
    
    return changed
    
    


def _assert_function_takes_function_and_arg_parameters(a_function):
    """ assert that a function's first parameters are "function", "args", and "kwargs"
    """
    assert a_function.__class__ == types.FunctionType
    code = a_function.__code__
    assert ( code.co_argcount >= 3 and 
             code.co_varnames[0:3] == ("function", "args", "kwargs")
           ), "New decorator must start with parameters function, args, and kwargs."
    

def _assert_function_takes_function_or_klass_parameter(a_function):
    """ assert that a function takes a parameter named "function" 
        or "klass", but does not take *args, **kwargs like others in this toolkit. 
    """
    assert a_function.__class__ == types.FunctionType
    code = a_function.__code__
    assert ( code.co_argcount >= 1 and code.co_varnames[0] in ("function", "klass") 
             and (code.co_argcount == 1 or code.co_varnames[1] != "args")
           ), "New decorator must start with parameter function or klass, but not " \
              "parameters args or kwargs."

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
    _assert_function_takes_function_or_klass_parameter(once_function)
    def decorator_to_call_once_function(hello_function):
        """  Decorator.  When applied (compile time), it calls once_function once and 
             then returns the original function.  That is, no effect except at 
             the decoration (compile) time. """
        once_function(hello_function, *once_args, **once_kwargs)
        return hello_function
    return decorator_to_call_once_function
    
def call_with_core(core_function, user_function, user_args, user_kwargs):
    _assert_function_takes_function_and_arg_parameters(user_function)
    def intermediate_call_user_function(hello_function):
        hello_decorated_by_core = core_function(user_function, user_args, user_kwargs,
                                        hello_function)
        new_hello_function = mimic(changed=hello_decorated_by_core, 
                                  look_like=hello_function)
        return new_hello_function
    intermediate_call_user_function.__doc__ = ("Intermediate function of " 
            + user_function.__name__ + " being decorated by a " 
            + core_function.__name__ + " core.")
    return intermediate_call_user_function

def call_instead_core(user_function, user_args, user_kwargs, hello_function):
    """ Core function of call_instead and make_call_instead decorators """
    def hello_decorated_by_core(*hello_args, **hello_kwargs):
        ret_val = user_function(hello_function, hello_args, hello_kwargs,
                                *user_args, **user_kwargs)
        return ret_val
    return hello_decorated_by_core

def call_before_core(user_function, user_args, user_kwargs, hello_function):
    def hello_decorated_by_core(*hello_args, **hello_kwargs):
        user_function(hello_function, hello_args, hello_kwargs,
                                *user_args, **user_kwargs)
        ret_val = hello_function(*hello_args, **hello_kwargs)
        return ret_val
    return hello_decorated_by_core

def call_after_core(user_function, user_args, user_kwargs, hello_function):
    def hello_decorated_by_core(*hello_args, **hello_kwargs):
        ret_val = hello_function(*hello_args, **hello_kwargs)
        user_function(hello_function, hello_args, hello_kwargs,
                                *user_args, **user_kwargs)
        return ret_val
    return hello_decorated_by_core

def call_if_core(user_function, user_args, user_kwargs, hello_function):
    def hello_decorated_by_core(*hello_args, **hello_kwargs):
        if user_function(hello_function, hello_args, hello_kwargs,
                                *user_args, **user_kwargs):
            ret_val = hello_function(*hello_args, **hello_kwargs)
        else:
            ret_val = None
        return ret_val
    return hello_decorated_by_core

def call_instead(user_function, *user_args, **user_kwargs):
    return call_with_core(call_instead_core, user_function, user_args, user_kwargs)

def call_before(user_function, *user_args, **user_kwargs):
    return call_with_core(call_before_core, user_function, user_args, user_kwargs)

def call_after(user_function, *user_args, **user_kwargs):
    return call_with_core(call_after_core, user_function, user_args, user_kwargs)

def call_if(user_function, *user_args, **user_kwargs):
    return call_with_core(call_if_core, user_function, user_args, user_kwargs)

def make_into_decorator(decorator_function, user_function, number_of_basic_args = 3):
    """ This decorator takes a user_function and returns a new dectorator.  When this
        new decorator is used to decorate a hello_function, the function returned
        by the decorator_function is returned instead.        
    """
    code = user_function.__code__
    if code.co_argcount == number_of_basic_args:
        # user_function has no additional arguments.  It will be used like:
        #    @user_function
        #    def hello(name):  ...
        # so we return the actual decorator.
        user_function_decorated = decorator_function(user_function)
        mimic(changed=user_function_decorated, look_like=user_function)
        return user_function_decorated
    else:
        # user_function has extra arguments, so
        # it will be used like:  @user_function("compiling", indention=2)
        # Which means the user_function is a function that returns the final decorator.
        # This function returns that user_function which the final decorator.
        
        def intermediate_to_take_user_function_parameters(*user_args, **user_kwargs):
            user_function_decorated = decorator_function(
                user_function, *user_args, **user_kwargs)
            return user_function_decorated
            
        mimic(changed=intermediate_to_take_user_function_parameters, look_like=user_function)
        return intermediate_to_take_user_function_parameters


def make_call_once(once_function):
    return make_into_decorator(call_once, once_function, number_of_basic_args=1)

def make_call_instead(instead_function):
    return make_into_decorator(call_instead, instead_function)
        
def make_call_before(before_function):
    return make_into_decorator(call_before, before_function)

def make_call_after(after_function):
    return make_into_decorator(call_after, after_function)

def make_call_if(if_function):
    return make_into_decorator(call_if, if_function)

def log_in_two_steps(function, args, kwargs, before_string_function, after_string_function):
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
def log_verbose(function, args, kwargs):
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
    
    