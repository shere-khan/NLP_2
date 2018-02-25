import sys, sqlite3
from datastructures import graph
from data import read, queries


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

        isword = queries.is_word_in_corpus(curs, w)
        if isword:
            wtags = queries.get_distinct_tags_for_word(cursor, w)
        else:
            wtags = [('NN',)]

        for wtag in wtags:
            wtag = wtag[0]
            likelihood = queries.get_word_likelihood(cursor, w, wtag)
            v = g.insert_vertex(WordVertex(w, wtag, likelihood))
            nextnodes.append(v)

            for u in prevnodes:
                transprob = queries.get_transition_prob(cursor, wtag, u.element.tag)
                g.insert_edge(u, v, transprob)

        exec_columns.append(nextnodes)
        prevnodes = nextnodes

    return g


def find_tagging(sentence):
    exec_columns = list()
    g = initializegraph(curs, sentence, exec_columns)
    print('Intermediate Values:', end='\n\n')
    viterbi(g, sentence, exec_columns)
    print_best_path(exec_columns)


def viterbi(g, sent, exec_columns):
    class Path:
        def __init__(self, edge, prob):
            self.edge = edge
            self.prob = prob

    for word, col in zip(sent, exec_columns):
        print('{0} : '.format(word), end=' ')
        resultlist = list()
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

            resultlist.append(((best_path.edge.origin.element.tag, v.element.tag),
                               best_path.prob))
        totprob = 0
        for res in resultlist:
            prob = res[1]
            totprob += prob

        for res in resultlist:
            edges = res[0]
            prob = res[1]
            prev = edges[0]
            cur = edges[1]
            print('({0:.6f}, {1})'.format(prob / totprob, prev), end=' ')
            sys.stdout.flush()

        print()


def print_emission_probs(curs):
    words = queries.get_distinct_words(curs)
    for w in words:
        w = w[0]
        tags = queries.get_distinct_tags_for_word(curs, w)
        for t in tags:
            t = t[0]
            like = queries.get_word_likelihood(curs, w, t)
            print('{:>23}'.format(w), end=' ')
            print('{:>4}'.format(t), end=' ')
            print('{:<.6f}'.format(like), end='\n')
    print()


def print_tags_observed(curs):
    tags = queries.get_distinct_tags(curs)

    print('All tags observed:')
    for i, tag in enumerate(tags):
        print("{0} {1}".format(i, tag[0]))
    print()


def print_tag_dist(curs):
    tags = queries.get_distinct_tags(curs)

    print('Initial Distributions', end='\n\n')
    for tag in tags:
        totsent = queries.get_sentence_total(curs)
        initct = queries.get_tag_initial_prob(curs, tag[0])
        p = initct / totsent
        print('{0} {1:.5f}'.format(tag[0], p))
    print()


def print_best_path(exec_column):
    best = max(exec_column[-1], key=lambda x: x.element.best_prob_so_far)

    print()
    print('Viterbi Tagger Output', end='\n\n')
    printlist = list()
    while best.element.prev:
        printlist.append((best.element.word, best.element.tag))
        best = best.element.prev

    for item in reversed(printlist):
        print('{0} tag: {1}'.format(item[0], item[1]))


def print_transition_probs(curs):
    print('Transition Probabilities:', end='\n\n')
    prevtags = queries.get_distinct_tags(curs)
    for pt in prevtags:
        pt = pt[0]
        tags = queries.get_all_distinct_tags_for_previous_tag(curs, pt)
        for t in tags:
            t = t[0]
            prob = queries.get_transition_prob2(curs, t, pt)
            print('[{0} | {1}] {2:.6f}'.format(t, pt, prob), end=' ')
        print()
    print()


def print_tag_count(curs):
    tags = queries.get_distinct_tags(curs)
    print('Total # tags: {0}'.format(len(tags)))


def print_lexicals(curs):
    words = queries.get_distinct_words(curs)
    print('Total # lexicals: {0}'.format(len(words)))


def print_num_sentences(curs):
    numsent = queries.get_sentence_total(curs)
    print('Total # sentences : {0}'.format(numsent), end='\n\n')


def print_tokens_found_in_corpus(curs, words):
    print('Tokens Found In Corpus:', end='\n\n')
    for i, w in enumerate(words):

        isword = queries.is_word_in_corpus(curs, w)
        if isword:
            tags = queries.get_distinct_tags_for_word(curs, w)
            # print('Iteration {ct}:'.format(ct=i), end='   ')
            print('{0} : '.format(w), end=' ')
            for t in tags:
                t = t[0]
                like = queries.get_word_likelihood(curs, w, t)
                print('{0} ({1:.6f})'.format(t, like), end=' ')
            print()


def print_bigrams(curs):
    words = queries.get_distinct_words(curs)
    tot_bigrams = 0
    for w in words:
        w = w[0]
        bigrams = queries.get_distinct_word_next_word_pairs(curs, w)
        if bigrams:
            tot_bigrams += len(bigrams)

    print('Total # bigrams : {0}'.format(tot_bigrams))


if __name__ == '__main__':
    print('University of Central Florida')
    print('CAP6640 String 2018 - Dr. Glinos')
    print()
    print('Viterbi Algorithm HMM Tagger by Justin Barry', end='\n\n')

    test_file = sys.argv[1]
    emissions_flag = sys.argv[2]

    conn = sqlite3.connect('../data/corpus.db')
    curs = conn.cursor()

    print_tags_observed(curs)
    print_tag_dist(curs)
    if emissions_flag == 'True':
        print_emission_probs(curs)
    print_transition_probs(curs)
    print('Corpus Features: ', end='\n\n')
    print_tag_count(curs)
    print_lexicals(curs)
    print_num_sentences(curs)

    with open(test_file) as f:
        for line in f:
            print()

            line = line.lower()
            sent = line.split()
            print_tokens_found_in_corpus(curs, sent)
            print()

            find_tagging(sent)
