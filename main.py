import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import utils
from pages import Page_Manager, Pages
from data import Data

window = TkinterDnD.Tk()

#Main Window:
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_aspect_ratio = 1.5
window_width = int(screen_width / 6)
window_height = int(window_width / window_aspect_ratio)
window.geometry(f"{window_width}x{window_height}")
window.resizable(0, 0)
window.update_idletasks()

#Menubar:
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
#filemenu.add_command(label="New", command=None)
filemenu.add_command(label="Open", command=lambda: print("open"))
#filemenu.add_command(label="Save", command=None)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
window.config(menu=menubar)

window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', lambda e: utils.process_dnd_data(e.data))
Page_Manager.setup_pages(window, Pages.START)

Data.on_data_registered = lambda data: Page_Manager.show_page(Pages.OPERATION)

window.mainloop()