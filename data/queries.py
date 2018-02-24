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


def get_distinct_tags_for_word(cursor, word):
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
    res1 = get_count_word_and_tag(cursor, word, tag)
    res2 = get_tag_count(cursor, tag)

    return res1 / res2


def get_distinct_words(curs):
    curs.execute('''select distinct word_ from word order by word_ ASC''')

    return curs.fetchall()


def get_tag_initial_prob(cursor, tag):
    cursor.execute('''select count(*) from tag where prev_tag = "" and tag_ = "{t}"'''
                   .format(t=tag))

    return cursor.fetchall()[0][0]


def insert_sentence_total(curs, count):
    curs.execute('''insert into statistics (tot_sentences) values ({ct})'''
                 .format(ct=count))


def get_sentence_total(curs):
    curs.execute('''select tot_sentences FROM statistics''')

    return curs.fetchall()[0][0]


def get_count_word_and_tag(curs, word, tag):
    curs.execute(
        '''select count(word_) from word where tag_ = "{tg}" and word_ = "{wd}"'''
            .format(tg=tag, wd=word))

    return curs.fetchall()[0][0]
