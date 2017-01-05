<p align="center"><img src="https://raw.githubusercontent.com/anfederico/Poesy/master/media/Poesy.png" width=250px><p>

<p align="center">
<i>
Carefully as he pulled up a little kingdom I possess<br>
As long as he spoke he heard cries of distress<br>
A most beautiful thing about it is what I supposed<br>
The little trundle bed boat went sailing through the closed<br>
The kind moon made a thing he thought very fast<br>
Marvellous white cloud rising from the village they rolled past<br>
Fields to see yes tiny green leaves a whole pot<br>
His people famous for victory and happiness he had got<br>
</i>
</p>

## Code Examples

#### Modeling a Corpus with Reverse N-grams

```python
from Poesy import reverseNgrams, setupModel
import json

# The input is simply a list of tokens or words from your text
# Tokens should be in order of appearance and collected per sentence
# Ideally, these will be tokens that have already been processed
# To lowercase, strip punctuation, remove numbers etc.
# I leave processing to the user because each text has specific needs 
sentence = ['w1','w2','w3','w4','w5','w6','w7','w8','w9']

# As you can see, you're generating "reverse" N-grams
# We can then build strings of words from the end, rather than the beginning
# This property is useful when you want to build sentences that rhyme
ngrams = reverseNgrams(sentence, 3)
for ngram in ngrams:
    print ngram
```

```text
['w9', 'w8', 'w7']
['w8', 'w7', 'w6']
['w7', 'w6', 'w5']
['w6', 'w5', 'w4']
['w5', 'w4', 'w3']
['w4', 'w3', 'w2']
['w3', 'w2', 'w1']
```

```python
# Organize N-grams in a frequency lookup table (N-layer nested dictionaries)
model = setupModel(ngrams)
for row in model:
    print row, model[row]
```

```text
w7 {'w6': {'w5': 1}}
w6 {'w5': {'w4': 1}}
w5 {'w4': {'w3': 1}}
w4 {'w3': {'w2': 1}}
w3 {'w2': {'w1': 1}}
w9 {'w8': {'w7': 1}}
w8 {'w7': {'w6': 1}}
```

```python
# Export the model to json so we can load it quickly later    
with open('example.json', 'w') as outfile:
    json.dump(model, outfile)
```

#### Generating a Poem
```python
from Poesy import reverseNgrams, setupModel
from nltk.corpus import gutenberg
import json

# In this example I'm using a corpus from NLTK - Gutenburg Project
# Sara Bryant - Stories to Tell to Children
sentences = gutenberg.sents('bryant-stories.txt') 

# Process text and collect reverse N-grams sentence by sentence
# Do not do this word by word or you'll have incoherent N-grams that span sentences
ngrams = []
for sentence in sentences:
    tokens = processText(sentence)
    ngrams += reverseNgrams(tokens, 3)

model = setupModel(ngrams)

with open('bryant-stories.json', 'w') as outfile:
    json.dump(model, outfile)

```

```python
from Poesy import generateCouplet, poemProcessing, printPoem
import json

with open('bryant-stories.json', 'r') as infile:    
    corpus = json.load(infile)
  
# This will generate a couplet - AABB CCDD EEFF GGHH
# With 8 lines, 10 words each line
poem = generateCouplet(corpus, 8, 10)

# Handles capitilization and formatting
poemProcessing(poem) 

# Short function to print to console
printPoem(poem)
```

#### Some Samples of Text and Style
##### Sara Bryant - Stories to Tell to Children
```text
Not been from himself at all were the very midst
Her fingers moved the bright needles but her father kissed
There in that house is poisoned at the beautiful city
The worst to bear was the cruelty of the pretty
An honest way to carry light the way many died
He had cleverly touched the prince's portrait by my side
Field mouse hurried as fast as she used to climb
A strange gentleman with his two little riddles in rhyme
```
##### John Milton - Paradise Lost
```
Utmost force and join him named almighty to thy deserted
Of all past ages to the waist and round skirted
Love the sole command sole daughter of god with cedars
Might be admired and each band the heads and leaders
Lull seafaring men o'erwatched whose bark by chance hath spied
Low and ignorant his worshippers dagon his name and sighed
Perhaps designing or exhorting glorious war caught in a trance
Awe whom yet with jealous leer malign eyed them askance
```
##### Herman Melville - Moby Dick
```
Many feet after emerging from the deck by some enchanter's
Length his spade he thrust both hands over the banners
Though he then paused to gaze over on their hones
Gun a straight line not a voyage in such tones
Repeated in this volume but the third day to desist
Over with large whiskers and all of a thick mist
From the breezy billows to windward like two rolling husks
Eagerness betrayed him whichever was true the white ivory tusks
```
