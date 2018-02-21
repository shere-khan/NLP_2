import sys, sqlite3
from datastructures import graph
from data import read


class Word:
    def __init__(self, word, tag, prob):
        self.word = word
        self.tag = tag
        self.prob = prob

    def __repr__(self):
        return 'word: {0} tag: {1} likelihood: {2}'.format(self.word, self.tag, self.prob)

    def __str__(self):
        return 'word: {0} tag: {1} likelihood: {2}'.format(self.word, self.tag, self.prob)


def initializegraph(cursor, sent):
    g = graph.Graph()
    vc = 0
    start = g.insert_vertex(vc, Word("", "", ""))
    prevnodes = [start]
    vc += 1

    for w in sent:
        nextnodes = list()
        wtags = read.get_tags_for_word(cursor, w)

        for u in prevnodes:
            for wtag in wtags:
                likelihood = read.get_word_likelihood(cursor, w, wtag[0])
                v = g.insert_vertex(vc, Word(w, wtag[0], likelihood))
                vc += 1
                nextnodes.append(v)
                # ti = wtag[0]
                # ti_1 = u.get_data().tag
                transprob = read.get_transition_prob(cursor, wtag[0], u.get_data().tag)
                g.insert_edge(u, v, transprob)

        prevnodes = nextnodes

    return g


if __name__ == '__main__':
    print('University of Central Florida')
    print('CAP6640 String 2018 - Dr. Glinos')
    print()
    print('Viterbi Algorithm')

    corpus = sys.argv[1]
    test_file = sys.argv[2]

    conn = sqlite3.connect('../data/corpus.db')
    curs = conn.cursor()

    try:
        f = open(test_file)
        for line in f:
            line = line.lower()
            sent = line.split()
            sent = sent[:-1]
            g = initializegraph(curs, sent)
        f.close()
    except FileNotFoundError:
        print('file not found')
