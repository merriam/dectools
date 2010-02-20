""" Example of old style nested decorator """

def check_me(level):
    print "level was ", level
    return True

def require(level):
    def take_params(function):
        def concrete(*args, **kwargs):
            if check_me(level):
                return function(*args,    **kwargs)
            return None
        return concrete
    return take_params

@require('OK')
def print_hello():
    print "Hello"

print_hello()
