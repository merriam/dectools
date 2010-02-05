# Welcome to reading this code.  It can be a bit tricky, with lots of function
# returns function of function of function type of stuff.   I have tried to 
# keep names clear and following simple examples.

import types

def mask(changed, look_like):
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
    

def make_call_once(once_function):
    """ This decorator takes a once_function and returns a new decorator.  When this
        new decorator is used to decorate a hello_functIon, the once_function is 
        called once when the decorator is compiled, i.e., at compile time.   The
        once_function is passed the hello_function as a paramter.   The 
        hello_function is unchanged.

        >>> import dectools
        >>> @dectools.make_call_once
        ... def once_function(function):
        ...     print "called once_function while compiling", function.__name__
        ... 
        >>> @once_function
        ... def hello_function():
        ...     print "hello"
        ... 
        called once_function while compiling hello_function
        >>> hello_function()
        hello        
        
        This has the same effect as:
        >>> def once_function(function):
        ...     print "called once_function while compiling", function.__name__
        ... 
        >>> def hello_function():
        ...     print "hello"
        ...
        >>> once_function(hello_function)
        called once_function while compiling hello_function
        >>> hello_function()
        hello        
        
    """
    code = once_function.__code__
    if code.co_argcount == 1:
        # call_once has no additional arguments.  It will be used like:
        #    @call_once
        #    def hello(name):  ...
        # so we return the actual decorator.
        decorated_by_once_function = call_once(once_function)
        mask(changed=decorated_by_once_function, look_like=once_function)
        return decorated_by_once_function
    else:
        # The once_function has extra arguments, so
        # it will be used like:  @call_once("compiling", indention=2)
        # Which means call_once() is a function whose output the real decorator.
        # So we need to return an intermediate function whose output is a decorator.

        def take_once_function_parameters(*once_args, **once_kwargs):
            decorated_by_once_function = call_once(
                once_function, *once_args, **once_kwargs)
            return decorated_by_once_function
            
        mask(changed=take_once_function_parameters, look_like=once_function)
        return take_once_function_parameters
        
def call_once(once_function, *once_args, **once_kwargs):
    """ This decorator calls once_function before calling the function it decorates.

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


def make_call_instead(instead_function):
    """ This decorator creates a new decorator for instead_function.   When the 
    new decorator is used on a hello_function, the instead_function is called 
    instead of the hello_function.  The instead_function is passed the 
    hello_function and its arguments as parameters. """
    code = instead_function.__code__
    if code.co_argcount == 1:
        # call_once has no additional arguments.  It will be used like:
        #    @call_once
        #    def hello(name):  ...
        # so we return the actual decorator.
        decorated_by_instead_function = call_instead(instead_function)
        mask(changed=decorated_by_instead_function, look_like=instead_function)
        return decorated_by_instead_function
    else:
        # The instead_function has extra arguments, so
        # it will be used like:  @call_once("compiling", indention=2)
        # Which means call_once() is a function whose output the real decorator.
        # So we need to return an intermediate function whose output is a decorator.

        def take_instead_function_parameters(*instead_args, **instead_kwargs):
            # assert not ( len(instead_args) == 1 and len(instead_kwargs) == 0
            #    and type(instead_args[0]) == types.FunctionType),\
            #    "You made a decorator with arguments but called it without arguments"
            # Unfortunately, I can't use this assert.  
            decorated_by_instead_function = call_instead(
                instead_function, *instead_args, **instead_kwargs)
            return decorated_by_instead_function
            
        mask(changed=take_instead_function_parameters, look_like=instead_function)
        return take_instead_function_parameters
    

    
def call_instead(instead_function, *instead_args, **instead_kwargs):
    """ This decorator decorates a hello_function so that, when hello_function would
    be called, the instead_function is called instead.  The instead_function is 
    passed the hello_function and its arguments as paraemters.
    
    This function returns an intermediate function which returns the final 
    hello_function replacement.
    """
    _assert_function_takes_function_and_arg_parameters(instead_function)
    def intermediate_call_instead_function(hello_function):
        """  Decorator.  Returns a new hello_function that calls instead_function
             instead.
             
             If you got a "TypeError: intermediate_call_instead_function() takes..."
             error, you may have made a decorator with arguments, and called it without
             arguments.  For example:
             
             @dectools.make_call_instead
             def trace(function, args, kwargs, indent):  ...
             @trace
             def add_two(first, second):..
             add_two(1,2)
             TypeError: intermediate_call_instead_function() takes exactly 1 argument (2 given)

        """
        def hello_decorated_by_call_instead(*hello_args, **hello_kwargs):
            """ Call the instead function. """
            return instead_function(hello_function, hello_args, hello_kwargs,
                                    *instead_args, **instead_kwargs)
        new_hello_function = mask(changed=hello_decorated_by_call_instead, 
                                  look_like=hello_function)
        return new_hello_function
    return intermediate_call_instead_function



        
def make_call_before(before_function):
    """ This decorator creates a decorator for before_function.  When the decorator
    is used on a hello_function, the before_function is called, with the 
    hello_function and its arguments passed as parameters, and then
    the hello_function is called.
    """
    raise NotImplementedError
    
def make_call_after(after_function):
    """ This decorator creates a decorator for after_function.  When the decorator
    is used on a hello_function, the hello_fuction is called, and then the 
    after_function is called, with the hello_function and its arguments passed 
    as parameters.
    """
    raise NotImplementedError


