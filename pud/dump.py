import json
from functools import reduce
import os


class JsonWriter:
    def __init__(self, limit=50, out='results'):
        self.pool = {}
        self.limit = limit
        self.first_word = ''
        self.last_word = ''
        if out[0] != '/':  # is not a root path
            self.path = os.path.join(os.getcwd(), out)
        else:
            self.path = out
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def write_word(self, word, definitions):
        if word and definitions:

            if self.first_word and word[0].lower() != self.first_word[0].lower():
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
        print(file_name)

        first_letter = file_name[0].lower()

        folder = os.path.join(self.path, first_letter)

        if not os.path.exists(folder):
            os.makedirs(folder)

        file = os.path.join(folder, file_name)

        with open(file, 'w') as f:
            # todo: add os.path.join and actually write to disk, as well as a letter folder structure
            json.dump(self.pool, f, sort_keys=True, indent=4)
        self.pool = {}

    def size(self):
        def r(total_len, word):
            defs = self.pool[word]

            return total_len + len(word) + reduce(lambda total, definition: total +
                                                  len(definition), defs, 4 * len(defs))

        return 2 * reduce(r, self.pool, 2)
