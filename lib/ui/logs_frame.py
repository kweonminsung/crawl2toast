from tkinter import *
from tkinter import ttk, messagebox
from lib import utils
from lib.db import Database, get_logs
from lib.constants import LOG_LOAD_LIMIT
from lib.i18n import t

log_offset: int = 0

log_listbox: Listbox | None = None

def logs_frame(master: ttk.Notebook):
    global log_listbox

    logs_frame = Frame(master)
    master.add(logs_frame, text=t('ui.notebook.logs.title'))

    log_listbox_scrollbar_y = ttk.Scrollbar(logs_frame)
    log_listbox_scrollbar_y.pack(side=RIGHT, fill=Y)
    log_listbox_scrollbar_y.config(command=log_listbox_scrollbar_y_onscroll_handler)

    log_listbox_scrollbar_x = ttk.Scrollbar(logs_frame, orient="horizontal")
    log_listbox_scrollbar_x.pack(side=BOTTOM, fill=X)

    log_listbox = Listbox(logs_frame, yscrollcommand=log_listbox_scrollbar_y.set, xscrollcommand=log_listbox_scrollbar_x.set)
    log_listbox.bind("<MouseWheel>", log_listbox_onscroll_handler)
    log_listbox.bind("<Double-1>", log_listbox_doubleclick_handler)
    log_listbox.pack(fill=BOTH, expand=True)
    log_listbox_scrollbar_x.config(command=log_listbox.xview)

    load_log_listbox()


def load_log_listbox():
    global log_listbox
    global log_offset

    log_offset = 0
    log_listbox.delete(0, END)

    logs = get_logs(Database().get_connection(), LOG_LOAD_LIMIT, log_offset)

    for log in logs:
        # log_listbox.insert(END, log)
        log_listbox.insert(END, f"""
{"✅" if log["ok"] else "❌"} {log['message']}

- Timestamp -
{utils.datetime_to_timestamp(log['timestamp'])}

- URL -
{log['url']}
""")
        log_listbox.itemconfig(END, {'bg': '#F0F0F0' if log['ok'] else '#f8D7DA', 'fg': '#000000' if log['ok'] else '#721C24'})


def log_listbox_load_more():
    global log_listbox
    global log_offset
    
    append_logs = get_logs(Database().get_connection(), LOG_LOAD_LIMIT, log_offset + LOG_LOAD_LIMIT)

    if len(append_logs) == 0:
        return

    log_offset += LOG_LOAD_LIMIT

    for log in append_logs:
        # log_listbox.insert(END, log[i])
        log_listbox.insert(END, f"""
{"✅" if log["ok"] else "❌"} {log['message']}

- Timestamp -
{utils.datetime_to_timestamp(log['timestamp'])}

- URL -
{log['url']}
""")
        log_listbox.itemconfig(END, {'bg': '#F0F0F0' if log['ok'] else '#f8D7DA', 'fg': '#000000' if log['ok'] else '#721C24'})

        

def log_listbox_scrollbar_y_onscroll_handler(*args):
    global log_listbox

    log_listbox.yview(*args)
    
    # Check scroll position
    pos = log_listbox.yview()
    # print(f"pos: {pos}")

    if pos[1] > 0.95:
        log_listbox_load_more()


def log_listbox_onscroll_handler(event):
    global log_listbox

    # Check scroll position
    pos = log_listbox.yview()
    # print(f"pos: {pos}")

    if pos[1] > 0.95:
        log_listbox_load_more()


def log_listbox_doubleclick_handler(event):
    global log_listbox

    selected_index = log_listbox.curselection()
    if not selected_index:
        return

    selected_log = log_listbox.get(selected_index[0])

    messagebox.showinfo(t('ui.notebook.logs.log_detail'), selected_log)