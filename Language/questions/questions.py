import os
import string
import math
import nltk
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # First we create an output dictionary var
    dictionary = dict()

    # Here we iterate through files in the directory and read them into the dictionary
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), encoding="utf-8") as file_reader:
            dictionary[file] = file_reader.read()

    # Here we return our desired dictionary
    return dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Important variables
    bad_punctuation = string.punctuation
    stop_words = nltk.corpus.stopwords.words("english")

    # Here we tokenize and turn the words into lowercase
    doc_tokenized = nltk.word_tokenize(document.lower())

    # Here we check and optimize the list elements
    optimized_list = [word for word in doc_tokenized if word not in bad_punctuation and word not in stop_words]

    # Here we return the desired list output
    return optimized_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Here we establish important values
    inverse_vals = dict()
    documents_num = len(documents)
    words_iterable = set(word for value in documents.values() for word in value)

    # Here we iterate through words(iterable) and calculates idf-vals
    for word in words_iterable:
        docs_containing_word = 0

        # Here we check for value appearing inside the docs
        for document_check in documents.values():
            if word in document_check:
                docs_containing_word += 1

        # Here we calculate idf based on the n-log
        inverse_doc_value = math.log(documents_num / docs_containing_word)
        inverse_vals[word] = inverse_doc_value

    # Here we return the desired idfs dictionary values
    return inverse_vals


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Here we establish important values
    file_values = dict()

    # Here we go through files to rank, and calculate tf-idf values
    for file, words in files.items():
        tf_idf = 0
        for word in query:
            tf_idf += words.count(word) * idfs[word]
        file_values[file] = tf_idf

    # Here we rank the dictionary and convert to list for output
    ranked_file_values = sorted(file_values.items(), key=lambda x: x[1], reverse=True)
    ranked_file_values = [x[0] for x in ranked_file_values]

    # Here we return our output list
    return ranked_file_values[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Here we establish important vars
    values = dict()

    # Here we iterate through sentences
    for sentence, words in sentences.items():
        value = 0
        for word in query:
            if word in words:
                value += idfs[word]

        # Here we deal with the ties situation
        if value != 0:
            density = sum([words.count(x) for x in query]) / len(words)
            values[sentence] = (value, density)

    # Here we sort by score and output desired output
    sorted_for_scores = [z for z, y in sorted(values.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]
    return sorted_for_scores[:n]


if __name__ == "__main__":
    main()
