import sys, sqlite3


def insert_word(cursor, word_val, table_name):
    cursor.execute('''select * from word where {tn} = "{val}"'''.
                   format(tn=table_name, val=word_val))
    val = c.fetchall()
    if val:
        cursor.execute('''update word set count = count + 1 where word_ = "{0}"'''.format(word_val))
    else:
        cursor.execute('''insert into word (word_) values ("{0}")'''.format(word_val))


if __name__ == '__main__':
    file_name = sys.argv[1]
    conn = sqlite3.connect('corpus.db')
    c = conn.cursor()

    corpus = open(file_name)

    for line in corpus:
        if line != '\n':
            entry = line.split()
            word = entry[0].lower()
            tag = entry[1].split('\n')[0]

            # insert word into word_ table
            insert_word(c, word, 'word')

    conn.commit()
    conn.close()
