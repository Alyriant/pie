import collections
import random

Card = collections.namedtuple('Card',['set','rank','name'])

class TarotDeck:
    minorArcanaSuites = 'Wands Pentacles Cups Swords'.split()
    
    minorArcanaRanks = ['Ace'] + [str(n) for n in range(2,11)
                       ] + ['Page', 'Knight', 'Queen', 'King']
                                  
    majorArcana =   (('0', 'The Fool'),  
                    ('I', 'The Magician'), 
                    ('II', 'The High Priestess'), 
                    ('III', 'The Empress'), 
                    ('IV', 'The Emperor'), 
                    ('V', 'The Hierophant'), 
                    ('VI', 'The Lovers'), 
                    ('VII', 'The Chariot'), 
                    ('VIII', 'Strength'), 
                    ('IX', 'The Hermit'), 
                    ('X', 'Wheel of Fortune'), 
                    ('XI', 'Justice'), 
                    ('XII', 'The Hanged Man'), 
                    ('XIII', 'Death'), 
                    ('XIV', 'Temperance'), 
                    ('XV', 'The Devil'), 
                    ('XVI', 'The Tower'), 
                    ('XVII', 'The Star'), 
                    ('XVIII', 'The Moon'), 
                    ('XIX', 'The Sun'), 
                    ('XX', 'Judgement'), 
                    ('XXI', 'The World'))

    def __init__(self):
        self._cards = [Card('Trumps', rank, name) 
                        for (rank, name) in self.majorArcana
                      ] + [Card('Minor', rank, name)
                        for name in self.minorArcanaSuites
                        for rank in self.minorArcanaRanks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


def main():
    deck = TarotDeck()
    print(len(deck), " cards in deck")
    spread = random.sample(list(deck), 10)
    for card in spread:
        print(card)

if __name__ == '__main__':
    main()
                                
