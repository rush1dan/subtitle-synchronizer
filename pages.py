import tkinter as tk
from enum import IntEnum
from data import Data

class Pages(IntEnum):
    START = 0
    OPERATION = 1


class Page(tk.Frame):
    def __init__(self, master):
        self.main_window = master
        self.window_width = master.winfo_width()
        self.window_height = master.winfo_height()
        tk.Frame.__init__(self, master=master)

    def show(self):
        self.pack(side="top", fill="both", expand=True)

    def hide(self):
        self.pack_forget()


class Page_Manager:
    current_page = None

    page_collection = {}

    @classmethod
    def setup_pages(cls, main_window: tk.Tk, start_page: Pages):
        cls.page_collection[Pages.START] = Start_Page(main_window)
        cls.page_collection[Pages.OPERATION] = Operation_Page(main_window)

        cls.show_page(start_page)

    @classmethod
    def show_page(cls, page: Pages):
        if cls.current_page != None:
            cls.hide_page(cls.current_page)

        cls.current_page = cls.page_collection[page]
        cls.current_page.show()

    @classmethod
    def hide_page(cls, page: Page):
        page.hide()


class Start_Page(Page):
    def __init__(self, master):
        super().__init__(master)

    def show(self):
        lbl_tutorial = tk.Label(master=self, text="Open or Drag and Drop File(s)", fg="grey", font=("Arial", 15, "bold"))
        lbl_tutorial.place(relx=0.5, rely=0.4, anchor="center")

        super().show()
        

class Operation_Page(Page):
    def __init__(self, master):
        super().__init__(master)

    def show(self):
        lbox_files = tk.Listbox(master=self, height=int(self.window_height * 0.5), width=int(self.window_width * 0.8), font=("Arial", 10))
        lbox_files.pack(side = "left", fill = "both", expand=True)

        scrollbar = tk.Scrollbar(lbox_files)
        scrollbar.pack(side = "right", fill = "both")
        for i, file in enumerate(Data.files):
            lbox_files.insert(i + 1, file)

        lbox_files.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = lbox_files.yview)


        super().show()