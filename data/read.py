import sys, sqlite3, re


def insert_and_count(cursor, table_name, column_name, value):
    cursor.execute('''select * from {tn} where {cn} = "{val}"'''.
                   format(tn=table_name, cn=column_name, val=value))
    val = c.fetchall()
    if val:
        cursor.execute('''update {tn} set count = count + 1 where {cn} = "{wv}"'''
                       .format(tn=table_name, cn=column_name, wv=value))
    else:
        cursor.execute('''insert into {tn} ({cn}) values ("{wv}")'''.format(tn=table_name, cn=column_name, wv=value))


def has_special_char(s):
    exp = r'[\W]'
    match = re.search(exp, s)

    return True if match else False


if __name__ == '__main__':
    file_name = sys.argv[1]
    conn = sqlite3.connect('corpus.db')
    c = conn.cursor()

    corpus = open(file_name)

    for line in corpus:
        # TODO: check to see if newline char is only char.
        # if it is skip, otherwise,  match on newline character with regex
        # then remove. Then check for special chars
        if not line != '\n':
            entry = line.split()
            word = entry[0].lower()
            tag = entry[1].split('\n')[0]
            # TODO: if not has_special_char(line)

            # insert word into word_ table
            insert_and_count(c, table_name='word', column_name='word_', value=word)
            insert_and_count(c, table_name='tag', column_name='tag_', value=tag)

    conn.commit()
    conn.close()
