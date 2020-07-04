# Find the most common words in the names of the unicode characters,
# and also print out every character that has the word 'ARROW' in the name

import unicodedata
import collections 

named = { unicodedata.name(chr(i))
          for i in range(0xFFFF)
          if unicodedata.name(chr(i),'') }

counter = collections.Counter()
for name in named:
    counter.update(name.split())

print(counter.most_common(150))

arrows = ['{0} 0x{1:4X} {2}'.format(chr(i), i, unicodedata.name(chr(i),''))
    for i in range(0xFFFF)
    if unicodedata.name(chr(i),'').split().__contains__('ARROW') ]
              
for arrow in arrows:
    print(arrow)
    
