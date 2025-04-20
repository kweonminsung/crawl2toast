from lib import ui, settings, db, stray

def main():
    db.initialize()

    settings.initialize()

    stray.initialize()

    ui.initialize()

if __name__ == "__main__":
    main()