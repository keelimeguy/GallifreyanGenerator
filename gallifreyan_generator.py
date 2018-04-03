import argparse
import re

class Gallifreyan:
    consonants = ['B', 'J', 'T', 'Th',
                  'Ph', 'Wh', 'Gh',
                  'Ch', 'K', 'Sh', 'Y',
                  'D', 'L', 'R', 'Z',
                  'C', 'Q',
                  'G', 'N', 'V', 'Qu',
                  'H', 'P', 'W', 'X',
                  'F', 'M', 'S', 'Ng']
    vowels = ['A', 'E', 'I', 'O', 'U']
    punctuation = ['.', ',', ';', '?', '!', ':', '\"', '\'', '-']


    class Word:
        def __init__(self, text):
            self._text = text

        def __str__(self):
            return '\"'+self._text+'\"'
        __repr__ = __str__


    def __init__(self, text):
        self._text = text
        self._words = []
        for word in re.compile('('+'|'.join(['\\'+s for s in self.punctuation+[' ', '\n', '\t', '\r']])+')').split(text):
            if word not in [' ', '\n', '\t', '\r', '']:
                self._words.append(self.Word(word))

    def __str__(self):
        return self._text
    __repr__ = __str__

    def words(self):
        return self._words


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert given text into Gallifreyan.')
    parser.add_argument('-t', '--text', default=None,
                        help='The text to convert.')
    args = parser.parse_args()

    if args.text == None:
        print('Try running with -h.')
        exit(0)

    g = Gallifreyan(args.text)
    print(g)
    print(g.words())
