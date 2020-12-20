def is_palindrome(word):
    if word == word[::-1]:
        return True
    else:
        return False

if __name__ == "__main__":
    sentence = input("Enter the sentence : ")
    counter = 0
    palindrome_words_count = 0
    while len(sentence.split())>counter:
        if is_palindrome(sentence.split()[counter]):
            palindrome_words_count +=1
        counter +=1
    print(F"Total palindrome words are : {palindrome_words_count}")

