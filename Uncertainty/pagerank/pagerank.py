import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Firstly we establish key vars
    output = {}
    links = len(corpus[page])

    # Secondly we check if outgoing links exist
    if links:

        # Here we add buffer factor to all pages
        for link in corpus:
            output[link] = (1 - damping_factor) / len(corpus)

        # Here we add the key factors to outgoing links
        for link in corpus[page]:
            output[link] += damping_factor / links

    # Here we add probabilities if no outgoing links exist
    else:
        for link in corpus:
            output[link] = 1 / len(corpus)

    # Here we return the probability distribution dictionary as output
    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Here we create a dictionary of page counts(initially 0 for all)
    page_count = {}
    for page in corpus:
        page_count[page] = 0

    # Here we establish a loop to iterate n times and create a transition model var
    transition_changer = {}
    for i in range(n):
        if i == 0:
            # Here we choose the first sample at random and tally its count in page count
            random_choice_1 = random.choice(list(corpus))
            for page in page_count:
                if page == random_choice_1:
                    page_count[page] += 1

            # Here we determine the next probability distribution
            transition_changer = transition_model(corpus, random_choice_1, damping_factor)
        else:

            # Here we establish weights for next sample
            weights = []
            for website in transition_changer:
                weights.append(transition_changer[website])
            # Here we pick randomly based on the weights list and tally the page count
            random_choice_next = random.choices(list(corpus), weights=weights, k=1)
            for page in page_count:
                if page == random_choice_next[0]:
                    page_count[page] += 1
            # Here we modify the transition model for next iteration
            transition_changer = transition_model(corpus, random_choice_next[0], damping_factor)

    # Here we create a proportion to determine page rank values and create output dictionary
    output = {}
    for page in page_count:
        output[page] = page_count[page] / n

    # Here we output the desired dictionary with page ranks and outputs
    return output


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Firstly we establish useful values
    page_ranks = {}
    convergence = 0.0001
    N = len(corpus)

    # Here we establish ranking output initially
    for page in corpus:
        page_ranks[page] = 1 / N

    # Here we iterate through the pages till the threshold is meet
    while True:
        # Here we establish a page check, sum variable, and calculate page ranks
        counter = 0
        for website in corpus:
            # The first part of the formula and initializing the second part
            latest = (1 - damping_factor) / N
            sum_val = 0
            # Here we implement the second part
            for site in corpus:
                if website in corpus[site]:
                    outgoing_links = len(corpus[site])
                    sum_val = sum_val + page_ranks[site] / outgoing_links
            sum_val = damping_factor * sum_val
            latest += sum_val

            # Here we check for the threshold being met, update vals
            # and move onto next page rank calc.
            if abs(page_ranks[website] - latest) < convergence:
                counter += 1
            page_ranks[website] = latest

        # Here we check if we've finished calculations
        if counter == N:
            break

    # Here we return the desired list of page rankings
    return page_ranks


if __name__ == "__main__":
    main()
