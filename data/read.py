import sys, sqlite3, re
from data import db_scripts, match, queries


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
                    queries.insert_word(curs, word, tag)

                    prevtag = ""

                    if prevline != '\n':
                        prev = parse_line(prevline)
                        prevtag = prev[1]

                    queries.insert_tag_and_prev(curs, tag, prevtag)
                else:
                    sent_count += 1
            else:
                if line != '\n':
                    word, tag = parse_line(line)
                    queries.insert_word(curs, word, tag)
                    queries.insert_tag_and_prev(curs, tag, "")

    queries.insert_sentence_total(curs, sent_count)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    readdata()
