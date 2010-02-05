def call_instead2(instead_function, *instead_args, **instead_kwargs):
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
docs =     """ This decorator creates a decorator for before_function.  When the decorator
    is used on a hello_function, the before_function is called, with the 
    hello_function and its arguments passed as parameters, and then
    the hello_function is called.
    """
    """ This decorator creates a decorator for after_function.  When the decorator
    is used on a hello_function, the hello_fuction is called, and then the 
    after_function is called, with the hello_function and its arguments passed 
    as parameters.
    """
    """ This decorator creates a new decorator for instead_function.   When the 
    new decorator is used on a hello_function, the instead_function is called 
    instead of the hello_function.  The instead_function is passed the 
    hello_function and its arguments as parameters. """
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

