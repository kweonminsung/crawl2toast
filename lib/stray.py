from pystray import MenuItem as item
import pystray
from PIL import Image
import os
from lib.ui import deiconify

APP_NAME = "crawl2toast"

icon = None

def initialize():
    global icon

    image = Image.open("public/icon.ico")
    menu = (item('설정 열기', deiconify), item('종료', exit_application))

    icon = pystray.Icon(APP_NAME, image, APP_NAME, menu)
    icon.run()


def exit_application():
    if icon:
        icon.stop()
    os._exit(0)


def destroy():
    icon.stop()
    icon.visible = False