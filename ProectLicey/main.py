import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import random
import os

class DB:
    def __init__(self, db_name='dictionary.db'):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cur = self.conn.cursor()
            self.create_table_if_not_exists()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка запроса к базе данных: {e}")
            exit()

    def __del__(self):
        self.conn.close()

    def create_table_if_not_exists(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS dictionary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                meaning TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def run_query(self, query, parameters=()):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(query, parameters)
                self.conn.commit()
                return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка запроса к базе данных: {e}")
            return None


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Главное меню")
        self.geometry("300x200")
        self.db = DB()
        self.from_memory_window = None
        self.match_app = None
        self.script_menu_window = None

        self.create_buttons()
        self.mainloop()

    def create_buttons(self):
        self.button_1 = tk.Button(self, text="Перевод по памяти", command=self.open_from_memory, height=100, width=100)
        self.button_2 = tk.Button(self, text="Перевод по таблице", command=self.open_match_app, height=100, width=100)
        self.button_3 = tk.Button(self, text="Меню скриптов", command=self.open_script_menu, height=100, width=100)

        self.button_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.button_2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.button_3.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        for i in range(3):
            self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)


    def open_from_memory(self):
        if self.from_memory_window is None:
            self.from_memory_window = FromMemoryApp(self, self.db)
        self.from_memory_window.deiconify()
        self.withdraw()

    def open_match_app(self):
        if self.match_app is None:
            self.match_app = MatchApp(self, self.db)
        self.match_app.deiconify()
        self.withdraw()

    def open_script_menu(self):
        if self.script_menu_window is None:
            self.script_menu_window = ScriptMenuApp(self)
        self.script_menu_window.deiconify()
        self.withdraw()



class FromMemoryApp(tk.Toplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.title("Перевод по памяти")
        self.db = db
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.score = 0
        self.count = 0
        self.ls_translates = []
        self.username = self.get_username()
        self.tupple_lists = self.random_lists()
        self.init_main()

    def get_username(self):
        while True:
            username = simpledialog.askstring("Имя пользователя", "Введите ваше имя:")
            if username is None:
                return "Неизвестный"
            elif username.strip() == "":
                messagebox.showwarning("Предупреждение", "Имя пользователя не может быть пустым.")
            else:
                return username.strip()

    def init_main(self):
        self.ls_word = self.tupple_lists[0]
        self.ls_answer = self.tupple_lists[1]
        self.label_translate = tk.Label(self, text='Перевод')
        self.label_translate.place(x=30, y=21)
        self.entry_translate = ttk.Entry(self, width=30)
        self.entry_translate.place(x=120, y=50)
        self.entry_translate.focus()
        self.label_word = tk.Label(self, text=self.ls_word[self.count], font='Arial 11 bold')
        self.label_word.place(x=120, y=20)

        btn_yes = tk.Button(self, text='да')
        btn_yes.place(x=120, y=80)
        btn_yes.bind('<Button-1>', lambda event: self.key_translate_func(self.entry_translate,))
        self.entry_translate.bind('<Return>', lambda event: self.key_translate_func(self.entry_translate,))

        btn_new_start = tk.Button(self, text='Начать снова', command=self.new_start)
        btn_new_start.place(x=282, y=80)
        btn_stop = tk.Button(self, text='Стоп', command=self.stop_translate)
        btn_stop.place(x=190, y=80)
        btn_save = tk.Button(self, text='Сохранить результат', command=self.save_and_view_results)
        btn_save.place(x=155, y=110)

        self.score_label = tk.Label(self, text=f"Счёт: {self.score}", font=('Arial', 12))
        self.score_label.place(relx=1.0, rely=0.0, x=-10, y=10, anchor='ne')

    def key_translate_func(self, event):
        try:
            self.ls_translates.append(self.ls_word[self.count])
            user_translation = self.entry_translate.get()
            self.ls_translates.append(user_translation)
            self.ls_translates.append(self.ls_answer[self.count])
            if user_translation.lower() == self.ls_answer[self.count].lower():
                self.score += 1
                self.score_label.config(text=f"Счёт: {self.score}")
            self.count += 1
            if self.count < len(self.ls_word):
                self.label_word.destroy()
                self.entry_translate.delete(0, tk.END)
                self.label_word = tk.Label(self, text=self.ls_word[self.count], font='Arial 11 bold')
                self.label_word.place(x=120, y=20)
            else:
                self.view_results()
        except IndexError:
            print('вопросы закончились')

    def random_lists(self):
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
        self.destroy()
        self.master.from_memory_window = None
        self.master.deiconify()

    def view_results(self):
        self.save_results_to_file(self.ls_translates, self.score, self.username)
        ViewResults(self.ls_translates, self.score, self.username)

    def save_and_view_results(self):
        self.view_results()

    def save_results_to_file(self, translates, score, username):
        try:
            with open("results.txt", "a", encoding="utf-8") as f:
                f.write(f"Имя пользователя: {username}, Счёт: {score}\n")
                for i in range(0, len(translates), 3):
                    f.write(f"Слово: {translates[i]}, Перевод пользователя: {translates[i+1]}, Правильный переовод: {translates[i+2]}\n")
                f.write("\n")
            messagebox.showinfo("Успех", "Результаты сохранены в файл results.txt")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении результатов: {e}")

    def stop_translate(self):
        self.view_results()

    def on_closing(self):
        self.master.deiconify()
        self.destroy()
        self.master.from_memory_window = None


class MatchApp(tk.Toplevel):
    db_name = 'dictionary.db'

    def __init__(self, master, db):
        super().__init__(master)
        self.master = master
        self.db = db
        self.title('Учим слова')
        self.eng, self.trans = str(), str()
        self.entry_search = tk.Entry(self, background='white')
        self.entry_search.grid(row=1, column=1)
        self.entry_search.bind('<Return>', lambda event: self.search_translate(self.entry_search))
        self.message = tk.Label(self, text='', fg='red')
        self.message.grid(row=1, column=0, sticky=tk.W + tk.E)

        self.left = tk.Listbox(self, height=44, exportselection=False, activestyle='none', selectbackground='yellow')
        self.left.grid(row=2, column=0)
        self.right = tk.Listbox(self, height=44, activestyle='none')
        self.right.grid(row=2, column=1)
        self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scroll.grid(row=2, column=2, sticky='ns')
        self.scroll.config(command=self.right.yview)
        self.right.config(yscrollcommand=self.scroll.set)
        self.right.bind("<<ListboxSelect>>", self.callback_right)
        self.left.bind("<<ListboxSelect>>", self.callback_left)
        ttk.Button(self, text="Начать сначала", command=self.restart_program).grid(row=4, column=1, sticky=tk.W + tk.E)
        ttk.Button(self, text="Редактировать", command=self.open_edit_dictionary).grid(row=4, column=0, sticky=tk.W + tk.E)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.edit_dictionary_window = None
        self.get_words()

    def open_edit_dictionary(self):
        if self.edit_dictionary_window is None:
            self.edit_dictionary_window = EditDictionaryApp(self, self.db)
            self.edit_dictionary_window.protocol("WM_DELETE_WINDOW", self.on_edit_closing)
        self.edit_dictionary_window.deiconify()
        self.withdraw()

    def on_edit_closing(self):
        self.edit_dictionary_window = None
        self.get_words()
        self.deiconify()
        self.master.withdraw()

    def on_closing(self):
        self.master.deiconify()
        self.destroy()
        self.master.match_app = None
        if self.edit_dictionary_window:
            self.edit_dictionary_window.destroy()

    def run_query(self, query, parameters=()):
        return self.db.run_query(query, parameters)

    def get_words(self):
        query = 'SELECT * FROM dictionary ORDER BY word DESC'
        db_rows = self.run_query(query)
        if db_rows is None: return
        lst_left, lst_right = [], []
        for row in db_rows:
            lst_left.append(row[1])
            lst_right.append(row[2])
        random.shuffle(lst_left)
        random.shuffle(lst_right)
        self.dic = dict(zip(lst_left, lst_right))
        self.left.delete(0, tk.END)
        self.right.delete(0, tk.END)
        for k, v in self.dic.items():
            if len(k) > 1:
                self.left.insert(tk.END, k)
            if len(v) > 1:
                self.right.insert(tk.END, v)

    def callback_left(self, event):
        self.message['text'] = ''
        if not event.widget.curselection():
            return
        w = event.widget
        idx = int(w.curselection()[0])
        self.eng = w.get(idx)
        with self.db.conn:
            cursor = self.db.conn.cursor()
            sqlite_select_query = 'SELECT * from dictionary WHERE word = ?'
            cursor.execute(sqlite_select_query, (self.eng,))
            record = cursor.fetchone()
            self.trans = record[2]

    def callback_right(self, event1):
        self.message['text'] = ''
        if not event1.widget.curselection():
            return
        self.w_right = event1.widget
        idx = int(self.w_right.curselection()[0])
        click = self.w_right.get(idx)
        if click == self.trans:
            self.right.delete(tk.ANCHOR)
            self.left.delete(tk.ANCHOR)
        else:
            self.message['text'] = 'Неправильно'
            self.right.selection_clear(0, tk.END)

    def restart_program(self):
        self.message['text'] = ''
        self.left.delete(0, tk.END)
        self.right.delete(0, tk.END)
        self.get_words()

    def search_translate(self, event2):
        search_text = self.entry_search.get().lower()
        if search_text == '':
            self.message['text'] = 'Введите слово'
        else:
            ls_tr = []
            for k, v in self.dic.items():
                if v.lower().startswith(search_text):
                    ls_tr.append(v)
            self.tup_tr = tuple(ls_tr)
            ind = self.right.curselection()
            count = 0
            while count < len(self.tup_tr):
                item_search = self.tup_tr[count]
                for i in range(0, self.right.size()):
                    if self.right.get(i) == item_search:
                        self.right.itemconfig(i, fg='red')
                count += 1



class ScriptMenuApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.geometry("300x200")
        self.title("Меню скриптов")
        self.create_buttons()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def create_buttons(self):
        button_1 = tk.Button(self, text="Создать txt файл", command=self.button_1_click, height=150, width=100)
        button_2 = tk.Button(self, text="Создать новую БД", command=self.button_2_click, height=150, width=100)
        button_1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        button_2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        for i in range(3):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(0, weight=1)

    def button_1_click(self):
        try:
            os.startfile("write_in_file.py")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл write_in_file.py не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при запуске скрипта: {e}")

    def button_2_click(self):
        try:
            os.startfile("create_new_db.py")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл create_new_db.py не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при запуске скрипта: {e}")

    def on_closing(self):
        self.master.deiconify()
        self.destroy()
        self.master.script_menu_window = None


class EditDictionaryApp(tk.Toplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.master = master
        self.db = db
        self.title('Редактирование словаря')
        self.init_widgets()

    def init_widgets(self):
        frame = tk.LabelFrame(self, text='Введите новое слово')
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        tk.Label(frame, text='Слово: ').grid(row=1, column=0)
        self.word = tk.Entry(frame)
        self.word.focus()
        self.word.grid(row=1, column=1)
        tk.Label(frame, text='Значение: ').grid(row=2, column=0)
        self.meaning = tk.Entry(frame)
        self.meaning.grid(row=2, column=1)
        ttk.Button(frame, text='Сохранить', command=self.add_word).grid(row=3, columnspan=2, sticky=tk.W + tk.E)
        self.message = tk.Label(self, text='', fg='green')
        self.message.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)
        self.tree = ttk.Treeview(self, columns=('word', 'meaning'), height=30, show='headings')
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.column('word', width=220, anchor=tk.W)
        self.tree.column('meaning', width=220, anchor=tk.W)
        self.tree.heading('word', text='Слово', anchor=tk.CENTER)
        self.tree.heading('meaning', text='Значение', anchor=tk.CENTER)

        self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.scroll.grid(row=4, column=3, sticky='ns')
        self.tree.configure(yscrollcommand=self.scroll.set)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.get_words()

        self.tree.bind("<<TreeviewSelect>>", self.clear_selection)

    def clear_selection(self, event):
        self.tree.selection_clear()

    def run_query(self, query, parameters=()):
        return self.db.run_query(query, parameters)

    def get_words(self):
        self.tree.selection_clear()
        words = self.run_query('SELECT word, meaning FROM dictionary')
        if words:
            self.tree.delete(*self.tree.get_children())
            for word, meaning in words:
                self.tree.insert('', tk.END, values=(word, meaning))
        else:
            messagebox.showerror("Ошибка", "Слова не найдены")


    def validation(self):
        return len(self.word.get()) != 0 and len(self.meaning.get()) != 0

    def add_word(self):
        if self.validation():
            words = self.run_query('SELECT word FROM dictionary')
            if words and self.word.get().lower() in [word[0].lower() for word in words]:
                self.message['text'] = 'Такое слово уже существует'
                return
            query = 'INSERT INTO dictionary (word, meaning) VALUES (?, ?)'
            parameters = (self.word.get(), self.meaning.get())
            result = self.run_query(query, parameters)
            if result is not None:
                self.message['text'] = 'Слово добавлено'
                self.word.delete(0, tk.END)
                self.meaning.delete(0, tk.END)
                self.get_words()
            else:
                self.message['text'] = 'Ошибка при добавлении слова'
        else:
            self.message['text'] = 'Введите слово и значение'

    def on_closing(self):
        self.master.deiconify()
        self.destroy()
        self.master.match_app.edit_dictionary_window = None


class ViewResults(tk.Toplevel):
    def __init__(self, translates, score, username):
        super().__init__()
        self.ls_translates = translates
        self.title = ('Перевод по памяти')
        self.geometry('915x950+600+0')
        self.start_print(score, username)
        self.grab_set()

    def start_print(self, score, username):
        self.message = tk.Label(self, text=f"Ваш счёт: {score}, Имя пользователя: {username}")
        self.message.grid(row=0, column=0, columnspan=3, sticky=tk.W + tk.E)
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

        self.tree.grid(row=1, column=0, columnspan=3)

        self.scroll = tk.Scrollbar(self, command=self.tree.yview)
        self.scroll.grid(row=1, column=4, sticky='ns')
        self.tree.configure(yscrollcommand=self.scroll.set)

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.ls_tupples]



if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = MainApp()
    root.title("Главное меню")
    root.geometry('300x200')