if __name__ == "__main__":
    sentence = input("Enter the sentence : ")
    counts = dict()
    for word in sentence.split():
        if word in counts.keys():
            counts[word] += 1
        else:
            counts[word] = 1
    print(counts)