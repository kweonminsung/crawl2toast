from tkinter import *
from tkinter import ttk, messagebox
from lib.enums import SettingKey
from lib.constants import APP_NAME
from lib import stray, db
import winreg
import os
import sys

start_onboot_checkbox_var = None
iconify_onclose_checkbox_var = None
stray_checkbox_var = None
stray_checkbox = None

def settings_frame(master: ttk.Notebook):
    from lib.settings import get_settings

    global start_onboot_checkbox_var
    global iconify_onclose_checkbox_var
    global stray_checkbox_var
    global stray_checkbox

    settings = get_settings()

    settings_frame = Frame(master)
    master.add(settings_frame, text='설정')

    run_button = Button(settings_frame, text="실행")
    run_button.pack(pady=20)

    stop_button = Button(settings_frame, text="중지")
    stop_button.pack(pady=20)

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

    reset_history_button = Button(settings_frame, text="기록 초기화", command=lambda: messagebox.showinfo("기록 초기화", "기록이 초기화되었습니다."))
    reset_history_button.pack(pady=20)

    reset_error_log_button = Button(settings_frame, text="실패 로그 초기화", command=lambda: messagebox.showinfo("실패 로그 초기화", "실패 로그가 초기화되었습니다."))
    reset_error_log_button.pack(pady=20)


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
    global start_onboot_checkbox_var

    start_onboot_var = start_onboot_checkbox_var.get()
    db.set_setting(SettingKey.START_ONBOOT, start_onboot_var)

    if start_onboot_var:
        set_start_onboot(True)
    else:
        set_start_onboot(False)


def iconify_onclose_checkbox_click_handler():
    from lib.ui import set_delete_window_handler

    global iconify_onclose_checkbox_var
    global stray_checkbox_var
    global stray_checkbox

    iconify_var = iconify_onclose_checkbox_var.get()
    db.set_setting(SettingKey.ICONIFY_ONCLOSE, iconify_var)

    if iconify_var:
        set_delete_window_handler(False)
        stray_checkbox.config(state="normal")
    else:
        set_delete_window_handler(True)
        stray_checkbox.config(state="disabled")
        stray_checkbox_var.set(False)


def stray_checkbox_click_handler():
    global stray_checkbox_var

    stray_var = stray_checkbox_var.get()
    db.set_setting(SettingKey.STRAY, stray_var)

    if stray_var:
        stray.start()
    else:
        stray.stop()