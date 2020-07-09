
a = 1

def foo():
    # a has global scope
    b = 2
    print(b)
    print(a)

def bar():
    # a has local scope because the function assigns to it, but
    # it is used as a local before the assignment so is an error
    b = 3
    print(b)
    print(a)
    a = 4

foo()
bar()

result = """
2
1
3
Traceback (most recent call last):
  File "D:/GitHub/Alyriant/pie/peculiar_scoping.py", line 16, in <module>
    bar()
  File "D:/GitHub/Alyriant/pie/peculiar_scoping.py", line 12, in bar
    print(a)
UnboundLocalError: local variable 'a' referenced before assignment
"""
