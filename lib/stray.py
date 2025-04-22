from pystray import MenuItem as item
import pystray
import threading
from PIL import Image
import os
from lib.utils import get_path
from lib.constants import APP_NAME

icon = None
icon_lock = threading.Lock()

def initialize():
    from lib.ui import deiconify
    from lib.ui.settings_frame import crawl_now_handler

    global icon

    image = Image.open(get_path("public/icon.ico"))
    menu = (item('지금 긁어오기', crawl_now_handler), item('설정 열기', deiconify), item('종료', exit_application))

    icon = pystray.Icon(APP_NAME, image, APP_NAME, menu)


def exit_application():
    global icon

    if icon:
        icon.stop()
    os._exit(0)


def start_stray():
    global icon

    with icon_lock:
        if icon is None or not icon.visible:
            initialize()
            stray_thread = threading.Thread(target=icon.run)
            stray_thread.daemon = True
            stray_thread.start()


def stop_stray():
    global icon

    with icon_lock:
        if icon and icon.visible:
            icon.stop()
            icon.visible = False