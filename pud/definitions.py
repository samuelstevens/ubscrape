import multiprocessing as mp
from typing import List

from bs4 import BeautifulSoup
import requests

from constants import BASE_URL
from db import initialize_db

CON = initialize_db()


def define_word(word) -> List[str]:
    if not word:
        raise ValueError('Must pass a word.')

    url = f'{BASE_URL}/define.php'

    r = requests.get(url, params={'term': word})

    soup = BeautifulSoup(r.text, features="html.parser")

    meaning_tags = soup.find_all('div', {'class': 'meaning'})

    definitions = [t.text for t in meaning_tags]

    return definitions


def write_definition(word):
    # complete = CON.execute(
    #     'SELECT complete FROM word WHERE word = ?', (word,)).fetchone()[0]

    # if complete:
    #     return CON.execute('SELECT definition FROM definition WHERE word_id = ?', (word,)).fetchall()

    defs = define_word(word)
    formatted_defs = [(d, word) for d in defs]

    CON.executemany(
        'INSERT INTO definition(definition, word_id) VALUES (?, ?)', formatted_defs)
    CON.execute('UPDATE word SET complete = 1 WHERE word = ?', (word,))
    CON.commit()

    return defs


def define_all_words():
    pool = mp.Pool(mp.cpu_count())

    words = CON.execute(
        'SELECT word FROM word WHERE complete = 0').fetchall()

    pool.map(write_definition, words, chunksize=200)
