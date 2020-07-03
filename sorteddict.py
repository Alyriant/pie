
foo = ( ('a','X'), ('g','c'), ('Z','w'), ('D','E') )
print("Initial tuple:\n", foo)

bar = [ (y.lower(), x ) for x,y in foo ]
print("Transformed:\n", bar)

# Dict construction order preserved in Python 3.7+
baz = { x:y for x,y in sorted(bar) }
print("Dict comprehension sorted by key:\n", baz)

moo = { x:y for x,y in sorted(bar, key=lambda c : c[1]) }
print("Dict comprehension sorted by value:\n", moo)

moo2 = { x:y for x,y in sorted(bar, key=lambda c : c[1].lower()) }
print("Dict comprehension sorted by value (case insensitive):\n", moo2)



