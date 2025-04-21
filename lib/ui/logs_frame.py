from tkinter import *
from tkinter import ttk

def logs_frame(master: ttk.Notebook):
    error_logs_frame = Frame(master)
    master.add(error_logs_frame, text='실행 로그')

    log_listbox = Listbox(error_logs_frame)
    log_listbox.pack(fill=BOTH, expand=True)