# Python Urban Dictionary Scraper (aka ubscrape)

This python script tries to scrape and store every single word and definition from Urban Dictionary.

```bash
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python ubscrape-runner.py # [args]
```

## Installation

## How ubscrape Works

1. ubscrape goes through the page indices looking for every word (https://www.urbandictionary.com/browse.php?character=A, https://www.urbandictionary.com/browse.php?character=A&page=2, etc). ubscrape adds these words to a SQLite database in a `words` table.

2. ubscrape goes through every row in the database and looks it up (https://www.urbandictionary.com/define.php?term=Magic%20Carpet%20Ride) and adds the definitions to a `definitions` table.

3. When ubscrape has added every definition for a word, it flags the word as `complete` and moves onto the next word.

4. When every word in ubscrape is complete, it dumps the SQLite database to JSON. Each letter gets its own folder, and then definitions are added to files in 50 MB groups. Each file will be ~50 MB, and the title will be the first and last word in the file (firstword-lastword.json).

If ubscrape crashes or fails, it will restart and try to redo as little work as possible.

## Questions

1. Do we want examples as well as definitions?

## To Do

- Add support for dumping at the same time as scraping, making it less linear.
- Add a version number to the CLI

## Limitations

- Cannot take escaped unicode characters as input to `--define`:

  - `ubscrape --define \u2764\ufe0f` does not work.
  - `ubscrape --define ❤️❤️` **DOES** work.

- Cannot dump to json while it's defining words.

## Parallelizing Work

- Using multiprocessing pool

Time of 100 words:
real 0m13.341s
real 0m12.922s
real 0m12.606s

Time of 0 words (testing for initialization):
real 0m3.033s
real 0m3.171s
real 0m2.893s

~13 and ~3 seem good enough for an estimate. 100 words takes 10 seconds, so 1.9 million words takes 0.19 million seconds.

0.19 \* 10 ^ 6 seconds / 60 sec/min / 60 min/hr / 24 hr/day = ~2.2 days

I could run it on my laptop for 6 hours a day, or I could run it on the school computers and get it done in two days (checking twice a day on progress).

## Building

1. Delete `build/`, `dist/`, `ubscrape.egg-info/`.

2. Bump version number in `ubscrape/setup.py`.

3. Activate your virtual environment, make sure everything is installed.

4. `python ubscrape/setup.py sdist bdist_wheel`

_Note to self_

- Activate global environment with `. ~/global_venv/bin/activate` before the next step.

5. Upload:

   - `twine upload --repository-url https://test.pypi.org/legacy/ dist/*` (test)
   - `twine upload dist/*` (real)

6. Download and test:

   - `pip install -i https://test.pypi.org/simple/ ubscrape==0.5` (test)
   - `pip install ubscrape` (real)

7. `ubscrape --help`
