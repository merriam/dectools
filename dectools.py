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
    # assert that function to be called takes a parameter named "function" or "klass"
    # ends with parameters name "function, *args, **kwargs"
    _assert_function_takes_function_or_klass_parameter(once_function)
    code = once_function.__code__
    if code.co_argcount == 1:
        # call_once has no additional arguments.  It will be used like:
        #    @call_once
        #    def hello(name):  ...
        def decorated_by_once_function(function_hello):
            """  Decorator.  Calls function_once once and then returns 
                 the original function.  That is, no effect except at 
                 the decoration (compile) time. """
            assert callable(function_hello)
            once_function(function_hello)
            return function_hello
        mask(changed=decorated_by_once_function, look_like=once_function)
        return decorated_by_once_function
    else:
        # call_once has extra arguments, e.g., call_once(function, message).  
        # It will be used like:  @call_once("compiling", indention=2)
        # So we need to return a function whose output is a decorator.

        def take_once_function_parameters(*once_args, **once_kwargs):
            def decorated_by_once_function(function_hello):
                """  Decorator.  Calls function_once once and then returns 
                     the original function.  That is, no effect except at 
                     the decoration (compile) time. """
                once_function(function_hello, *once_args, **once_kwargs)
                return function_hello
            return decorated_by_once_function            
        mask(changed=take_once_function_parameters, look_like=once_function)
        return take_once_function_parameters
        
def call_once(once_function, *once_args, **once_kwargs):
    """ This decorator takes arguments of a once_function to call and any additional
        arguments to be passed on to that once function.
        
        @call_once(once_function, "Compiling", indent=3)
        def hello():
            print "Hello"
        
        does the same as
        def hello():
            print "Hello"
        once_function(hello, "Compiling", indent=3)
    """
    # assert that function_once ends with parameters name "function, *args, **kwargs"
    _assert_function_takes_function_or_klass_parameter(once_function)
    def decorator_to_call_once_function(function_hello):
        """  Decorator.  When applied (compile time), it calls function_once once and then returns 
             the original function.  That is, no effect except at 
             the decoration (compile) time. """
        once_function(function_hello, *once_args, **once_kwargs)
        return function_hello
    return decorator_to_call_once_function


def make_call_instead(instead_function):
    """ This decorator creates a new decorator for instead_function.   When the 
    new decorator is used on a hello_function, the instead_function is called 
    instead of the hello_function.  The instead_function is passed the 
    hello_function and its arguments as parameters. """
    raise NotImplemented

def call_instead(instead_function, *instead_args, **instead_kwargs):
    """ This decorator decorates a hello_function so that, when hello_function would
    def call_once(once_function, *once_args, **once_kwargs):
    """
    raise NotImplemented
    
def make_call_before(before_function):
    """ This decorator creates a decorator for before_function.  When the decorator
    is used on a hello_function, the before_function is called, with the 
    hello_function and its arguments passed as parameters, and then
    the hello_function is called.
    """
    raise NotImplemented
    
def make_call_after(after_function):
    """ This decorator creates a decorator for after_function.  When the decorator
    is used on a hello_function, the hello_fuction is called, and then the 
    after_function is called, with the hello_function and its arguments passed 
    as parameters.
    """
    raise NotImplemented


