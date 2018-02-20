import sys, sqlite3, re
from data import db_scripts


def insert(cursor, table_name, column_name, value):
    cursor.execute('''insert into {tn} ({cn}) values ("{wv}")'''
                   .format(tn=table_name, cn=column_name, wv=value))


def insert_word(cursor, word):
    cursor.execute(
        '''insert into word (word_) values ("{wordval}")'''.format(wordval=word))


def insert_tag_and_prev(cursor, tag, prevtag):
    cursor.execute(
        '''insert into tag (tag_, prev_tag) values ("{tagval}", "{pt}")'''
            .format(tagval=tag, pt=prevtag))


def get_tags_for_word(cursor, word):
    cursor.execute('''select * from tag where word_ = "{wd}"'''.format(wd=word))

    return cursor.fetchall()


def get_transition_prob(cursor, prevtag, tag):
    cursor.execute('''select * from tag where tag_ = "{t}"'''.format(
        t=tag))
    tagcount = len(cursor.fetchall())

    cursor.execute('''SELECT * FROM tag WHERE prev_tag = "{pt}"'''.format(pt=prevtag))
    tag_combo_count = len(cursor.fetchall())

    return tag_combo_count / tagcount


def get_word_likelihood(cursor, word, tag):
    wt = cursor.execute('''select * from word where tag_ = "{tg}" and word_ = "{wd}"'''
                        .format(tg=tag, wd=word))
    t = cursor.execute('''select * from word where tag_ = "{tg}"'''.format(tg=tag))

    return wt / t


def has_special_char(s):
    exp = r'[\W]'
    match = re.search(exp, s)

    return True if match else False


def parse_line(line):
    entry = line.split()
    word = entry[0].lower()
    tag = entry[1].split('\n')[0]

    return word, tag


def readdata():
    file_name = sys.argv[1]
    conn = sqlite3.connect('corpus.db')
    curs = conn.cursor()

    db_scripts.delete(curs)
    db_scripts.create(curs)

    with open(file_name, 'r') as f:
        lines = f.readlines()

        for i in range(0, len(lines)):
            line = lines[i]

            if i >= 1:
                prevline = lines[i - 1]
                if line != '\n':
                    word, tag = parse_line(line)
                    insert_word(curs, word)

                    prevtag = ""
                    if prevline != '\n':
                        prev = parse_line(prevline)
                        prevtag = prev[1]
                    insert_tag_and_prev(curs, tag, prevtag)
            else:
                if line != '\n':
                    word, tag = parse_line(line)
                    insert_word(curs, word)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    readdata()
