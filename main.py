from lib import ui, settings, stray, crawler, scheduler
from lib.db import Database

def main():
    # Do not change the order
    Database()

    settings.initialize()

    scheduler.initialize()

    crawler.initialize()

    stray.initialize()

    ui.initialize()

if __name__ == "__main__":
    main()