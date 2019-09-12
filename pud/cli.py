from definitions import define_all_words, write_definition
from words import write_all_words
from db import initialize_db, clear_database, dump_database
import argparse


def scrape():
    con = initialize_db()
    write_all_words(con)
    define_all_words()
    con.close()


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",
                        "--scrape",
                        help="Continues scraping Urban Dictionary using the SQLite database as its starting point.",
                        action="store_true")
    parser.add_argument('-d',
                        '--dump',
                        action='store_true',
                        help="Dumps the SQLite database to .json files.")

    parser.add_argument('-o',
                        '--out',
                        dest='dump',
                        help="Specifies the directory for --dump.")

    parser.add_argument("--define",
                        help="Look up a particular word and define it.")
    parser.add_argument("--define-all",
                        help="Define all words currently stored in SQLite that are not defined.",
                        action="store_true")
    parser.add_argument("-c",
                        "--clear",
                        help="Clears the existing SQLite database.",
                        action="store_true")
    parser.add_argument("-f",
                        "--force",
                        help="Forces the SQLite database to be cleared.",
                        action="store_true")

    args = parser.parse_args()

    if args.scrape:
        scrape()
    elif args.dump:
        dump_database(args.dump)
    elif args.define:
        definitions = write_definition(args.define)
        print(definitions)
    elif args.define_all:
        define_all_words()
    elif args.clear:
        if args.force:
            clear_database()
        else:
            print(
                "Use --clear [-c] with --force [-f] to COMPLETELY DELETE the SQLite database.")
    else:
        print('No arguments detected. Continuing to scrape.')
        scrape()


if __name__ == "__main__":
    cli()
