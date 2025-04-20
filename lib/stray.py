from pystray import MenuItem as item
import pystray
import threading
from PIL import Image
import os

APP_NAME = "crawl2toast"

icon = None

def initialize():
    from lib.ui import deiconify

    global icon

    image = Image.open("public/icon.ico")
    menu = (item('설정 열기', deiconify), item('종료', exit_application))

    icon = pystray.Icon(APP_NAME, image, APP_NAME, menu)


def exit_application():
    if icon:
        icon.stop()
    os._exit(0)


def start():
    # multithreading for stray icon
    stray_thread = threading.Thread(target=icon.run)
    stray_thread.daemon = True
    stray_thread.start()


def stop():
    icon.stop()
    icon.visible = False