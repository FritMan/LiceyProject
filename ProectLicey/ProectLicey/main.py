import tkinter as tk
import os

def button_1_click():
    os.startfile("from_memory.py")


def button_2_click():
    os.startfile("word_match.py")


def button_3_click():
    os.startfile("btn_menu.py")

window = tk.Tk()
window.geometry("300x200")
window.title("Главное меню")


button_1 = tk.Button(window, text="Перевод по памяти", command=button_1_click, height=100, width=100)
button_2 = tk.Button(window, text="Перевод по таблице", command=button_2_click, height=100, width=100)
button_3 = tk.Button(window, text="Меню скриптов", command=button_3_click, height=100, width=100)

button_1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
button_2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
button_3.grid(row=2, column=0, padx=10, pady=10, sticky="ew")



for i in range(3):
  window.rowconfigure(i, weight=1)
  window.columnconfigure(0, weight=1)

window.mainloop()