from textblob import TextBlob

#1. Read the contents of a text file. (Choose a file of your choice) .
contents = str()

with open('sampletext.txt') as data:
    contents = data.read()

#i. Display the sentences and words in the paragraph.
print(TextBlob(contents).sentences)
print(F"\n{TextBlob(contents).words}")

#ii. Display the noun phrases in the paragraph.
print(F"\n{TextBlob(contents).noun_phrases}")

#iii. Attempt to correct the spellings of the words.
print(F"\n{TextBlob(contents).correct()}")

#iv. Translate the content into Spanish .
if (TextBlob(contents).detect_language() != 'es'):
    print(F"\n{TextBlob(contents).translate(to='es')}")

#v. Display the parts of speech of the contents of the file.
print(F"\n{TextBlob(contents).tags}")