from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from lib.enums import SettingKey, Language
from lib.constants import APP_NAME
from lib.db import Database, delete_all_histories, delete_all_logs
from lib.settings import get_settings, set_setting
from lib.crawler import request_crawl
from lib.scheduler import cancel_all_jobs, register_job
from lib.utils import time_to_int
from lib.i18n import t
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

language_combobox: ttk.Combobox | None = None

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

    global language_combobox

    settings = get_settings()

    settings_frame = Frame(master)
    master.add(settings_frame, text=t('ui.notebook.settings.title'))

    # ----------------------------------------------------------------

    crawling_options_labelframe = LabelFrame(settings_frame, text=t('ui.notebook.settings.crawling_options.title'))
    crawling_options_labelframe.pack(padx=5, fill=X)

    recent_crawl_label = Label(crawling_options_labelframe, text=f"{t('ui.notebook.settings.crawling_options.recent_crawl.title')} : {t('ui.notebook.settings.crawling_options.recent_crawl.loading')}")
    recent_crawl_label.pack(padx=5, pady=1, anchor='w')

    crawl_now_button = Button(crawling_options_labelframe, text=t('ui.notebook.settings.crawling_options.recent_crawl.crawl_now'), command=crawl_now_handler)
    crawl_now_button.pack(padx=5, pady=2, fill=X, expand=True)

    # ----------------------------------------------------------------
    sp1 = ttk.Separator(crawling_options_labelframe, orient='horizontal')
    sp1.pack(fill=X, padx=5, pady=5)
    # ----------------------------------------------------------------

    crawl_interval_label = Label(crawling_options_labelframe, text=t('ui.notebook.settings.crawling_options.crawl_interval.title'))
    crawl_interval_label.pack(padx=5, pady=1, anchor='w')


    crawl_interval_var = StringVar(value=settings[SettingKey.INTERVAL])
    crawl_interval_entry = Entry(crawling_options_labelframe, textvariable=crawl_interval_var, width=10)
    crawl_interval_entry.pack(padx=5, pady=2)

    interval_buttons_frame = Frame(crawling_options_labelframe)
    interval_buttons_frame.pack(padx=5, pady=2, fill=X, expand=True)
    
    apply_interval_button = Button(interval_buttons_frame, text=t('ui.notebook.settings.crawling_options.crawl_interval.apply_interval'), width=15, command=apply_crawl_interval_button_handler)
    apply_interval_button.pack(side=LEFT, padx=2, pady=2, fill=X, expand=True)

    undo_interval_button = Button(interval_buttons_frame, text=t('ui.notebook.settings.crawling_options.crawl_interval.undo_interval'), width=15, command=undo_crawl_interval_button_handler)
    undo_interval_button.pack(side=RIGHT, padx=2, pady=2, fill=X, expand=True)

    # ----------------------------------------------------------------
    sp2 = ttk.Separator(crawling_options_labelframe, orient='horizontal')
    sp2.pack(fill=X, padx=5, pady=5)
    # ----------------------------------------------------------------

    crawling_panedwindow_label = Label(crawling_options_labelframe, text=t('ui.notebook.settings.crawling_options.crawling_status.title'))
    crawling_panedwindow_label.pack(padx=5, pady=1, anchor='w')


    crawling_panedwindow = PanedWindow(crawling_options_labelframe, orient=HORIZONTAL, relief=RAISED, borderwidth=2)
    crawling_panedwindow.pack(fill=X, padx=5, pady=(2, 5))

    crawling_status_label = Label(crawling_panedwindow, text=t('ui.notebook.settings.crawling_options.crawling_status.loading'), fg="orange", width=10)
    crawling_status_label.pack(side=LEFT, padx=2, fill=X, expand=True)
    
    run_button = Button(crawling_panedwindow, text=t('ui.notebook.settings.crawling_options.crawling_status.run'), command=lambda: set_crawling_status(True))
    run_button.pack(side=LEFT, padx=2, pady=2, fill=X, expand=True)
    run_button.config(state="disabled")

    stop_button = Button(crawling_panedwindow, text=t('ui.notebook.settings.crawling_options.crawling_status.stop'), command=lambda: set_crawling_status(False))
    stop_button.pack(side=RIGHT, padx=2, pady=2, fill=X, expand=True)
    stop_button.config(state="disabled")
    
    set_recent_crawl(settings[SettingKey.RECENT_CRAWL])
    set_crawling_status(settings[SettingKey.RECENT_STATUS])

    # ----------------------------------------------------------------

    system_options_labelframe = LabelFrame(settings_frame, text=t('ui.notebook.settings.system_options.title'))
    system_options_labelframe.pack(padx=5, fill=X)

    start_onboot_checkbox_var = BooleanVar(value=settings[SettingKey.START_ONBOOT])
    start_onboot_checkbox = Checkbutton(system_options_labelframe, text=t('ui.notebook.settings.system_options.start_onboot'), variable=start_onboot_checkbox_var, command=lambda: set_start_onboot(start_onboot_checkbox_var.get()))
    start_onboot_checkbox.pack(padx=5, pady=1, anchor='w')

    iconify_onclose_checkbox_var = BooleanVar(value=settings[SettingKey.ICONIFY_ONCLOSE])
    iconify_onclose_checkbox = Checkbutton(system_options_labelframe, text=t('ui.notebook.settings.system_options.iconify_onclose'), variable=iconify_onclose_checkbox_var, command=iconify_onclose_checkbox_click_handler)
    iconify_onclose_checkbox.pack(padx=5, pady=1, anchor='w')

    stray_checkbox_var = BooleanVar(value=settings[SettingKey.STRAY])
    stray_checkbox = Checkbutton(system_options_labelframe, text=t('ui.notebook.settings.system_options.stray'), variable=stray_checkbox_var, command=stray_checkbox_click_handler)
    stray_checkbox.config(state= "normal" if settings[SettingKey.ICONIFY_ONCLOSE] else "disabled")
    stray_checkbox.pack(padx=5, pady=(1, 5), anchor='w')

    set_iconify_ondeletewindow_handler(iconify_onclose_checkbox_var.get())

    if iconify_onclose_checkbox_var.get() and stray_checkbox_var.get():
        start_stray()

    # ----------------------------------------------------------------
    sp3 = ttk.Separator(system_options_labelframe, orient='horizontal')
    sp3.pack(fill=X, padx=5, pady=5)
    # ----------------------------------------------------------------

    language_label = Label(system_options_labelframe, text=t('ui.notebook.settings.system_options.language.title'))
    language_label.pack(padx=5, pady=1, anchor='w')
        
    language_combobox = ttk.Combobox(system_options_labelframe, values=[lang.to_native() for lang in Language], state='readonly', width=15)
    language_combobox.bind("<<ComboboxSelected>>", set_language_handler)
    language_combobox.pack(padx=10, pady=(1, 5), anchor='w')
    
    language_combobox.current([lang.to_native() for lang in Language].index(settings[SettingKey.LANGUAGE].to_native()))

    # ----------------------------------------------------------------

    reset_options_labelframe = LabelFrame(settings_frame, text=t('ui.notebook.settings.reset_options.title'))
    reset_options_labelframe.pack(padx=5, fill=X)

    reset_history_button = Button(reset_options_labelframe, text=t('ui.notebook.settings.reset_options.reset_history'), command=reset_history_handler)
    reset_history_button.pack(fill=X, padx=5, pady=1)

    reset_log_button = Button(reset_options_labelframe, text=t('ui.notebook.settings.reset_options.reset_log'), command=reset_log_handler)
    reset_log_button.pack(fill=X, padx=5, pady=(1, 5))


def set_crawling_status(status):
    global crawling_status_label
    global run_button
    global stop_button

    if status:
        settings = get_settings()

        crawling_status_label.config(text=t('ui.notebook.settings.crawling_options.crawling_status.running'), fg="green")

        set_setting(SettingKey.RECENT_STATUS, True)

        run_button.config(state="disabled")
        stop_button.config(state="normal")

        apply_interval_button.config(state="disabled")
        undo_interval_button.config(state="disabled")

        register_job(request_crawl, time_to_int(settings[SettingKey.INTERVAL]))
    else:
        crawling_status_label.config(text=t('ui.notebook.settings.crawling_options.crawling_status.stopped'), fg="red")

        set_setting(SettingKey.RECENT_STATUS, False)
        
        run_button.config(state="normal")
        stop_button.config(state="disabled")

        apply_interval_button.config(state="normal")
        undo_interval_button.config(state="normal")

        cancel_all_jobs()


def set_recent_crawl(recent_crawl: datetime):
    global crawling_status_label

    recent_crawl_str = recent_crawl.strftime("%Y-%m-%d %H:%M:%S")

    recent_crawl_label.config(text=f"{t('ui.notebook.settings.crawling_options.recent_crawl.title')} : {recent_crawl_str}")

    set_setting(SettingKey.RECENT_CRAWL, recent_crawl_str)


def apply_crawl_interval_button_handler():
    global crawl_interval_var

    interval = crawl_interval_var.get()

    try:
        # Validate the input format(HH:mm:ss)
        datetime.strptime(interval, "%H:%M:%S")
        
        set_setting(SettingKey.INTERVAL, interval)

        messagebox.showinfo(t('message.title.info'), t('ui.notebook.settings.crawling_options.crawl_interval.message.applied'))
    except ValueError:
        messagebox.showerror(t('message.title.error'), t('ui.notebook.settings.crawling_options.crawl_interval.message.error'))


def undo_crawl_interval_button_handler():
    global crawl_interval_var

    settings = get_settings()

    crawl_interval_var.set(settings[SettingKey.INTERVAL])


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
    if messagebox.askyesno(t('message.title.confirm'), t('ui.notebook.settings.crawling_options.recent_crawl.message.crawl_now')) is True:
        request_crawl()
        set_recent_crawl(datetime.now())


def set_language_handler(event):
    from lib.i18n import set_language
    from lib.ui import refresh
    
    global language_combobox

    settings = get_settings()

    if settings[SettingKey.LANGUAGE] == Language.from_native(language_combobox.get()):
        return

    if messagebox.askyesno(t('message.title.confirm'), t('ui.notebook.settings.system_options.language.message.apply')) is True:
        selected_language = language_combobox.get()

        set_language(Language.from_native(selected_language))

        if messagebox.askyesno(t('message.title.info'), t('ui.notebook.settings.system_options.language.message.restart')):
            refresh()
            
    else:
        language_combobox.current([lang.to_native() for lang in Language].index(settings[SettingKey.LANGUAGE].to_native()))

def reset_history_handler():
    from lib.ui.main_frame import reload_current_history_listbox
    
    if messagebox.askyesno(t('message.title.confirm'), t('ui.notebook.settings.reset_options.message.reset_history')) is True:
        delete_all_histories(Database().get_connection())

        reload_current_history_listbox()
        messagebox.showinfo(t('message.title.info'), t('ui.notebook.settings.reset_options.message.reset_history_success'))


def reset_log_handler():
    if messagebox.askyesno(t('message.title.confirm'), t('ui.notebook.settings.reset_options.message.reset_log')) is True:
        delete_all_logs(Database().get_connection())
        messagebox.showinfo(t('message.title.info'), t('ui.notebook.settings.reset_options.message.reset_log_success'))