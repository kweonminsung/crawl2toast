from tkinter import *

def error_logs_frame(master):
    error_logs_frame = Frame(master)
    master.add(error_logs_frame, text='실패 로그')

    log_listbox = Listbox(error_logs_frame)
    log_listbox.pack(fill=BOTH, expand=True)