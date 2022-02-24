import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# This is my original attempt. It suffered from more ambiguity. Also several
# Definitions that recurred back to defining a single noun as NP caused issues
# with finding correct noun phrases. The noun alone got picked up wWhile any
# words modifying it belonged to a higher noun phrase.
NONTERMINALS = """
S -> NP VP
NP -> N | Adj NP | Det N | Det Adj NP | N NP | Adv | Adv NP | Conj S | Conj VP | PP
VP -> V | V NP | V NP PP | V PP
PP -> P NP
"""

# This is the version of non-terminals that I'm trying to backwards engineer from
# the grader outputs.
NONTERMINALS = """
S -> S T | NP Vd | S Conj Sd | Vd T
T -> NP | PNP | Adv
NP -> Det Nd | NP PNP | N
PNP -> P NP
Nd -> N | Adj N
Vd -> V | Adv V
Sd -> S
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # First sentence is converted to lowercase and the words are split into
    # a list on any whitespace markers. Then that list is filtered. The lambda
    # function used as the filtering conditions checks every letter of a given
    # word and produces a logical array telling whether or not the characters are
    # alphabetic. A non-zero sum tells us that the word has at least one alphabet.
    return list(filter(lambda w: sum([c.isalpha() for c in w]) != 0,
        nltk.word_tokenize(sentence.lower())))


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Using Depth first search to find NP chunks in the same order
    # as they read.
    np_chunks = list()
    for subtree in tree:
        # This is false if we're at terminal node.
        if isinstance(subtree, type(tree)):
            # Finding np_chunks in the examined subtree.
            sub_np_chunks = np_chunk(subtree)

            # If none found, and currently at NP, add current.
            if (len(sub_np_chunks) == 0) & (subtree.label() == 'NP'):
                np_chunks.append(subtree)

            # Any NP chunk found at this, or lower level is added to np_chunks.
            # Grammar here doesn't allow a tree that would have multiple NP subtrees,
            # but this solution should work even if that grammar was to change.
            np_chunks += sub_np_chunks
    return np_chunks       


if __name__ == "__main__":
    main()
