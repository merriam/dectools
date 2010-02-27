# Testing for this package is 'special' as in a 'special short bus'.
# Most of the tests involve defining and using decorated functions, and
# nested functions do not behave in quite the same way.  This makes it 
# much harder, meaning less intuitive to read, write, and understand.
# It's better to hack all the "test functions" into this file.
#
# To run these tests, if you have the decorator module in your PYTHONPATH,
# you can:
#     1.  $ python test_all.py
#         This does lots of output. 
#     2.  nosetests
#         Lots of dots
#
# To add tests, follow the boilerplate.  I thought of just doing a
# quick generate on the fly, but it's easy to debug a test without 
# the metaprogramming.

import unittest2 as unittest

class Test_by_import(unittest.TestCase):
    def test_call_before(self):
        import test_call_before
    
    def test_call_if2(self):
        import test_call_if2
        
    def test_call_if(self):
        import test_call_if
    
    def test_call_instead(self):
        import test_call_instead
    
    def test_call_once(self):
        import test_call_once
    
    def test_make_call_if(self):
        import test_make_call_if
    
    def test_make_call_instead(self):
        import test_make_call_instead
    
    def test_log(self):
        import test_log
    
    def test_make_call_once(self):
        import test_make_call_once
    
    def test_dict_as_called(self):
        import test_dict_as_called
    
    def test_pre_post(self):
        import test_pre_post
    
    def test_invariants(self):
        import test_invariants

if __name__ == "__main__":
    unittest.main()
    print("All tests done...")
    
