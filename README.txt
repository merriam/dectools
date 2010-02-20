========
DecTools
========

DecTools provides a library of tools for creating Python decorators.  It 
unifies usage between class decorators, decorators requiring arguments,
and simple decorators.  It also provides correct names, doc, and function
signatures for decorated functions.  Typical usage often looks like this::

    @make_call_once
    def register_callback(function):
          gui.callback_create(function.__name__, function)

    @make_call_before
    def require_login(function, args, kwargs, page_name):
         while not current_user_id():
            ...

    @register
    @require_login("Summary of Items")
    def view_summary():
        ...

This release has *@make_call_(once/before/after/instead)*.  It also has 
commonly used decorators in this release, including:

* *@pre*, *@post* for pre and post condition processing

* *@log()* for logging function calls

* *@invariant*, a class decorator, for contract programming

Thanks
======

Thanks to Michele Simionato for exposing utility functions in 
Decorator Decorator and to David Mertz for his excellent IBM
Developer Works article "Charming Python:  Decorators make
magic easy", http://www.ibm.com/developerworks/linux/library/l-cpdecor.html

Contact
=======

You can contact the author, Charles Merriam, at charles.merriam@gmail.com. 
Or visit http://charlesmerriam.com

Other Notes
===========
This is a 'shared experiment' release.

This package depends on "decorator", 3.1.2 or above, http://pypi.python.org/pypi/decorator/3.1.2
