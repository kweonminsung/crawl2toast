from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from lib.enums import SettingKey
from lib.constants import APP_NAME
from lib import stray
from lib.db import Database, set_setting
from lib.settings import get_settings
from lib.crawler import request_crawl
from lib.scheduler import cancel_all_jobs, register_job
from lib.utils import time_to_int
import winreg
import os
import sys

recent_crawl_label: Label | None = None

crawling_status_label: Label | None = None
run_button: Button | None = None
stop_button: Button | None = None

start_onboot_checkbox_var: BooleanVar | None = None
iconify_onclose_checkbox_var: BooleanVar | None = None
stray_checkbox_var: BooleanVar | None = None
stray_checkbox: Checkbutton | None = None

def settings_frame(master: ttk.Notebook):
    global recent_crawl_label

    global crawling_status_label
    global run_button
    global stop_button

    global start_onboot_checkbox_var
    global iconify_onclose_checkbox_var
    global stray_checkbox_var
    global stray_checkbox

    settings = get_settings()

    settings_frame = Frame(master)
    master.add(settings_frame, text='설정')

    # ----------------------------------------------------------------

    crawling_options_labelframe = LabelFrame(settings_frame, text="크롤링 옵션")
    crawling_options_labelframe.pack(padx=5, fill=X)

    recent_crawl_label = Label(crawling_options_labelframe, text="마지막 크롤링 시각 : 로드 중")
    recent_crawl_label.pack(padx=5, pady=1, anchor='w')


    crawl_now_button = Button(crawling_options_labelframe, text="지금 긁어오기", command=crawl_now_handler)
    crawl_now_button.pack(padx=5, pady=2, fill=X, expand=True)


    crawling_panedwindow = PanedWindow(crawling_options_labelframe, orient=HORIZONTAL, relief=RAISED, borderwidth=2)
    crawling_panedwindow.pack(fill=X, padx=5, pady=5)

    crawling_status_label = Label(crawling_panedwindow, text="로드 중", fg="orange", width=10)
    crawling_status_label.pack(side=LEFT, padx=2, fill=X, expand=True)
    
    run_button = Button(crawling_panedwindow, text="실행", command=lambda: set_operation(True))
    run_button.pack(side=LEFT, padx=2, pady=2, fill=X, expand=True)
    run_button.config(state="disabled")

    stop_button = Button(crawling_panedwindow, text="중지", command=lambda: set_operation(False))
    stop_button.pack(side=RIGHT, padx=2, pady=2, fill=X, expand=True)
    stop_button.config(state="disabled")
    
    set_recent_crawl(settings[SettingKey.RECENT_CRAWL.value])
    set_operation(settings[SettingKey.RECENT_STATUS.value])

    # ----------------------------------------------------------------

    system_options_labelframe = LabelFrame(settings_frame, text="시스템 옵션")
    system_options_labelframe.pack(padx=5, fill=X)

    start_onboot_checkbox_var = BooleanVar(value=settings[SettingKey.START_ONBOOT.value])
    start_onboot_checkbox = Checkbutton(system_options_labelframe, text="윈도우 시작 시 실행", variable=start_onboot_checkbox_var, command=start_onboot_checkbox_click_handler)
    start_onboot_checkbox.pack(padx=5, pady=1, anchor='w')

    iconify_onclose_checkbox_var = BooleanVar(value=settings[SettingKey.ICONIFY_ONCLOSE.value])
    iconify_onclose_checkbox = Checkbutton(system_options_labelframe, text="X 버튼 클릭 시 창 최소화", variable=iconify_onclose_checkbox_var, command=iconify_onclose_checkbox_click_handler)
    iconify_onclose_checkbox.pack(padx=5, pady=1, anchor='w')

    stray_checkbox_var = BooleanVar(value=settings[SettingKey.STRAY.value])
    stray_checkbox = Checkbutton(system_options_labelframe, text="작업 표시줄에 아이콘 표시", variable=stray_checkbox_var, command=stray_checkbox_click_handler)
    stray_checkbox.config(state= "normal" if settings[SettingKey.ICONIFY_ONCLOSE.value] else "disabled")
    stray_checkbox.pack(padx=5, pady=(1, 5), anchor='w')

    if iconify_onclose_checkbox_var.get() and stray_checkbox_var.get():
        stray.start()

    # ----------------------------------------------------------------

    reset_options_labelframe = LabelFrame(settings_frame, text="초기화")
    reset_options_labelframe.pack(padx=5, fill=X)

    reset_history_button = Button(reset_options_labelframe, text="기록 초기화", command=lambda: messagebox.showinfo("기록 초기화", "기록이 초기화되었습니다."))
    reset_history_button.pack(fill=X, padx=5, pady=1)

    reset_log_button = Button(reset_options_labelframe, text="실패 로그 초기화", command=lambda: messagebox.showinfo("실패 로그 초기화", "실패 로그가 초기화되었습니다."))
    reset_log_button.pack(fill=X, padx=5, pady=(1, 5))


def set_operation(status):
    global crawling_status_label
    global run_button
    global stop_button

    if status:
        settings = get_settings()

        crawling_status_label.config(text="실행 중", fg="green")
        set_setting(Database().get_connection(), SettingKey.RECENT_STATUS, True)
        run_button.config(state="disabled")
        stop_button.config(state="normal")

        register_job(request_crawl, time_to_int(settings[SettingKey.INTERVAL.value]))
    else:
        crawling_status_label.config(text="중지됨", fg="red")
        set_setting(Database().get_connection(), SettingKey.RECENT_STATUS, False)
        run_button.config(state="normal")
        stop_button.config(state="disabled")

        cancel_all_jobs()


def set_recent_crawl(recent_crawl: datetime):
    global crawling_status_label

    recent_crawl_str = recent_crawl.strftime("%Y-%m-%d %H:%M:%S")

    recent_crawl_label.config(text=f"마지막 크롤링 시각 : {recent_crawl_str}")
    set_setting(Database().get_connection(), SettingKey.RECENT_CRAWL, recent_crawl_str)


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

    set_setting(Database().get_connection(), SettingKey.START_ONBOOT, start_onboot_var)

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
    set_setting(Database().get_connection(), SettingKey.ICONIFY_ONCLOSE, iconify_var)

    if iconify_var:
        set_delete_window_handler(False)
        stray_checkbox.config(state="normal")

        if stray_checkbox_var.get():
            stray.start()
    else:
        set_delete_window_handler(True)
        stray_checkbox.config(state="disabled")



def stray_checkbox_click_handler():
    global stray_checkbox_var

    stray_var = stray_checkbox_var.get()
    set_setting(Database().get_connection(), SettingKey.STRAY, stray_var)

    if stray_var:
        stray.start()
    else:
        stray.stop()


def crawl_now_handler():
    if messagebox.askyesno("확인", "지금 긁어오시겠습니까?"):
        request_crawl()
        set_recent_crawl(datetime.now())