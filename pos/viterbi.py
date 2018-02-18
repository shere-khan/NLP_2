import sys, sqlite3
from datastructures import graph
from data import read


class Word:
    def __init__(self, word, tag, prob):
        self.word = word
        self.tag = tag
        self.prob = prob


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
                likelihood = read.get_word_likelihood(cursor, w, wtag)
                v = g.insert_vertex(vc, Word(wtag, w, likelihood))
                nextnodes.append(v)
                transprob = read.get_transition_prob(cursor, wtag, u.word.tag)
                g.insert_edge(u, v, transprob)

        prevnodes = nextnodes


if __name__ == '__main__':
    print('University of Central Florida')
    print('CAP6640 String 2018 - Dr. Glinos')
    print()
    print('Viterbi Algorithm')

    corpus = sys.argv[1]
    test_file = sys.argv[2]

    conn = sqlite3.connect('corpus.db')
    curs = conn.cursor()
