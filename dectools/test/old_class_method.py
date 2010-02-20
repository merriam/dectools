""" This is included as model of the old-style of creating decorators """

def check_me(level):
    print "You seem like level", level
    return True

class require(object):
    def __init__(self, level):
        self.level = level
        
    def decorated_by_require(self, *args, **kwargs):
        if check_me(self.level):
            return self.function(*args, **kwargs)
        return None
    
    def __call__(self, function):
        self.function = function
        return self.decorated_by_require
    

@require('manager')
def update_price(new_price):
    print "Setting new price to ", new_price
    
update_price(2)