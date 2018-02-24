import sys, sqlite3, re
from data import db_scripts, match


def insert(cursor, table_name, column_name, value):
    cursor.execute('''insert into {tn} ({cn}) values ("{wv}")'''
                   .format(tn=table_name, cn=column_name, wv=value))


def insert_word(cursor, word, tag):
    cursor.execute('''insert into word (word_, tag_) values ("{wordval}", "{tg}")'''
                   .format(wordval=word, tg=tag))


def insert_tag_and_prev(cursor, tag, prevtag):
    cursor.execute(
        '''insert into tag (tag_, prev_tag) values ("{tagval}", "{pt}")'''
            .format(tagval=tag, pt=prevtag))


def get_distinct_tags(cursor):
    cursor.execute('''SELECT DISTINCT tag_ FROM tag ORDER BY tag_'''.format())

    return cursor.fetchall()


def get_prob_for_tag(curs, tag):
    curs.execute('''select count(*) from tag where tag_ = "{t}"'''.format(t=tag))
    res = curs.fetchall()[0][0]
    tot = get_tag_total_count(curs)

    return res / tot


def get_tag_count(cursor, tag):
    cursor.execute('''select count(*) from tag where tag_ = "{t}"'''.format(t=tag))

    return cursor.fetchall()[0][0]


def get_tag_total_count(curs):
    curs.execute('''SELECT count(*) FROM tag''')

    return curs.fetchall()[0][0]


def get_tags_for_word(cursor, word):
    cursor.execute(
        '''select distinct tag_ from word where word_ = "{wd}"'''.format(wd=word))
    res = cursor.fetchall()

    return res


def get_transition_prob(cursor, tag, prevtag):
    cursor.execute('''select count(*) from tag where tag_ = "{t}"'''.format(t=tag))
    tagcount = cursor.fetchall()

    cursor.execute('''SELECT count(*) FROM tag WHERE tag_ = "{t}" and prev_tag = "{pt}"'''
                   .format(t=tag, pt=prevtag))
    tag_combo_count = cursor.fetchall()

    return tag_combo_count[0][0] / tagcount[0][0]


def get_word_likelihood(cursor, word, tag):
    cursor.execute(
        '''select count(word_) from word where tag_ = "{tg}" and word_ = "{wd}"'''
            .format(tg=tag, wd=word))
    res1 = cursor.fetchall()
    cursor.execute('''select count(word_) from word where tag_ = "{tg}"'''.format(
        tg=tag))
    res2 = cursor.fetchall()

    return res1[0][0] / res2[0][0]


def get_distinct_words(curs):
    curs.execute('''SELECT DISTINCT word_ FROM word''')

    return curs.fetchall()


def get_tag_initial_prob(cursor, tag):
    cursor.execute('''select count(*) from tag where prev_tag = "" and tag_ = "{t}"'''
                   .format(t=tag))

    return cursor.fetchall()[0][0]


def insert_sentence_total(curs, count):
    curs.execute('''insert into statistics (tot_sentences) values ({ct})'''
                 .format(ct=count))


def get_sentence_total(curs):
    curs.execute('''SELECT tot_sentences FROM statistics''')

    return curs.fetchall()[0][0]


def has_special_char(s):
    exp = r'[\W]'
    match = re.search(exp, s)

    return True if match else False


def parse_line(line):
    entry = line.split()
    word = entry[0].lower()
    r = match.Rules()
    word = r.lemmatize(word)

    tag = entry[1].split('\n')[0]

    return word, tag


class Stats:
    def __init__(self):
        self.sent_count = 0


def readdata():
    file_name = sys.argv[1]
    conn = sqlite3.connect('corpus.db')
    curs = conn.cursor()

    db_scripts.delete(curs)
    db_scripts.create(curs)

    sent_count = 0
    with open(file_name, 'r') as f:
        lines = f.readlines()

        for i in range(0, len(lines)):
            line = lines[i]

            if i >= 1:
                prevline = lines[i - 1]
                if line != '\n':
                    word, tag = parse_line(line)
                    insert_word(curs, word, tag)

                    prevtag = ""

                    if prevline != '\n':
                        prev = parse_line(prevline)
                        prevtag = prev[1]

                    insert_tag_and_prev(curs, tag, prevtag)
                else:
                    sent_count += 1
            else:
                if line != '\n':
                    word, tag = parse_line(line)
                    insert_word(curs, word, tag)
                    insert_tag_and_prev(curs, tag, "")

    insert_sentence_total(curs, sent_count)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    readdata()
