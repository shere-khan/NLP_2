import sqlite3


def create(c):
    c.execute('''CREATE TABLE word (word_ text, next_word text, count real)''')
    c.execute('''CREATE TABLE tag (tag_ text, next_tag text, count real)''')


def delete(c):
    c.execute('''drop table word''')
    c.execute('''drop table tag''')


if __name__ == '__main__':
    conn = sqlite3.connect('corpus.db')
    c = conn.cursor()

    create(c)
    # delete(c)

    conn.commit()
    conn.close()
