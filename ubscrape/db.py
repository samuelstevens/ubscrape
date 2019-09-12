import sqlite3
from .jsonwriter import JsonWriter
from typing import List, Tuple
DB_FILE_NAME = 'urban-dict.db'


def get_connection():
    con = sqlite3.connect(DB_FILE_NAME)

    return con


def initialize_db():
    con = get_connection()

    con.execute('''CREATE TABLE IF NOT EXISTS word (
    word text PRIMARY KEY,
    letter text NOT NULL,
    complete integer NOT NULL,
    page_num integer NOT NULL
    );''')

    con.execute('''CREATE TABLE IF NOT EXISTS definition (
    id integer PRIMARY KEY,
    word_id text NOT NULL,
    definition text NOT NULL,
    FOREIGN KEY (word_id) REFERENCES word (word)
    );''')

    con.commit()

    return con


def clear_database():
    con = get_connection()

    con.execute('DROP TABLE definition')
    con.execute('DROP TABLE word')

    con.commit()

    con.close()


def dump_database(arg):
    con = get_connection()

    writer = JsonWriter()

    if isinstance(arg, str):
        writer = JsonWriter(out=arg)

    prev_word = ''
    definition_set = set()

    query = 'SELECT word.word, definition.definition FROM definition INNER JOIN word ON definition.word_id=word.word ORDER BY word.word ASC;'

    for (word, definition) in con.execute(query).fetchall():
        if word == prev_word:
            # add to the same set
            definition_set.add(definition)

        if word != prev_word:
            # dump this definition and start a new set
            writer.write_word(prev_word, definition_set)

            prev_word = word
            definition_set = set([definition])

    writer.write_word(prev_word, definition_set)
    writer.dump_pool()
