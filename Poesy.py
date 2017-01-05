import random
import pronouncing

# Create reverse N-grams from a list of tokens
def reverseNgrams(tokens, n):
    ngrams = []
    for i in range(len(tokens)-1, 0+n-2, -1):
        ngram = []
        for j in range(i, i-n, -1):
            ngram.append(tokens[j])
        ngrams.append(ngram)
    return ngrams

# Organize N-grams in a frequency lookup table (N-layer nested dictionaries)
def setupModel(ngrams):
    lookup = {}
    n = len(ngrams[0])
    for ngram in ngrams:
        ptr = lookup
        for i in range(0, n):
            if i == n-1:
                ptr.setdefault(ngram[i], 0)
                ptr[ngram[i]] += 1
            else:
                try: ptr = ptr[ngram[i]]
                except KeyError: 
                    ptr.setdefault(ngram[i], {})
                    ptr = ptr[ngram[i]]
    return lookup

# Loads all first words into an array for efficiency
def getFirstWords(corpus):
    firstWords = []
    for first in corpus:
        firstWords.append(first)
    return firstWords

# Randomly chooses a word from the corpus
def findFirst(corpus, firstWords):
    pick = random.randrange(0, len(firstWords)-1)
    return firstWords[pick]

# Randomly chooses a second word from the corpus based on the first 
def findSecond(first, corpus, firstWords):
    words = []
    try:
        for second in corpus[first]:
            words.append(second)
    except KeyError:
        return findFirst(corpus, firstWords)
        
    if len(words) == 0: return findFirst(corpus, firstWords)
    elif len(words) == 1: return words[0]
    
    pick = random.randrange(0, len(words)-1, 1)
    return words[pick]
   
# Randomly chooses a third word from the corpus based on the first and second    
def findThird(first, second, corpus, firstWords):
    words = []
    try: 
        for third in corpus[first][second]:
            words.append(third)
    except KeyError:
        return findSecond(first, corpus, firstWords)
            
    if len(words) == 0: return findSecond(first, corpus, firstWords)
    elif len(words) == 1: return words[0]
    
    pick = random.randrange(0, len(words)-1)
    return words[pick]

# Builds sentences word by word
def addWord(sentence, first, second, corpus, firstWords):
    third = findThird(first, second, corpus, firstWords)
    sentence.append(third)
    first, second = second, third
    return first, second

# Randomly chooses a rhyming word from the corpus
def findRhyme(word, corpus):
    rhymes = pronouncing.rhymes(word)
    while (True):
        if len(rhymes) == 0:
            return None
      
        elif len(rhymes) == 1:
            try:
                corpus[rhymes[0]]
                return rhymes[0]
            except KeyError:
                return None        
        
        else:
            pick = random.randrange(0, len(rhymes)-1)
            try:
                corpus[rhymes[pick]]
                return rhymes[pick]
            except KeyError:
                rhymes.remove(rhymes[pick])
                continue

# Implementation of a couplet - AABB CCDD EEFF GGHH
def generateCouplet(corpus, lines, wordsPerLine):
    firstWords = getFirstWords(corpus)
    poem = []   
    for i in xrange(lines):            
        line = []  
        if i % 2 == 0:
            while (True):
                A = findFirst(corpus, firstWords)
                AA = findRhyme(A, corpus)                
                if AA != None:
                    break 
    
            first = A
            second = findSecond(first, corpus, firstWords)
            line += [first, second]
        
        if i % 2 == 1:
            first = AA
            second = findSecond(first, corpus, firstWords)
            line += [first, second]
        
        for j in xrange(wordsPerLine-2):
            first, second = addWord(line, first, second, corpus, firstWords)
        
        poem.append(line[::-1])
    return poem
 
# Handles capitalization lost from pre-processing
def poemProcessing(poem):
    for line in poem:
        line[0] = line[0][0].upper()+line[0][1:]
        for index, word in enumerate(line):
            if word[0:2] == "i'":
                line[index] = word[0:2].upper()+word[2:]
            if word == 'i':
                line[index] = word.upper()

# Prints poem line by line
def printPoem(poem):
    for line in poem:
        for word in line:
            print word,
        print