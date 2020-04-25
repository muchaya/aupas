import tkinter as tk
import tkinter as ttk
from tkinter import *



bg_color__btn = "#212121"
font_color__btn = "#fff"
highlight_bg_color__btn = "#212121"
active_font_color__btn = "#fff"
activebackground_color__btn = "#444"


root = Tk()

content = ttk.Frame(root, padding="3 3 12 12")
content.grid(column = 0, row = 0, sticky=(N,W,E,S))
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)



selectdata__btn = tk.Button(content, cursor="hand1",width ="20",padx = 2, fg = font_color__btn,activeforeground = active_font_color__btn, highlightbackground = highlight_bg_color__btn , bg = bg_color__btn,activebackground = activebackground_color__btn, text="Upload")
selectdata__btn.grid(column = 3, row = 3)

feet = StringVar()


feet_entry = ttk.Entry(content, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

root.title("bLESSING")
root.geometry("900x600")
root.mainloop()