from tkinter import *
from tkinter import ttk, messagebox
import webbrowser
from lib.ui.main_frame import main_frame, load_source
from lib.ui.settings_frame import settings_frame, crawl_now_handler
from lib.ui.logs_frame import logs_frame
from lib.utils import get_path
from lib.constants import APP_NAME, CHECK_UPDATE_URL
from lib.i18n import t


root: Tk | None = None

def set_iconify_ondeletewindow_handler(iconfiy: bool):
    global root

    if iconfiy:
        root.protocol("WM_DELETE_WINDOW", root.iconify)
    else:
        root.protocol("WM_DELETE_WINDOW", root.quit)


def deiconify():
    global root

    root.deiconify()
    root.lift()
    root.focus_force()


def initialize():
    global root

    root = Tk()
    root.title(APP_NAME)

    root.iconbitmap(get_path("public/icon.ico"))
    root.geometry('400x600')
    root.attributes('-fullscreen', False)
    root.resizable(False, False)

    # ----------------------------------------------------------------

    menubar = Menu(root)

    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label=t('ui.menubar.menu1.help'), command=lambda: messagebox.showinfo(t('message.title.info'), t('message.common.update_later')))
    menu1.add_command(label=t('ui.menubar.menu1.check_for_updates'), command=lambda: webbrowser.open(CHECK_UPDATE_URL))
    menu1.add_command(label=t('ui.menubar.menu1.exit'), command=root.quit)
    menubar.add_cascade(label=t('ui.menubar.menu1.file'), menu=menu1)

    menu2 = Menu(menubar, tearoff=0)
    menu2.add_command(label=t('ui.menubar.menu2.reload_source'), command=lambda: load_source(True))
    menubar.add_cascade(label=t('ui.menubar.menu2.load'), menu=menu2)

    menu3 = Menu(menubar, tearoff=0)
    menu3.add_command(label=t('ui.menubar.menu3.crawl_now'), command=crawl_now_handler)
    menubar.add_cascade(label=t('ui.menubar.menu3.crawling'), menu=menu3)

    root.config(menu=menubar)

    # ----------------------------------------------------------------

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill=BOTH)

    main_frame(notebook)

    settings_frame(notebook)

    logs_frame(notebook)

    root.mainloop()

        
