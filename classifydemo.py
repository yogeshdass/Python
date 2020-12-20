from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

trainingSet = [ ('Akbar ruled frm Fatehpur Sikri', 'History'),
                ('Light is a form of energy', 'Physics'),
                ('taj mahal was build by emperor', 'History'),
                ('Sound is another form of enrgy', 'Physics')
]
sentence = "There is a branch of science which studies nature, matter and energy"

print(NaiveBayesClassifier(trainingSet).classify(sentence))