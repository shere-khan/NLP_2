import sqlite3


def create(c):
    c.execute('''CREATE TABLE word (word_ text, tag_ text, count real, next_word text)''')
    c.execute('''CREATE TABLE tag (tag_ text, prev_tag text, next_tag text, count real)''')
    c.execute('''CREATE TABLE statistics (tot_sentences real)''')


def delete(c):
    c.execute('''drop table word''')
    c.execute('''drop table tag''')
    c.execute('''drop table statistics''')


if __name__ == '__main__':
    conn = sqlite3.connect('corpus.db')
    c = conn.cursor()

    delete(c)
    create(c)

    conn.commit()
    conn.close()
