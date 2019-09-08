import requests
from bs4 import BeautifulSoup
from typing import List

from constants import BASE_URL


def define_word(word) -> List[str]:
    if not word:
        raise ValueError('Must pass a word.')

    url = f'{BASE_URL}/define.php'

    r = requests.get(url, params={'term': word})

    soup = BeautifulSoup(r.text, features="html.parser")

    meaning_tags = soup.find_all('div', {'class': 'meaning'})

    definitions = [t.text for t in meaning_tags]

    return definitions


def define_all_words(con):
    words = con.execute('SELECT * FROM word WHERE complete = 0').fetchall()

    for w in words:
        w = w[0]

        defs = define_word(w)

        formatted_defs = [(d, w) for d in defs]

        con.executemany(
            'INSERT INTO definition(definition, word_id) VALUES (?, ?)', formatted_defs)
        con.execute('UPDATE word SET complete = 1 WHERE word = ?', (w,))
        con.commit()
