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

NONTERMINALS = """
S -> NP VP | VP NP | S PP | S Conj S | S AdvP | S NP PP PP
NP -> N | Det N | Det AdjP
VP -> V | V NP | V AdvP | AdvP NP  
PP -> P | P NP | P NP P
AdjP -> Adj | Adj N | Adj Adj N | Adj Adj Adj N
AdvP -> Adv | Adv V | V Adv
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
    # First we utilize word_tokenize to create a list from the sentence
    sentence_list = nltk.word_tokenize(sentence)

    # Here we invoke string processing helper function
    processed_list = string_text_processor(sentence_list)

    # Here we return the desired output
    return processed_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Here we create a list of desired values
    np_list = []

    # [ I made sure the inner tree problem wouldn't occur when defining NONTERMINALS by avoiding
    #   defining NPs in terms of itself, since I didn't really find a need to self-define NPs.]
    #
    # We iterate through the NP Subtrees
    for subtree in tree.subtrees(lambda t: t.label() == 'NP'):
        np_list.append(subtree)

    # Here we return our desired NP chunks list
    return np_list


# Helper function to process list of strings for preprocess
def string_text_processor(sentence_list):
    # Here we track non-alphabetical vals and iterate to convert uppercase ones
    removable_vals = []
    for index, item in enumerate(sentence_list):
        if not item.islower():
            if item.isalpha():
                sentence_list[index] = item.lower()
            else:
                removable_vals.append(item)

    # Here we remove non-alpha vals
    for value in removable_vals:
        sentence_list.remove(value)

    # Here we return desired output
    return sentence_list


if __name__ == "__main__":
    main()
