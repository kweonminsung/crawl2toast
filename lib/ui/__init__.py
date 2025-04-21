from tkinter import *
from tkinter import ttk, messagebox
import webbrowser
from lib.ui.main_frame import main_frame, load_source
from lib.ui.settings_frame import settings_frame
from lib.ui.error_logs_frame import error_logs_frame
from lib.constants import APP_NAME, CHECK_UPDATE_URL
from lib.crawler import request_crawl


root: Tk | None = None

def set_delete_window_handler(close: bool):
    global root
    
    if close:
        root.protocol("WM_DELETE_WINDOW", root.quit)
    else:
        root.protocol("WM_DELETE_WINDOW", root.iconify)


def deiconify():
    global root

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

    # ----------------------------------------------------------------

    menubar = Menu(root)

    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label='도움말', command=lambda: messagebox.showinfo(APP_NAME, "추후 업데이트 예정입니다."))
    menu1.add_command(label='업데이트 확인', command=lambda: webbrowser.open(CHECK_UPDATE_URL))
    menu1.add_command(label='종료', command=root.quit)
    menubar.add_cascade(label='파일', menu=menu1)

    menu2 = Menu(menubar, tearoff=0)
    menu2.add_command(label='소스파일 다시 로드', command=load_source)
    menubar.add_cascade(label='로드', menu=menu2)

    menu3 = Menu(menubar, tearoff=0)
    menu3.add_command(label='지금 긁어오기', command=crawl_now_handler)
    menubar.add_cascade(label='크롤링', menu=menu3)

    root.config(menu=menubar)

    # ----------------------------------------------------------------

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill=BOTH)

    main_frame(notebook)

    settings_frame(notebook)

    error_logs_frame(notebook)

    root.mainloop()


def crawl_now_handler():
    if messagebox.askyesno("확인", "지금 긁어오시겠습니까?"):
        request_crawl()

        
