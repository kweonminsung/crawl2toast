from tkinter import *
from tkinter import ttk, messagebox
from win10toast import ToastNotifier
from lib import crawler, stray, db, utils
from lib.enums import SettingKey
import winreg
import os
import sys

APP_NAME = "crawl2toast"
HISTORY_LIMIT = 10

toaster = ToastNotifier()

selected_url = None
history_offset = 0

root = None
log_listbox = None
start_onboot_checkbox_var = None
iconify_onclose_checkbox_var = None
stray_checkbox_var = None
stray_checkbox = None
url_listbox = None
history_listbox = None

def deiconify():
    root.deiconify()
    root.lift()
    root.focus_force()


def url_listbox_click_handler(event):
    global selected_url
    global history_offset
    
    history_offset = 0

    selected_index = url_listbox.curselection()
    if not selected_index:
        return
    selected_url = selected_index[0]

    histories = db.get_histories(url_listbox.get(selected_url), HISTORY_LIMIT, history_offset)

    history_listbox.delete(0, END)
    for history in histories:
        history_listbox.insert(END, history)
        # history_listbox.insert(END, f"{utils.timestamp_to_datetime(history['timestamp'])} - {history['title']}")


def history_listbox_load_more():
    global history_listbox
    global selected_url
    global history_offset
    
    append_histories = db.get_histories(url_listbox.get(selected_url), HISTORY_LIMIT, history_offset + HISTORY_LIMIT)
    print(f"append_histories: {len(append_histories)}")

    if len(append_histories) == 0:
        return

    history_offset += HISTORY_LIMIT

    for i in range(len(append_histories)):
        history_listbox.insert(END, append_histories[i])
        # history_listbox.insert(END, f"{utils.timestamp_to_datetime(histories[history_offset]['timestamp'])} - {histories[history_offset]['title']}")
        

def history_listbox_scrollbar_onscroll_handler(*args):
    global history_listbox

    history_listbox.yview(*args)
    
    # Check scroll position
    pos = history_listbox.yview()
    print(f"pos: {pos}")

    if pos[1] > 0.95:
        history_listbox_load_more()


def history_listbox_onscroll_handler(event):
    global history_listbox

    # Check scroll position
    pos = history_listbox.yview()
    print(f"pos: {pos}")

    if pos[1] > 0.95:
        history_listbox_load_more()


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
    global iconify_onclose_checkbox_var
    global stray_checkbox_var
    global stray_checkbox

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
    global stray_checkbox_var

    stray_var = stray_checkbox_var.get()
    db.set_setting(SettingKey.STRAY, stray_var)

    if stray_var:
        stray.start()
    else:
        stray.stop()
    

def initialize():
    from lib.settings import get_settings

    global root
    global log_listbox
    global start_onboot_checkbox_var
    global iconify_onclose_checkbox_var
    global stray_checkbox_var
    global stray_checkbox
    global url_listbox
    global history_listbox

    settings = get_settings()

    root = Tk()
    root.title(APP_NAME)
    root.iconbitmap('public/icon.ico')
    root.geometry('400x600')
    root.attributes('-fullscreen', False)
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill=BOTH)

    # ----------------------------------------------------------------

    main_frame = Frame(notebook)
    notebook.add(main_frame, text='기록')


    url_frame = Frame(main_frame)
    url_frame.pack(fill=X)

    url_label = Label(url_frame, text="URL", anchor='w')
    url_label.pack(fill=X, padx=3)

    url_listbox_scrollbar = ttk.Scrollbar(url_frame)
    url_listbox_scrollbar.pack(side=RIGHT, fill=Y)
    url_listbox = Listbox(url_frame, height=5, yscrollcommand=url_listbox_scrollbar.set)
    url_listbox.pack(fill=X)

    url_listbox.bind('<<ListboxSelect>>', url_listbox_click_handler)
    url_listbox.insert(0, "https://example.com")
    url_listbox.insert(1, "https://example.com")    
    url_listbox.insert(2, "https://example.com")
    url_listbox.insert(3, "https://example.com")
    url_listbox.insert(4, "https://example.com")
    url_listbox.insert(5, "https://example.com")
    url_listbox.insert(6, "https://example.com")
    url_listbox.insert(7, "https://example.com")
    url_listbox.insert(8, "https://example.com")
    url_listbox.insert(9, "https://example.com")
    

    sp1 = ttk.Separator(main_frame, orient='horizontal')
    sp1.pack(fill=X)


    history_frame = Frame(main_frame)
    # history_frame.pack(fill=BOTH, expand=True)
    history_frame.pack(fill=X)

    history_label = Label(history_frame, text="기록", anchor='w')
    history_label.pack(fill=X, padx=3)

    history_listbox_scrollbar = ttk.Scrollbar(history_frame)
    history_listbox_scrollbar.pack(side=RIGHT, fill=Y)
    history_listbox_scrollbar.config(command=history_listbox_scrollbar_onscroll_handler)
    history_listbox = Listbox(history_frame, yscrollcommand=history_listbox_scrollbar.set, height=9)
    history_listbox.bind("<MouseWheel>", history_listbox_onscroll_handler)
    # history_listbox.pack(fill=BOTH, expand=True)
    history_listbox.pack(fill=X)



    # ----------------------------------------------------------------
    
    settings_frame = Frame(notebook)
    notebook.add(settings_frame, text='설정')

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

    # ----------------------------------------------------------------
    logs_frame = Frame(notebook)
    notebook.add(logs_frame, text='실패 로그')

    log_listbox = Listbox(logs_frame)
    log_listbox.pack(fill=BOTH, expand=True)

    root.mainloop()