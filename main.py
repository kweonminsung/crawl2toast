from lib import ui, settings, stray
import threading

def main():
    settings.initialize()

    # multithreading for stray icon
    stray_thread = threading.Thread(target=stray.initialize)
    stray_thread.daemon = True
    stray_thread.start()

    ui.initialize()

if __name__ == "__main__":
    main()