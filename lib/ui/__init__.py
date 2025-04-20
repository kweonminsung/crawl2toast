from tkinter import *
from tkinter import ttk
from win10toast import ToastNotifier
from lib.ui.main_frame import main_frame
from lib.ui.settings_frame import settings_frame
from lib.ui.error_logs_frame import error_logs_frame
from lib.constants import APP_NAME


toaster = ToastNotifier()


def set_delete_window_handler(close: bool):
    if close:
        root.protocol("WM_DELETE_WINDOW", root.quit)
    else:
        root.protocol("WM_DELETE_WINDOW", root.iconify)


def deiconify():
    root.deiconify()
    root.lift()
    root.focus_force()


def initialize():
    global root

    root = Tk()
    root.title(APP_NAME)
    root.iconbitmap('public/icon.ico')
    root.geometry('400x600')
    root.attributes('-fullscreen', False)
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill=BOTH)

    # ----------------------------------------------------------------

    main_frame(notebook)

    settings_frame(notebook)

    error_logs_frame(notebook)

    root.mainloop()