# Welcome to reading this code.  It can be a bit tricky, with lots of function
# returns function of function of function type of stuff.   I have tried to 
# keep names clear and following simple examples.

import types

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
    

def make_call_once(function_once):
    """ This decorator takes a once_function, and returns a decorator that calls
        that once_function once before returning the original object. 
        
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
        
        This is roughly equivalent to:
        >>> def once_function(function):
        ...     print "called once_function while compiling", function.__name__
        ... 
        >>> once_function_decorator = dectools.make_call_once(once_function)
        >>> def hello_function():
        ...     print "hello"
        ... 
        >>> old_hello_function = hello_function
        >>> new_hello_function = once_function_decorator(hello_function)
        called once_function while compiling hello_function
        >>> old_hello_function == new_hello_function
        True
        >>>         
    """
    # assert that function to be called takes a parameter named "function" or "klass"
    # ends with parameters name "function, *args, **kwargs"
    _assert_function_takes_function_or_klass_parameter(function_once)
    code = function_once.__code__
    if code.co_argcount == 1:
        # call_once has no additional arguments.  It will be used like:
        #    @call_once
        #    def hello(name):  ...
        def decorated_by_function_once(function_hello):
            """  Decorator.  Calls function_in once and then returns 
                 the original function.  That is, no effect except at 
                 the decoration (compile) time. """
            assert callable(function_hello)
            function_once(function_hello)
            return function_hello
        return decorated_by_function_once
    else:
        # call_once has extra arguments, e.g., call_once(function, message).  
        # It will be used like:  @call_once("compiling", indention=2)
        # So we need to return a function whose output is a decorator.
        def take_function_once_parameters(*once_args, **once_kwargs):
            def decorated_by_function_once(function_hello):
                """  Decorator.  Calls function_in once and then returns 
                     the original function.  That is, no effect except at 
                     the decoration (compile) time. """
                function_once(function_hello, *once_args, **once_kwargs)
                return function_hello
            return decorated_by_function_once
        return take_function_once_parameters
        
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
    # assert that function_in ends with parameters name "function, *args, **kwargs"
    _assert_function_takes_function_or_klass_parameter(function_once)
    code = function_once.__code__
    def decorator_by_call_once(function_hello):
        """  Decorator.  Calls function_in once and then returns 
             the original function.  That is, no effect except at 
             the decoration (compile) time. """
        function_once(function_hello, *once_args, **once_kwargs)
        return function_hello
    return decorator_by_function_once
