import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import utils
from pages import Page_Manager, Pages
from data import Data
import base64

window = TkinterDnD.Tk()

#Main Window:
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_aspect_ratio = 1.5
window_width = int(screen_width / 6)
window_height = int(window_width / window_aspect_ratio)
window.title("Subtitle Synchronizer")
#from https://www.motobit.com/util/base64-decoder-encoder.asp, 32*32 png to utf-8 base64 string
base64_png = "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"
img= base64.b64decode(base64_png)
photo_icon = tk.PhotoImage(data= img)
window.wm_iconphoto(True, photo_icon)
window.geometry(utils.center_window(window_width, window_height, screen_width, screen_height))
window.resizable(0, 0)
window.update_idletasks()

#Menubar:
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
#filemenu.add_command(label="New", command=None)
filemenu.add_command(label="Open", command=lambda: utils.open_files())
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

# pyinstaller --onefile -w --paths "C:\PythonProjects\SubtitleSynchronizer\.venv\Lib\site-packages" main.py -i "C:\PythonProjects\SubtitleSynchronizer\SubSyncIcon.ico" --additional-hooks-dir=.