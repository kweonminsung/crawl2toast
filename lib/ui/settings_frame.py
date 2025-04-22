from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from lib.enums import SettingKey
from lib.constants import APP_NAME
from lib.db import Database, delete_all_histories, delete_all_logs
from lib.settings import get_settings, set_setting
from lib.crawler import request_crawl
from lib.scheduler import cancel_all_jobs, register_job
from lib.utils import time_to_int
import winreg
import os
import sys

recent_crawl_label: Label | None = None

crawl_interval_var: StringVar | None = None
apply_interval_button: Button | None = None
undo_interval_button: Button | None = None

crawling_status_label: Label | None = None
run_button: Button | None = None
stop_button: Button | None = None

iconify_onclose_checkbox_var: BooleanVar | None = None
stray_checkbox_var: BooleanVar | None = None
stray_checkbox: Checkbutton | None = None

def settings_frame(master: ttk.Notebook):
    from lib.ui import set_iconify_ondeletewindow_handler
    from lib.stray import start_stray

    global recent_crawl_label

    global crawl_interval_var
    global apply_interval_button
    global undo_interval_button

    global crawling_status_label
    global run_button
    global stop_button

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

    # ----------------------------------------------------------------
    sp1 = ttk.Separator(crawling_options_labelframe, orient='horizontal')
    sp1.pack(fill=X, padx=5, pady=5)
    # ----------------------------------------------------------------

    crawl_interval_label = Label(crawling_options_labelframe, text="크롤링 주기 설정 (HH:mm:ss 형식으로 입력)")
    crawl_interval_label.pack(padx=5, pady=1, anchor='w')


    crawl_interval_var = StringVar(value=settings[SettingKey.INTERVAL.value])
    crawl_interval_entry = Entry(crawling_options_labelframe, textvariable=crawl_interval_var, width=10)
    crawl_interval_entry.pack(padx=5, pady=2)

    interval_buttons_frame = Frame(crawling_options_labelframe)
    interval_buttons_frame.pack(padx=5, pady=2, fill=X, expand=True)
    
    apply_interval_button = Button(interval_buttons_frame, text="적용", width=15, command=apply_crawl_interval_button_handler)
    apply_interval_button.pack(side=LEFT, padx=2, pady=2, fill=X, expand=True)

    undo_interval_button = Button(interval_buttons_frame, text="되돌리기", width=15, command=undo_crawl_interval_button_handler)
    undo_interval_button.pack(side=RIGHT, padx=2, pady=2, fill=X, expand=True)

    # ----------------------------------------------------------------
    sp2 = ttk.Separator(crawling_options_labelframe, orient='horizontal')
    sp2.pack(fill=X, padx=5, pady=5)
    # ----------------------------------------------------------------

    crawling_panedwindow_label = Label(crawling_options_labelframe, text="크롤링 상태", width=10)
    crawling_panedwindow_label.pack(padx=5, pady=1, anchor='w')


    crawling_panedwindow = PanedWindow(crawling_options_labelframe, orient=HORIZONTAL, relief=RAISED, borderwidth=2)
    crawling_panedwindow.pack(fill=X, padx=5, pady=(2, 5))

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
    start_onboot_checkbox = Checkbutton(system_options_labelframe, text="윈도우 시작 시 실행", variable=start_onboot_checkbox_var, command=lambda: set_start_onboot(start_onboot_checkbox_var.get()))
    start_onboot_checkbox.pack(padx=5, pady=1, anchor='w')

    iconify_onclose_checkbox_var = BooleanVar(value=settings[SettingKey.ICONIFY_ONCLOSE.value])
    iconify_onclose_checkbox = Checkbutton(system_options_labelframe, text="X 버튼 클릭 시 창 최소화", variable=iconify_onclose_checkbox_var, command=iconify_onclose_checkbox_click_handler)
    iconify_onclose_checkbox.pack(padx=5, pady=1, anchor='w')

    stray_checkbox_var = BooleanVar(value=settings[SettingKey.STRAY.value])
    stray_checkbox = Checkbutton(system_options_labelframe, text="작업 표시줄에 아이콘 표시", variable=stray_checkbox_var, command=stray_checkbox_click_handler)
    stray_checkbox.config(state= "normal" if settings[SettingKey.ICONIFY_ONCLOSE.value] else "disabled")
    stray_checkbox.pack(padx=5, pady=(1, 5), anchor='w')

    set_iconify_ondeletewindow_handler(iconify_onclose_checkbox_var.get())

    if iconify_onclose_checkbox_var.get() and stray_checkbox_var.get():
        start_stray()

    # ----------------------------------------------------------------

    reset_options_labelframe = LabelFrame(settings_frame, text="초기화")
    reset_options_labelframe.pack(padx=5, fill=X)

    reset_history_button = Button(reset_options_labelframe, text="기록 초기화", command=reset_history_handler)
    reset_history_button.pack(fill=X, padx=5, pady=1)

    reset_log_button = Button(reset_options_labelframe, text="실행 로그 초기화", command=reset_log_handler)
    reset_log_button.pack(fill=X, padx=5, pady=(1, 5))


def set_operation(status):
    global crawling_status_label
    global run_button
    global stop_button

    if status:
        settings = get_settings()

        crawling_status_label.config(text="실행 중", fg="green")

        set_setting(SettingKey.RECENT_STATUS, True)

        run_button.config(state="disabled")
        stop_button.config(state="normal")

        apply_interval_button.config(state="disabled")
        undo_interval_button.config(state="disabled")

        register_job(request_crawl, time_to_int(settings[SettingKey.INTERVAL.value]))
    else:
        crawling_status_label.config(text="중지됨", fg="red")

        set_setting(SettingKey.RECENT_STATUS, False)
        
        run_button.config(state="normal")
        stop_button.config(state="disabled")

        apply_interval_button.config(state="normal")
        undo_interval_button.config(state="normal")

        cancel_all_jobs()


def set_recent_crawl(recent_crawl: datetime):
    global crawling_status_label

    recent_crawl_str = recent_crawl.strftime("%Y-%m-%d %H:%M:%S")

    recent_crawl_label.config(text=f"마지막 크롤링 시각 : {recent_crawl_str}")

    set_setting(SettingKey.RECENT_CRAWL, recent_crawl_str)


def apply_crawl_interval_button_handler():
    global crawl_interval_var

    interval = crawl_interval_var.get()

    try:
        # Validate the input format(HH:mm:ss)
        datetime.strptime(interval, "%H:%M:%S")
        
        set_setting(SettingKey.INTERVAL, interval)

        messagebox.showinfo("크롤링 주기 설정", f"크롤링 주기가 {interval}로 설정되었습니다.")
    except ValueError:
        messagebox.showerror("오류", "올바른 HH:mm:ss 형식으로 입력해주세요.")


def undo_crawl_interval_button_handler():
    global crawl_interval_var

    settings = get_settings()

    crawl_interval_var.set(settings[SettingKey.INTERVAL.value])


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


def set_start_onboot(start_onboot: bool):
    set_setting(SettingKey.START_ONBOOT, start_onboot)

    if start_onboot:
        set_start_onboot(True)
    else:
        set_start_onboot(False)


def iconify_onclose_checkbox_click_handler():
    from lib.ui import set_iconify_ondeletewindow_handler
    from lib.stray import start_stray

    global iconify_onclose_checkbox_var
    global stray_checkbox_var
    global stray_checkbox

    iconify_var = iconify_onclose_checkbox_var.get()

    set_setting(SettingKey.ICONIFY_ONCLOSE, iconify_var)

    if iconify_var:
        set_iconify_ondeletewindow_handler(True)
        stray_checkbox.config(state="normal")

        if stray_checkbox_var.get():
            start_stray()
    else:
        set_iconify_ondeletewindow_handler(False)
        stray_checkbox.config(state="disabled")



def stray_checkbox_click_handler():
    from lib.stray import start_stray, stop_stray
    
    global stray_checkbox_var

    stray_var = stray_checkbox_var.get()
    
    set_setting(SettingKey.STRAY, stray_var)

    if stray_var:
        start_stray()
    else:
        stop_stray()


def crawl_now_handler():
    if messagebox.askyesno("확인", "지금 긁어오시겠습니까?"):
        request_crawl()
        set_recent_crawl(datetime.now())


def reset_history_handler():
    if messagebox.askyesno("확인", "기록을 초기화하시겠습니까?"):
        delete_all_histories(Database().get_connection())

        from lib.ui.main_frame import reload_current_history_listbox
        reload_current_history_listbox()
        messagebox.showinfo("기록 초기화", "기록이 초기화되었습니다.")


def reset_log_handler():
    if messagebox.askyesno("확인", "실행 로그를 초기화하시겠습니까?"):
        delete_all_logs(Database().get_connection())
        messagebox.showinfo("실행 로그 초기화", "실행 로그가 초기화되었습니다.")