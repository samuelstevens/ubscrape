'''
module: `csvwriter` exposes a class CsvWriter that writes Urban Dictionary words and their definitions to many CSV files.
'''

import csv
import os
from typing import List, Set


class CsvWriter:
    '''
    Writes Urban Dictionary definitions according a spec set by Wei Xu.
    '''

    def __init__(self, limit=1000, out='UDdata/wordsonly'):
        # maps words to a list of definitions
        self.rows: List[List[str]] = []
        self.limit: int = limit
        self.first_word: str = ''
        self.last_word: str = ''

        # counts the number of files dumped for file naming
        self.filesdumped = 0

        if out[0] != '/':  # is not a root path
            self.path = os.path.join(os.getcwd(), out)
        else:
            self.path = out

    def write_word(self, word: str, definitions: Set[str]):
        '''
        Adds a word and writes to file if >1000 words.
        '''

        # check if both word and definitions are non-empty
        if word and definitions:
            # add the word to the pool.
            self.rows.append([word] + list(definitions))

            # if we have 1000 words, dump them
            if len(self.rows) >= self.limit:
                self.dump_pool()

    def dump_pool(self):
        '''
        Dumps the current pool of words to a file and clears self.rows.
        '''

        wordnumber = self.filesdumped * self.limit + 1

        wordletters = self.rows[0][0][0:2].lower()

        wordletters = ''.join([c for c in wordletters if not c.isspace()])

        filename = f'UD_{wordnumber:09}_{wordletters}.tsv'

        folder = self.path

        if not os.path.exists(folder):
            os.makedirs(folder)

        filepath = os.path.join(folder, filename)

        with open(filepath, 'w') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(self.rows)

        self.filesdumped += 1
        self.rows = []
