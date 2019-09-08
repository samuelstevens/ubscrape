# internal to python
import re
from typing import List
from urllib.parse import unquote
from string import ascii_uppercase
from sqlite3 import IntegrityError

# external
import requests
from bs4 import BeautifulSoup


from constants import BASE_URL


def write_words_for_letter(prefix: str, con):
    if not prefix:
        raise ValueError(f'Prefix {prefix} needs to be at least one letter.')

    def make_url():
        if page_num > 1:
            return f'{BASE_URL}/browse.php?character={letter}&page={page_num}'
        return f'{BASE_URL}/browse.php?character={letter}'

    letter = prefix.upper()

    page_num = con.execute(
        'SELECT max(page_num) FROM word WHERE letter = ?', (letter,)).fetchone()[0]

    if not page_num:
        page_num = 1

    url = make_url()
    r = requests.get(url)

    while r.url != 'https://www.urbandictionary.com/':

        soup = BeautifulSoup(r.text, features="html.parser")
        a_tags = soup.find_all('a', href=re.compile(r'/define.php'))

        pattern = re.compile(
            r'\/define\.php\?term=(.*)')

        links = [l['href'] for l in a_tags]

        encoded_words = [pattern.search(l).group(
            1) for l in links if pattern.search(l)]

        words = [unquote(w) for w in encoded_words]

        formatted_words = [(w, 0, page_num, letter) for w in words]

        try:
            con.executemany(
                'INSERT INTO word(word, complete, page_num, letter) VALUES (?, ?, ?, ?)', formatted_words)
            con.commit()
        except IntegrityError:
            pass

        print(
            f'Working on page {page_num} for {letter}. Total {140 * page_num} {letter} words.')

        page_num += 1
        url = make_url()
        r = requests.get(url)


def write_all_words(con):
    for l in ascii_uppercase:
        write_words_for_letter(l, con)
