from tkinter import *
from tkinter import ttk
from lib import db, utils
from lib.constants import HISTORY_LIMIT

history_offset = 0

selected_url = None
url_listbox = None
history_listbox = None

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
    history_frame.pack(fill=BOTH, expand=True)

    history_label = Label(history_frame, text="기록", anchor='w')
    history_label.pack(fill=X, padx=3)

    history_listbox_scrollbar = ttk.Scrollbar(history_frame)
    history_listbox_scrollbar.pack(side=RIGHT, fill=Y)
    history_listbox_scrollbar.config(command=history_listbox_scrollbar_onscroll_handler)
    history_listbox = Listbox(history_frame, yscrollcommand=history_listbox_scrollbar.set)
    history_listbox.bind("<MouseWheel>", history_listbox_onscroll_handler)
    history_listbox.pack(fill=BOTH, expand=True)


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
        # history_listbox.insert(END, history)
        history_listbox.insert(END, f"{utils.timestamp_to_datetime(history['timestamp'])} - {history['title']}")


def history_listbox_load_more():
    global history_listbox
    global selected_url
    global history_offset
    
    append_histories = db.get_histories(url_listbox.get(selected_url), HISTORY_LIMIT, history_offset + HISTORY_LIMIT)

    if len(append_histories) == 0:
        return

    history_offset += HISTORY_LIMIT

    for i in range(len(append_histories)):
        # history_listbox.insert(END, append_histories[i])
        history_listbox.insert(END, f"{utils.timestamp_to_datetime(append_histories[i]['timestamp'])} - {append_histories[i]['title']}")
        

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
    