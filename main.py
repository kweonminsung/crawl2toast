from lib import ui, settings, stray, crawler
from lib.db import Database

def main():
    Database()

    settings.initialize()

    crawler.initialize()

    stray.initialize()

    ui.initialize()

if __name__ == "__main__":
    main()