import json

SETTINGS_FILE = 'source.json'

settings = None

def initialize():
    global settings
    
    try:
        with open(SETTINGS_FILE) as f:
            settings = json.load(f)
            print("Settings loaded successfully.")

            need_renderer = False
            for source in settings['source']:
                if source["render_options"]["render"] == True:
                    need_renderer = True
                    break

            if need_renderer:
                from lib.crawler import initialize_selenium_driver
                initialize_selenium_driver()
                
    except FileNotFoundError:
        raise Exception("Settings file not found.")
    except json.JSONDecodeError:
        raise Exception("Error decoding JSON from settings file.")

def get_settings():
    global settings

    if settings is None:
        raise Exception("Settings not initialized.")

    return settings