
a = 1

def foo():
    # a has global scope implicitly
    print(a)

def bar():
    # a has local scope because the function assigns to it, but
    # it is used as a local before the assignment so is an error:
    # UnboundLocalError: local variable 'a' referenced before assignment

    # uncomment this to get rid of the exception
    #global a

    print(a)
    a = 2

foo()
bar()

