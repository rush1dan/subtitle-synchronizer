import tkinter as tk
from enum import IntEnum

class Pages(IntEnum):
    START = 0
    OPERATION = 1

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
        cls.page_collection[page].show()

class Page(tk.Frame):
    def __init__(self, master):
        self.main_window = master
        self.window_width = master.winfo_width()
        self.window_height = master.winfo_height()
        tk.Frame.__init__(self, master=master)

    def show(self):
        self.pack(side="top", fill="both", expand=True)

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
        

        super().show()