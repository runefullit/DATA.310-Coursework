import re
from os import path

STOPWORDS = ["a", "an", "and", "as", "at", "for", "from",\
    "in", "into", "of", "on", "or", "the", "to"]

class NonpositiveNGramLengthException(Exception):
    pass

def filtered_read(fname):
    fpath = "/".join([path.dirname(path.abspath(__file__)), fname])
    contents = open(fpath, "r").read()
    return super_strip(contents)

def super_strip(input_string):
    # Getting rid of capitalization and splitting on word separating symbols.
    lower_strings = re.split("[-'\n ]", input_string.lower())

    words = list()
    for word in lower_strings:
        # Removing all non-alphabetic characters from each word
        alpha_word = "".join(symbol for symbol in word if symbol.isalpha())

        # Filtering out short words and stopwords
        if alpha_word not in STOPWORDS and len(alpha_word) >= 2:
            words.append(alpha_word)

    return words

# def get_Ngrams(text, N, startstop=True):
#     """Return characterwise n-gram of size N."""

#     # Checking inputs
#     if not isinstance(N, type(int())):
#         raise TypeError("N must be an integer")
#     if not isinstance(text, type(str())):
#         raise TypeError("First parameter must be a string")
#     if N <= 0:
#         raise NonpositiveNGramLengthException("N must be positive")

#     # Adding end and beginning symbols
#     if startstop:
#         text = "".join(['[', text, ']'])
#     nGrams = dict()
#     # Must cut the loop short by N-1 iterations
#     for i in range(len(text)-(N-1)):
#         seq = text[i:i+N]
#         if seq not in nGrams:
#             nGrams[seq] = 0
#         nGrams[seq] += 1
#     # Get sum of vals
#     valsum = sum(nGrams.values())
#     nGrams  = {k: v/valsum for k, v in nGrams.items()}
#     return nGrams


def get_Ngrams(words, N):
    '''Return word-wise n-gram of size N'''
    words.insert(0, 'START')
    words.append('END')
    nGrams = dict()
    for i in range(len(words) - (N-1)):
        seq = tuple(words[i:i+N])
        if seq not in nGrams:
            nGrams[seq] = 0
        nGrams[seq] += 1
    valsum = sum(nGrams.values())
    nGrams = {k: v/valsum for k, v in nGrams.items()} # Normalize to probabilities.
    return nGrams

def proba(test_phrase, nGrams, N):
    """Return the probability of the test phrase existing given learned nGrams"""
    words = super_strip(test_phrase)
    prob = 1
    for i in range(len(words) - (N -1)):
        seq = tuple(words[i:i+N])
        prob *= nGrams[seq]
    return prob

def getNSignificantDigits(num, N):
    """Return N significant digits without rounding."""
    fstr = f"{num:#.{N}g}" # To string. Remove leading zeros, keep trailing.
    fstr = "".join(ch for ch in fstr if ch.isnumeric()) # Remove any punctuation.
    return  int(fstr)
            

def main():
    contents = filtered_read("TheStoryofAnHour-KateChopin.txt")
    test_phrase = 'no one'

    nGrams = get_Ngrams(contents, 2)
    prob = proba(test_phrase, nGrams, 2)
    significants = getNSignificantDigits(prob, 3)
    rem = significants%173
    print(f"Remainder without start and stop markers: {rem}")


if __name__ == "__main__":
    main()