import sys, sqlite3, re
from data import db_scripts


def insert(cursor, table_name, column_name, value):
    cursor.execute('''insert into {tn} ({cn}) values ("{wv}")'''
                   .format(tn=table_name, cn=column_name, wv=value))


def insert_word_and_next(cursor, word, next_word):
    cursor.execute('''insert into word (word_, next_word) values ("{wordval}", "{nextwordval}")'''
                   .format(wordval=word, nextwordval=next_word))


def insert_tag_and_next(cursor, tag, next_tag):
    cursor.execute('''insert into tag (tag_, next_tag) values ("{tagval}", "{nexttagval}")'''
                   .format(tagval=tag, nexttagval=next_tag))


def has_special_char(s):
    exp = r'[\W]'
    match = re.search(exp, s)

    return True if match else False


def parse_line(line):
    entry = line.split()
    word = entry[0].lower()
    tag = entry[1].split('\n')[0]

    return word, tag


if __name__ == '__main__':
    file_name = sys.argv[1]
    conn = sqlite3.connect('corpus.db')
    curs = conn.cursor()

    db_scripts.delete(curs)
    db_scripts.create(curs)

    with open(file_name, 'r') as f:
        lines = f.readlines()

        for i in range(0, len(lines)):
            line = lines[i]
            if i + 1 < len(lines):
                nextline = lines[i + 1]

            # insert word into word_ table
            if line != '\n':
                word, tag = parse_line(line)
                if nextline != '\n':
                    nextword, nexttag = parse_line(nextline)
                    insert_tag_and_next(curs, tag, nexttag)
                    insert_word_and_next(curs, word, nextword)
                else:
                    insert_tag_and_next(curs, tag, '')
                    insert_word_and_next(curs, word, '')

    conn.commit()
    conn.close()
