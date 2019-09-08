import sqlite3


def get_connection(db_file_name):
    conn = sqlite3.connect(db_file_name)

    return conn


def initialize_db():
    con = get_connection('urban-dict.db')

    con.execute('''CREATE TABLE IF NOT EXISTS word (
    word text PRIMARY KEY,
    letter text NOT NULL,
    complete integer NOT NULL,
    page_num integer NOT NULL
    );''')

    con.execute('''CREATE TABLE IF NOT EXISTS definition (
    id integer PRIMARY KEY,
    word_id integer NOT NULL,
    definition text NOT NULL,
    FOREIGN KEY (word_id) REFERENCES word (id)
    );''')

    con.commit()

    return con
