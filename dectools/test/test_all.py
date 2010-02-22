# Testing for this package is 'special' as in a 'special short bus'.
# Most of the tests involve defining and using decorated functions, and
# nested functions do not behave in quite the same way.  This makes it 
# much harder, meaning less intuitive to read, write, and understand.
# It's better to hack all the "test functions" into this file.
#
# To run these tests, if you have the decorator module in your PYTHONPATH,
# you can:
#     1.  $ python test_all.py
#         This does lots of output, stops on first error.  "All tests done" 
#         is last line on success.
#     2.  nosetests
#         Lots of dots
#
# To add tests, follow the boilerplate.  I thought of just doing a
# quick generate on the fly, but it's better to avoid the metaprogramming.


def test_call_before():
    import test_call_before

def test_call_if():
    import test_call_if2
    
def test_call_if():
    import test_call_if

def test_call_instead():
    import test_call_instead

def test_call_once():
    import test_call_once

def test_make_call_if():
    import test_make_call_if

def test_make_call_instead():
    import test_make_call_instead

def test_log():
    import test_log

def test_make_call_once():
    import test_make_call_once

def test_dict_as_called():
    import test_dict_as_called

def test_pre_post():
    import test_pre_post

def test_invariants():
    import test_invariants

if __name__ == "__main__":
    tests = [func for name, func in locals().items() if name.startswith("test_")]
    for test in tests:
        test()
    print "All tests done..."
    