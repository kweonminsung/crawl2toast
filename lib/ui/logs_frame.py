from tkinter import *
from tkinter import ttk
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

    log_listbox_scrollbar = ttk.Scrollbar(logs_frame)
    log_listbox_scrollbar.pack(side=RIGHT, fill=Y)
    log_listbox_scrollbar.config(command=log_listbox_scrollbar_onscroll_handler)
    log_listbox = Listbox(logs_frame, yscrollcommand=log_listbox_scrollbar.set)
    log_listbox.bind("<MouseWheel>", log_listbox_onscroll_handler)
    log_listbox.pack(fill=BOTH, expand=True)

    load_log_listbox()


def load_log_listbox():
    global log_listbox
    global log_offset

    log_offset = 0
    log_listbox.delete(0, END)

    logs = get_logs(Database().get_connection(), LOG_LOAD_LIMIT, log_offset)

    for log in logs:
        # log_listbox.insert(END, log)
        log_listbox.insert(END, f"{"✅" if log["ok"] else "❌"} {utils.datetime_to_timestamp(log['timestamp'])} - {log['message']}")


def log_listbox_load_more():
    global log_listbox
    global log_offset
    
    append_logs = get_logs(Database().get_connection(), LOG_LOAD_LIMIT, log_offset + LOG_LOAD_LIMIT)

    if len(append_logs) == 0:
        return

    log_offset += LOG_LOAD_LIMIT

    for i in range(len(append_logs)):
        # log_listbox.insert(END, append_logs[i])
        log_listbox.insert(END, f"{"✅" if append_logs[i]['ok'] else "❌"} {utils.datetime_to_timestamp(append_logs[i]['timestamp'])} - {append_logs[i]['message']}")
        

def log_listbox_scrollbar_onscroll_handler(*args):
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
    