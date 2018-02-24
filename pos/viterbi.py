import sys, sqlite3
from datastructures import graph
from data import read


class WordVertex:
    def __init__(self, word, tag, likelihood):
        self.word = word
        self.tag = tag
        self.likelihood = likelihood
        self.best_prob_so_far = self.likelihood
        self.best_prev = None
        self.prev = None

    def __repr__(self):
        return 'word: {0} tag: {1} likelihood: {2}'.format(self.word, self.tag,
                                                           self.likelihood)

    def __str__(self):
        return 'word: {0} tag: {1} likelihood: {2}'.format(self.word, self.tag,
                                                           self.likelihood)


def initializegraph(cursor, sent, exec_columns):
    g = graph.Graph(directed=True)
    start = g.insert_vertex(WordVertex(word="", tag="", likelihood=1))
    prevnodes = [start]

    for w in sent:
        nextnodes = list()
        wtags = read.get_tags_for_word(cursor, w)

        for wtag in wtags:
            likelihood = read.get_word_likelihood(cursor, w, wtag[0])
            v = g.insert_vertex(WordVertex(w, wtag[0], likelihood))
            nextnodes.append(v)

            for u in prevnodes:
                transprob = read.get_transition_prob(cursor, wtag[0], u.element.tag)
                g.insert_edge(u, v, transprob)

        exec_columns.append(nextnodes)
        prevnodes = nextnodes

    return g


def find_tagging(sentence):
    exec_columns = list()
    g = initializegraph(curs, sentence, exec_columns)
    viterbi(g, exec_columns)
    print_best_path(exec_columns)


def viterbi(g, exec_columns):
    class Path:
        def __init__(self, edge, prob):
            self.edge = edge
            self.prob = prob

    for col in exec_columns:
        for v in col:
            edges_in = g.incident_edges(v, outgoing=False)
            probs = list()

            # select best transition probability out of all incoming edges to v
            # and stores best path (prev) and prob (maxprob) in v
            for e in edges_in:
                prev = e.opposite(v)
                possible_best = prev.element.best_prob_so_far * e.element \
                                * v.element.likelihood
                probs.append(Path(e, possible_best))

            best_path = max(probs, key=lambda x: x.prob)
            v.element.best_prob_so_far = best_path.prob
            v.element.prev = best_path.edge.opposite(v)


def print_emission_probs(curs):
    words = read.get_distinct_words(curs)
    tags = read.get_distinct_tags(curs)
    for w in words:
        for t in tags
    # for each word
        # for each tag
            # get ct(word, tag)
            # get tag count


def print_tags_observed(curs):
    tags = read.get_distinct_tags(curs)

    print('All tags observed:')
    for i, tag in enumerate(tags):
        print("{0} {1}".format(i, tag[0]))


def print_tag_dist(curs):
    tags = read.get_distinct_tags(curs)

    print('Initial Distributions')
    for tag in tags:
        totsent = read.get_sentence_total(curs)
        initct = read.get_tag_initial_prob(curs, tag[0])
        p = initct / totsent
        print('{0} {1:.5f}'.format(tag[0], p))


def print_best_path(exec_column):
    best = max(exec_column[-1], key=lambda x: x.element.best_prob_so_far)

    print('word and tagging in reverse')
    while best.element.prev:
        print('word: {0} tag: {1}'.format(best.element.word, best.element.tag))
        best = best.element.prev


if __name__ == '__main__':
    print('University of Central Florida')
    print('CAP6640 String 2018 - Dr. Glinos')
    print()
    print('Viterbi Algorithm HMM Tagger by Justin Barry')

    test_file = sys.argv[1]

    conn = sqlite3.connect('../data/corpus.db')
    curs = conn.cursor()

    # print_tags_observed(curs)
    # print()
    # print_tag_dist(curs)
    print_emission_probs(curs)

    # with open(test_file) as f:
    #     for line in f:
    #         print()
    #         line = line.lower()
    #         sent = line.split()
    #         find_tagging(sent)
