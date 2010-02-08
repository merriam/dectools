# from functools import wraps

class call_if(object):
    def __init__(self, test_function):
        self.test_function = test_function

    def __call__(self, decorated):
        # @wraps(decorated)
        def wrapped_by_call_if(*args, **kwargs):
            return decorated(*args, **kwargs) if self.test_function() \
                   else False
        return wrapped_by_call_if

class call_before(object):
    """ Decorator like '@call_before(my_before_function)' """
    def __init__(self, before_function):
        self.before_function = before_function
    
    def __call__(self, decorated):
        # @wraps(decorated)
        def wrapped_by_call_before(*args, **kwargs):
            self.before_function()
            return decorated(*args, **kwargs)
        return wrapped_by_call_before




# Decorator Toolkit

# define __all__

# call/pass  once/if/before/after

# debug/trace/log

# 

print("Hello")