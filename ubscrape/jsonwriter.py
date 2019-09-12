import json
from functools import reduce
import os
from typing import List, Dict, Set
from string import ascii_lowercase


def get_letter(word: str) -> str:
    if not word:
        return None

    if word[0].lower() in ascii_lowercase:
        return word[0].lower()
    else:
        return '*'


class JsonWriter:
    def __init__(self, limit=1, out='results'):
        self.pool: Dict[str, List[str]] = {}
        self.limit: int = limit
        self.first_word: str = ''
        self.last_word: str = ''
        if out[0] != '/':  # is not a root path
            self.path = os.path.join(os.getcwd(), out)
        else:
            self.path = out
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def write_word(self, word: str, definitions: Set[str]):
        if word and definitions:
            if self.first_word and get_letter(word) != get_letter(self.first_word):
                self.dump_pool()

            if not self.pool.keys():
                self.first_word = word

            self.pool[word] = list(definitions)

            self.last_word = word

            # 50 mb = 50 * 1024 * 1024 bytes
            # 50 * 1024 * 1024 / 2 = 26,214,400 characters
            if self.size() > 1024 * 1024 * self.limit:
                self.dump_pool()

    def dump_pool(self):
        file_name = f'{self.first_word}-{self.last_word}.json'

        first_letter = get_letter(file_name)

        folder = os.path.join(self.path, first_letter)

        if not os.path.exists(folder):
            os.makedirs(folder)

        file = os.path.join(folder, file_name)

        with open(file, 'w') as fp:
            json.dump(self.pool, fp, sort_keys=True, indent=4)
        self.pool = {}

    def size(self) -> int:
        def reduce_f(total_len: int, word: str):
            defs: List[str] = self.pool[word]

            return total_len + len(word) + reduce(lambda total, definition: total +
                                                  len(definition), defs, 4 * len(defs))

        return reduce(reduce_f, self.pool, 2)
