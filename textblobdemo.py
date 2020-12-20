#python -m textblob.download_corpora
#python3 -m nltk.downloader punkt
#python3 -m nltk.downloader averaged_perceptron_tagger
from nltk.util import pr
from textblob import TextBlob

sentence = TextBlob("This is a sample sentence")
#print(sentence.words)

s1 = "The boy is running. The boys stopped to watch the bear."
tSentence = TextBlob(s1)
#print(type(tSentence.tags[0]))

lemmaSet = set()
for word, pos in tSentence.tags:
    if pos.startswith("NN"):
        lemmitizedWord = word.lemmatize()
        #print(F"{word} : {pos}")
        print(lemmitizedWord)
        lemmaSet.add(lemmitizedWord)
print(lemmaSet)