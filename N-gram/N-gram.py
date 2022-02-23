import re
from os import path

STOPWORDS = ["a", "an", "and", "as", "at", "for", "from",\
    "in", "into", "of", "on", "or", "the", "to"]

class NonpositiveNGramLengthException(Exception):
    pass

def filtered_read(fname):
    fpath = "\\".join([path.dirname(path.abspath(__file__)), fname])
    contents = open(fpath, "r").read()
    return super_strip(contents)

def super_strip(input_string):
    # Getting rid of capitalization and splitting on word separating symbols.
    lower_strings = re.split("[-'\n ]", input_string.lower())

    output_string = list()
    for word in lower_strings:
        # Removing all non-alphabetic characters from each word
        alpha_word = "".join(symbol for symbol in word if symbol.isalpha())

        # Filtering out short words and stopwords
        if alpha_word not in STOPWORDS and len(alpha_word) >= 2:
            output_string.append(alpha_word)

    return " ".join(output_string)

def get_Ngrams(text, N, startstop=True):
    """Return characterwise n-gram of size N."""

    # Checking inputs
    if not isinstance(N, type(int())):
        raise TypeError("N must be an integer")
    if not isinstance(text, type(str())):
        raise TypeError("First parameter must be a string")
    if N <= 0:
        raise NonpositiveNGramLengthException("N must be positive")

    # Adding end and beginning symbols
    if startstop:
        text = "".join(['[', text, ']'])
    nGrams = dict()
    # Must cut the loop short by N-1 iterations
    for i in range(len(text)-(N-1)):
        seq = text[i:i+N]
        if seq not in nGrams:
            nGrams[seq] = 0
        nGrams[seq] += 1
    # Get sum of vals
    valsum = sum(nGrams.values())
    nGrams  = {k: v/valsum for k, v in nGrams.items()}
    return nGrams

def proba(test_phrase, nGrams):
    """Return the probability of the test phrase existing given learned nGrams"""
    # Getting the length of the first element to pass info of what N is.
    N = len(list(nGrams.keys())[0])
    prob = 1
    for i in range(len(test_phrase) - (N-1)):
        seq = test_phrase[i:i+N]
        prob *= nGrams[seq]
    return prob

def main():
    contents = filtered_read("TheStoryofAnHour-KateChopin.txt")
    test_phrase = 'no one'
    
    # With start and stop markers added
    nGrams = get_Ngrams(contents, 2)
    prob = proba(test_phrase, nGrams)
    rem = int("".join(str(prob)[:4].split('.'))) % 173
    print(f"Remainder with start and stop markers: {rem}")

    # Without start and stop markers
    nGrams = get_Ngrams(contents, 2, startstop=False)
    prob = proba(test_phrase, nGrams)
    rem = int("".join(str(prob)[:4].split('.')))%173
    print(f"Remainder without start and stop markers: {rem}")


if __name__ == "__main__":
    main()