# + scrollbar. Корректное отображение более одного слова.

from tkinter import ttk
from tkinter import *
import sqlite3


class Dictionary:
    db_name = 'dictionary.db'

    def __init__(self, window):

        self.wind = window
        self.wind.title('Редактирование словаря')

        frame = LabelFrame(self.wind, text='Введите новое слово')
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        Label(frame, text='Слово: ').grid(row=1, column=0)
        self.word = Entry(frame)
        self.word.focus()
        self.word.grid(row=1, column=1)
        Label(frame, text='Значение: ').grid(row=2, column=0)
        self.meaning = Entry(frame)
        self.meaning.grid(row=2, column=1)
        ttk.Button(frame, text='Сохранить', command=self.add_word).grid(row=3, columnspan=2, sticky=W + E)
        self.message = Label(text='', fg='green')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)
        self.tree = ttk.Treeview(columns=('word', 'meaning'), height=36, show='headings')
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.column('word', width=220, anchor=W)
        self.tree.column('meaning', width=220, anchor=W)
        self.tree.heading('word', text='Слово', anchor=CENTER)
        self.tree.heading('meaning', text='Значение', anchor=CENTER)
        self.scroll = (Scrollbar(command=self.tree.yview))
        self.scroll.grid(row=4, column=3, sticky='ns')
        self.tree.configure(yscrollcommand=self.scroll.set)

        ttk.Button(text='Удалить', command=self.delete_word).grid(row=5, column=0, sticky=W + E)
        ttk.Button(text='Изменить', command=self.edit_word).grid(row=5, column=1, sticky=W + E)

        self.get_words()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_words(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('''SELECT word, meaning FROM dictionary ORDER BY word''')
        db_rows = cur.fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in db_rows]

    def validation(self):
        return len(self.word.get()) != 0 and len(self.meaning.get()) != 0

    def add_word(self):
        if self.validation():
            query = 'INSERT INTO dictionary VALUES(NULL, ?, ?)'
            parameters = (self.word.get(), self.meaning.get())
            self.run_query(query, parameters)
            self.message['text'] = 'слово {} добавлено в словарь'.format(self.word.get())
            self.word.delete(0, END)
            self.meaning.delete(0, END)
        else:
            self.message['text'] = 'введите слово и значение'
        self.get_words()

    def edit_records(self, new_word, word, new_meaning, old_meaning):
        query = 'UPDATE dictionary SET word = ?, meaning = ? WHERE word = ? AND meaning = ?'
        parameters = (new_word, new_meaning, word, old_meaning)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'слово {} успешно изменено'.format(word)
        self.get_words()


if __name__ == '__main__':
    window = Tk()
    application = Dictionary(window)
    window.mainloop()
