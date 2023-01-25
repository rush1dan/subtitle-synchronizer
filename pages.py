import tkinter as tk
from tkinter import filedialog
from enum import IntEnum
from data import Data
from utils import Duration_Unit, center_window, get_parent_directory
from operation import modify_sub_files
from tkinter import messagebox

class Pages(IntEnum):
    START = 0
    OPERATION = 1
    PROGRESS = 2
    COMPLETE = 3


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
        cls.page_collection[Pages.PROGRESS] = Progress_Page(main_window)
        cls.page_collection[Pages.COMPLETE] = Complete_Page(main_window)

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
        self.rowconfigure(0, minsize=int(self.window_height * 0.5))
        self.rowconfigure(1, minsize=int(self.window_height * 0.5))
        self.columnconfigure(0, minsize=int(self.window_width))

        frm_upper = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_upper.grid(row=0, column=0, sticky=tk.NSEW)

        frm_upper.columnconfigure(0, minsize=int(self.window_width * 0.95))
        frm_upper.columnconfigure(1, minsize=int(self.window_width * 0.05))
        frm_upper.rowconfigure(0, minsize=int(self.window_height * 0.5))

        frm_lbox_files = tk.Frame(master=frm_upper, relief=tk.FLAT, borderwidth=0)
        frm_lbox_files.grid(row=0, column=0, sticky=tk.NSEW)

        lbox_files = tk.Listbox(master=frm_lbox_files, width=1, height=1, font=("Arial", 10), justify="left")
        for i, file in enumerate(Data.files):
            lbox_files.insert(i + 1, f"{i + 1}. {file}")
        lbox_files.pack(side="left", fill="both", expand=True)

        frm_scrollbar = tk.Frame(master=frm_upper, relief=tk.FLAT, borderwidth=0)
        frm_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

        scrollbar = tk.Scrollbar(frm_scrollbar)
        scrollbar.pack(side="right", fill="both")

        lbox_files.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command=lbox_files.yview)

        frm_lower = tk.Frame(master=self, relief=tk.FLAT, borderwidth=0)
        frm_lower.grid(row=1, column=0, sticky=tk.NSEW)

        lbl_duration = tk.Label(master=frm_lower, text="Duration", fg="grey", font=("Arial", 12, "bold"))
        lbl_duration.place(relx=0.25, rely=0.3, anchor=tk.CENTER)

        entered_text = tk.StringVar()
        ent_duration = tk.Entry(master=frm_lower, width=12, font=("Arial", 12), borderwidth=2, textvariable=entered_text)
        ent_duration.place(relx=0.25, rely=0.6, anchor=tk.CENTER)
        def validate_entry(*args):
            val = entered_text.get()
            if not (len(val) > 0 and val[-1].isdigit() or (len(val) == 1 and val[-1] == "-")):
                ent_duration.delete(ent_duration.index(tk.INSERT) - 1, tk.END)
        entered_text.trace("w", validate_entry)

        lbl_unit = tk.Label(master=frm_lower, text="Unit", fg="grey", font=("Arial", 12, "bold"))
        lbl_unit.place(relx=0.6, rely=0.3, anchor=tk.CENTER)

        options = ["ms", "s", "m"]
        selected_option = tk.StringVar()
        selected_option.set(options[0])
        unit_dict = {"ms":Duration_Unit.ms, "s":Duration_Unit.s, "m":Duration_Unit.m}
        self.selected_unit = Duration_Unit.ms
        def select_unit(s: str):
            self.selected_unit = unit_dict[s]
        drp_unit = tk.OptionMenu(frm_lower, selected_option, *options, command=lambda x: select_unit(x))
        drp_unit.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

        def commence_operation():
            if len(ent_duration.get()) == 0:
                messagebox.showwarning(title="Duration Entry", message="Please enter modification duration.")
            else:
                suggested_directory = get_parent_directory(Data.files[0])
                saving_directory = save_filesorfolders_at(suggested_directory)
                
                if saving_directory:
                    self.main_window.config(menu="")
                    self.main_window.drop_target_unregister()
                    Page_Manager.show_page(Pages.PROGRESS)
                    self.main_window.update_idletasks()
                    modify_sub_files(Data.files, int(ent_duration.get()), self.selected_unit, saving_directory)

        btn_ok = tk.Button(master=frm_lower, text="OK", font=("Arial", 12, "bold"), relief=tk.RAISED, borderwidth=4, 
            command=commence_operation)
        btn_ok.place(relx=0.85, rely=0.6, anchor=tk.CENTER)

        super().show()


class Progress_Page(Page):
    def __init__(self, master):
        super().__init__(master)

    def show(self):
        window_width = self.window_width
        window_height = int(self.window_height * 0.5)

        self.main_window.geometry(center_window(window_width, window_height, self.winfo_screenwidth(), self.winfo_screenheight()))

        lbl_processing = tk.Label(master=self, text="Processing...", font=("Arial", 15, "bold"), anchor=tk.CENTER)
        lbl_processing.pack(side="top", fill="both", expand="true")


        super().show()


class Complete_Page(Page):
    def __init__(self, master):
        super().__init__(master)

    def show(self):
        window_width = self.window_width
        window_height = int(self.window_height * 0.5)

        self.main_window.geometry(center_window(window_width, window_height, self.winfo_screenwidth(), self.winfo_screenheight()))

        lbl_processing = tk.Label(master=self, text="Completed", font=("Arial", 15, "bold"), anchor=tk.CENTER)
        lbl_processing.pack(side="top", fill="both", expand="true")


        super().show()


def save_filesorfolders_at(suggested_dir: str)->str:
    return filedialog.askdirectory(initialdir=suggested_dir, mustexist=True)
