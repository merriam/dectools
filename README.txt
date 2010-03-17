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

You can find manuals in docs/index.html. 
