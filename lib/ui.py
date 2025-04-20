from tkinter import *
from tkinter import ttk, messagebox
from win10toast import ToastNotifier
from lib import crawler, stray, db
from lib.enums import SettingKey
import winreg
import os
import sys

APP_NAME = "crawl2toast"

toaster = ToastNotifier()

root = None
log_listbox = None
start_onboot_checkbox_var = None
iconify_onclose_checkbox_var = None
stray_checkbox_var = None
stray_checkbox = None

def deiconify():
    root.deiconify()
    root.lift()
    root.focus_force()


def set_start_onboot(enable: bool):
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE
    )
    if enable:
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, os.path.abspath(sys.argv[0]))
    else:
        try:
            winreg.DeleteValue(key, APP_NAME)
        except FileNotFoundError:
            pass
    winreg.CloseKey(key)


def start_onboot_checkbox_click_handler():
    start_onboot_var = start_onboot_checkbox_var.get()
    db.set_setting(SettingKey.START_ONBOOT, start_onboot_var)

    if start_onboot_var:
        set_start_onboot(True)
    else:
        set_start_onboot(False)


def iconify_onclose_checkbox_click_handler():
    iconify_var = iconify_onclose_checkbox_var.get()
    db.set_setting(SettingKey.ICONIFY_ONCLOSE, iconify_var)

    if iconify_var:
        root.protocol("WM_DELETE_WINDOW", root.iconify)
        stray_checkbox.config(state="normal")
    else:
        root.protocol("WM_DELETE_WINDOW", root.quit)
        stray_checkbox.config(state="disabled")
        stray_checkbox_var.set(False)


def stray_checkbox_click_handler():
    stray_var = stray_checkbox_var.get()
    db.set_setting(SettingKey.STRAY, stray_var)

    if stray_var:
        stray.start()
    else:
        stray.stop()

def test():
    result = crawler.crawl()
    print(result)
    # toaster.show_toast(result[])
    

def initialize():
    from lib.settings import get_settings

    global root
    global log_listbox
    global start_onboot_checkbox_var
    global iconify_onclose_checkbox_var
    global stray_checkbox_var
    global stray_checkbox

    settings = get_settings()

    root = Tk()
    root.title(APP_NAME)
    root.iconbitmap('public/icon.ico')
    root.geometry('300x400')
    root.attributes('-fullscreen', False)
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill=BOTH)

    # ----------------------------------------------------------------

    main_frame = Frame(notebook)
    notebook.add(main_frame, text='메인')

    run_button = Button(main_frame, text="실행")
    run_button.pack(pady=20)

    stop_button = Button(main_frame, text="중지")
    stop_button.pack(pady=20)

    
    toast_button = Button(root, text="Toast", command=test)
    toast_button.pack(pady=20)


    # ----------------------------------------------------------------
    
    settings_frame = Frame(notebook)
    notebook.add(settings_frame, text='설정')

    start_onboot_checkbox_var = BooleanVar(value=settings[SettingKey.START_ONBOOT.value])
    start_onboot_checkbox = Checkbutton(settings_frame, text="윈도우 시작 시 실행", variable=start_onboot_checkbox_var, command=start_onboot_checkbox_click_handler)
    start_onboot_checkbox.pack(pady=20)

    iconify_onclose_checkbox_var = BooleanVar(value=settings[SettingKey.ICONIFY_ONCLOSE.value])
    iconify_onclose_checkbox = Checkbutton(settings_frame, text="X 버튼 클릭 시 창 최소화", variable=iconify_onclose_checkbox_var, command=iconify_onclose_checkbox_click_handler)
    iconify_onclose_checkbox.pack(pady=20)

    stray_checkbox_var = BooleanVar(value=settings[SettingKey.STRAY.value])
    stray_checkbox = Checkbutton(settings_frame, text="작업 표시줄에 아이콘 표시", variable=stray_checkbox_var, command=stray_checkbox_click_handler)
    stray_checkbox.config(state= "disabled" if settings[SettingKey.ICONIFY_ONCLOSE.value] else "normal")
    stray_checkbox.pack(pady=20)

    reset_history_button = Button(settings_frame, text="기록 초기화", command=lambda: messagebox.showinfo("로그 초기화", "로그가 초기화되었습니다."))
    reset_history_button.pack(pady=20)

    # ----------------------------------------------------------------
    logs_frame = Frame(notebook)
    notebook.add(logs_frame, text='로그')

    log_listbox = Listbox(logs_frame)
    log_listbox.pack(fill=BOTH, expand=True)

    root.mainloop()