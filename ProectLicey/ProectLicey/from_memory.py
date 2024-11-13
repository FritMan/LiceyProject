# виджет treeview
# Выровнял размер окна root

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq
import random, os, sys


class Main:
    def __init__(self, root):
        self.root = root
        self.db = db
        self.count = 0
        self.ls_translates = []
        self.tupple_lists = self.random_lists()
        self.init_main()

    def init_main(self):
        self.ls_word = self.tupple_lists[0]
        self.ls_answer = self.tupple_lists[1]
        self.label_translate = tk.Label(self.root, text='Перевод')
        self.label_translate.place(x=30, y=21)
        self.entry_translate = ttk.Entry(self.root, width=30)
        self.entry_translate.place(x=120, y=50)
        self.entry_translate.focus()

        while self.count < len(self.ls_word):
            self.label_word = tk.Label(self.root, text=self.ls_word[self.count], font='Arial 11 bold')
            self.label_word.place(x=120, y=20)
            break

        btn_yes = tk.Button(self.root, text='да')
        btn_yes.place(x=120, y=80)
        btn_yes.bind('<Button-1>', lambda event: self.key_translate_func(self.entry_translate,))
        self.entry_translate.bind('<Return>', lambda event: self.key_translate_func(self.entry_translate,))

        btn_new_start = tk.Button(self.root, text='Начать снова', command=self.new_start)
        btn_new_start.place(x=282, y=80)
        btn_stop = tk.Button(self.root, text='Стоп', command=self.stop_translate)
        btn_stop.place(x=190, y=80)

    def key_translate_func(self, event):
        try:
            self.ls_translates.append(self.ls_word[self.count])
            self.ls_translates.append(self.entry_translate.get())
            self.ls_translates.append(self.ls_answer[self.count])
            self.count += 1
            if self.count < len(self.ls_word):
                self.label_word.destroy()
                self.entry_translate.delete(0, tk.END)

                self.init_main()
            else:
                self.view_results()
        except IndexError:
            print('вопросы закончились')

    def random_lists(self):
        # sql запрос
        self.db.cur.execute('''SELECT word, meaning FROM dictionary''')
        self.dictionary = self.db.cur.fetchall()
        random.shuffle(self.dictionary)
        self.ls_key_dictionary = []
        self.ls_value_dictionary = []
        for item in self.dictionary:
            if len(item[0]) > 1 and len(item[1]) > 1:
                self.ls_key_dictionary.append(item[0])
                self.ls_value_dictionary.append(item[1])
        
        return self.ls_key_dictionary, self.ls_value_dictionary

    def new_start(self):
        self.root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)


    def view_results(self):
        ViewResults(self.ls_translates)

    def stop_translate(self):
        self.view_results()


# Класс DB, создаёт/открывает базу данных (БД)
class DB:
    with sq.connect('dictionary.db') as conn:
        cur = conn.cursor()

class ViewResults(tk.Toplevel):
    def __init__(self, translates):
        super().__init__()
        self.ls_translates = translates
        self.title = ('Перевод по памяти')
        self.geometry('915x950+600+0')
        self.start_print()

        self.grab_set()

    def start_print(self):
        self.message = tk.Label(self, text='')  # Просто отступ от заголовка.
        self.message.grid(row=1, column=0, columnspan=3, sticky=tk.W + tk.E)
        count = 0
        step = 3
        self.ls_tupples = []
        while count < len(self.ls_translates):
            word = self.ls_translates[count]
            my_tr = self.ls_translates[count + 1]
            tr = self.ls_translates[count + 2]
            tupple_translate = (word, my_tr, tr)
            self.ls_tupples.append(tupple_translate)
            count += step

        self.tree = ttk.Treeview(self, columns=('word', 'my_tr', 'tr'), height=45, show='headings')

        self.tree.column('word', width=300)
        self.tree.column('my_tr', width=300)
        self.tree.column('tr', width=300)
        self.tree.heading('word', text='слово')
        self.tree.heading('my_tr', text='мой перевод')
        self.tree.heading('tr', text='перевод')

        self.tree.grid(row=2, column=0, columnspan=3)

        self.scroll = tk.Scrollbar(self, command=self.tree.yview)
        self.scroll.grid(row=2, column=4, sticky='ns')
        self.tree.configure(yscrollcommand=self.scroll.set)

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.ls_tupples]


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    root.title("Перевод по памяти")
    root.geometry('500x180+450+200')
    root.mainloop()
