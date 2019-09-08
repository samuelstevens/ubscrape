# Python Urban Dictionary Scraper (aka PUDS)

This python script tries to scrape and store every single word and definition from Urban Dictionary.

```bash
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python pud/core.py
```

## Features

## How PUD Works

1. PUD goes through the page indices looking for every word (https://www.urbandictionary.com/browse.php?character=A, https://www.urbandictionary.com/browse.php?character=A&page=2, etc). PUD adds these words to a SQLite database in a `words` table. 

2. PUD goes through every row in the database and looks it up (https://www.urbandictionary.com/define.php?term=Magic%20Carpet%20Ride) and adds the definitions to a `definitions` table.

3. When PUD has added every definition for a word, it flags the word as `complete` and moves onto the next word.

4. When every word in PUD is complete, it dumps the SQLite database to JSON. Each letter gets its own folder, and then definitions are added to files in 1 MB groups. Each file will be ~1 MB, and the title will be the first and last word in the file (firstword-lastword.json).

If PUD crashes or fails, it will restart and try to redo as little work as possible.

## Questions

1. Do we want examples as well as definitions?

## To Do

* Add support for dumping to JSON
* Add threading, or some way to parallelize the work