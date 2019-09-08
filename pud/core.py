import re
from db import initialize_db
from constants import BASE_URL
from words import write_all_words
from definitions import define_all_words


def main():
    con = initialize_db()

    write_all_words(con)
    define_all_words(con)
    con.close()


if __name__ == "__main__":
    main()
