from tkinter import *
from tkinter import ttk
from lib.utils import datetime_to_timestamp
from lib.db import Database, get_histories
from lib.constants import HISTORY_LOAD_LIMIT
from lib.settings import get_sources, load_sources

history_offset: int = 0

selected_url: str | None = None
url_listbox: Listbox | None = None
history_listbox: Listbox | None = None

def main_frame(master: ttk.Notebook):
    global url_listbox
    global history_listbox

    main_frame = Frame(master)
    master.add(main_frame, text='기록')


    url_frame = Frame(main_frame)
    url_frame.pack(fill=X)

    url_label = Label(url_frame, text="URL", anchor='w')
    url_label.pack(fill=X, padx=3)

    url_listbox_scrollbar = ttk.Scrollbar(url_frame)
    url_listbox_scrollbar.pack(side=RIGHT, fill=Y)
    url_listbox = Listbox(url_frame, height=5, yscrollcommand=url_listbox_scrollbar.set)
    url_listbox.pack(fill=X)
    url_listbox.bind('<<ListboxSelect>>', url_listbox_click_handler)
    

    sp1 = ttk.Separator(main_frame, orient='horizontal')
    sp1.pack(fill=X)


    history_frame = Frame(main_frame)
    history_frame.pack(fill=BOTH, expand=True)

    history_label = Label(history_frame, text="기록", anchor='w')
    history_label.pack(fill=X, padx=3)

    history_listbox_scrollbar = ttk.Scrollbar(history_frame)
    history_listbox_scrollbar.pack(side=RIGHT, fill=Y)
    history_listbox_scrollbar.config(command=history_listbox_scrollbar_onscroll_handler)
    history_listbox = Listbox(history_frame, yscrollcommand=history_listbox_scrollbar.set)
    history_listbox.bind("<MouseWheel>", history_listbox_onscroll_handler)
    history_listbox.pack(fill=BOTH, expand=True)

    load_source()


def load_source():
    global url_listbox
    
    load_sources()
    sources = get_sources()

    url_listbox.delete(0, END)

    for _url, _source in sources.items():
        url_listbox.insert(END, _url)

    # url_listbox.insert(0, "https://example.com")


def url_listbox_click_handler(event):
    global selected_url
    global history_offset

    selected_index = url_listbox.curselection()
    if not selected_index:
        return
    new_selected_url = url_listbox.get(selected_index[0])

    # Do not update if the selected URL is the same as the previous one
    if new_selected_url == selected_url:
        return

    load_history_listbox(new_selected_url)


def load_history_listbox(url: str):
    global selected_url
    global history_listbox
    global history_offset

    selected_url = url    
    history_offset = 0
    history_listbox.delete(0, END)

    sources = get_sources()

    if sources[selected_url]["options"]["disable_history"]:
        history_listbox.insert(END, "이 URL은 기록을 저장하지 않습니다.")
        return

    histories = get_histories(Database().get_connection(), selected_url, HISTORY_LOAD_LIMIT, history_offset)

    for history in histories:
        # history_listbox.insert(END, history)
        history_listbox.insert(END, f"{datetime_to_timestamp(history['timestamp'])} - {history['content']}")


def reload_current_history_listbox():
    global selected_url

    if selected_url is None:
        return

    load_history_listbox(selected_url)


def history_listbox_load_more():
    global history_listbox
    global selected_url
    global history_offset
    
    append_histories = get_histories(Database().get_connection(), selected_url, HISTORY_LOAD_LIMIT, history_offset + HISTORY_LOAD_LIMIT)

    if len(append_histories) == 0:
        return

    history_offset += HISTORY_LOAD_LIMIT

    for i in range(len(append_histories)):
        # history_listbox.insert(END, append_histories[i])
        history_listbox.insert(END, f"{datetime_to_timestamp(append_histories[i]['timestamp'])} - {append_histories[i]['content']}")
        

def history_listbox_scrollbar_onscroll_handler(*args):
    global history_listbox

    history_listbox.yview(*args)
    
    # Check scroll position
    pos = history_listbox.yview()
    # print(f"pos: {pos}")

    if pos[1] > 0.95:
        history_listbox_load_more()


def history_listbox_onscroll_handler(event):
    global history_listbox

    # Check scroll position
    pos = history_listbox.yview()
    # print(f"pos: {pos}")

    if pos[1] > 0.95:
        history_listbox_load_more()
    