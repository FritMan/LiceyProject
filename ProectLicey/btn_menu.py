import tkinter as tk
import os

def button_1_click():
    os.startfile("write_in_file.py")


def button_2_click():
    os.startfile("create_new_db.py")


window = tk.Tk()
window.geometry("300x200")
window.title("Меню скриптов")


button_1 = tk.Button(window, text="Создать txt файл", command=button_1_click, height=150, width=100)
button_2 = tk.Button(window, text="Созать новую БД", command=button_2_click, height=150, width=100)

button_1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
button_2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")



for i in range(3):
  window.rowconfigure(i, weight=1)
  window.columnconfigure(0, weight=1)

window.mainloop()