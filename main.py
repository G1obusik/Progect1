import tkinter as tk 
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_records()

    #  метод инициализации виджетов
    def init_main(self):

        # тулбар
        toolbar = tk.Frame(bg='#B2C5F0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # кнопка добовления 
        # PhotoImage - добавленное изображения
        self.add_img = tk.PhotoImage(file='.add.png')
        # image - картинка, которая размещена на кнопке
        # bg - фон 
        # bd - граница
        btn_add = tk.Button(toolbar,
                            image=self.add_img,
                            bg='#B2C5F0', bd=0, 
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # кнопка редактирования
        self.upd_img = tk.PhotoImage(file='update.png')
        btn_upd = tk.Button(toolbar, 
                            image=self.upd_img,
                            bg='#B2C5F0', bd=0, 
                            command=self.open_update)
        btn_upd.pack(side=tk.LEFT)

        # кнопка удаления
        self.del_img = tk.PhotoImage(file='delete.png')
        btn_del = tk.Button(toolbar, 
                            image=self.del_img,
                            bg='#B2C5F0', bd=0, 
                            command=self.del_records)
        btn_del.pack(side=tk.LEFT)

        # кнопка поиска
        self.search_img = tk.PhotoImage(file='search.png')
        btn_search = tk.Button(toolbar, 
                            image=self.search_img,
                            bg='#B2C5F0', bd=0, 
                            command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # кнопка обновления
        self.refresh_img = tk.PhotoImage(file='refresh.png')
        btn_refresh = tk.Button(toolbar, 
                            image=self.refresh_img,
                            bg='#B2C5F0', bd=0, 
                            command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # таблица для вывода информации для контакотов
        self.tree = ttk.Treeview(self,
                                  columns=('ID','name','phone','email', 'salary'),
                                  show='headings',
                                  height=17)
        # настройки для столбцов
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=100, anchor=tk.CENTER)

        # задаем подписи столбцам
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Email')
        self.tree.heading('salary', text='Salary')

        self.tree.pack()

    #медот добавдения в БД(посредник) 
    def record(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # метод редактирования
    def upd_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE users SET name = ?, phone = ?, email = ?, salary = ?
                    WHERE id = ? 
                    ''', ( name, phone, email, salary, id))
        self.db.conn.commit()
        self.view_records()

    # метод удаления
    def del_records(self):
        for i in self.tree.selection():
            self.db.cur.execute('DELETE FROM users WHERE id = ?',
                               (self.tree.set(i, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # метод поиска 
    def search_records(self, name):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM users WHERE name LIKE ?', ('%' + name + '%',))
        r = self.db.cur.fetchall()
        for i in r: 
            self.tree.insert('', 'end', values=i)

    # перезаполнение виджета таблицы
    def view_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM users')
        r = self.db.cur.fetchall()
        for i in r: 
            self.tree.insert('', 'end', values=i)

    #  метод открытия окна добавления
    def open_child(self):
        Child()

    # метод открытия окна редактирования 
    def open_update(self):
        Update()

    # метод открытия окна поиска
    def open_search(self):
        Search()


# класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    # метод для создания виджетов дочернего окна
    def init_child(self):
        self.title('Добавление контакта')
        self.geometry('400x250')
        self.resizable(False, False)
        #  перехватывем события происходящие в риложении
        self.grab_set()
        # перехват фокус
        self.focus_set
        
        label_name = tk.Label(self, text='ФИО')
        label_phone = tk.Label(self, text='Телефон')
        label_email = tk.Label(self, text='Email')
        label_salary = tk.Label(self, text='Зарплата')
        label_name.place(x=50,y=50)
        label_phone.place(x=50,y=80)
        label_email.place(x=50,y=110)
        label_salary.place(x=50,y=130)

        self.entry_name = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_salary = tk.Entry(self)
        self.entry_name.place(x=250,y=50)
        self.entry_phone.place(x=250,y=80)
        self.entry_email.place(x=250,y=110)
        self.entry_salary.place(x=250,y=150)

        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=250, y=190)

        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>',
                          lambda ev: self.view.record(self.entry_name.get(),
                                                      self.entry_phone.get(),
                                                      self.entry_email.get(),
                                                      self.entry_salary.get()))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(),
                          add='+')
        self.btn_ok.place(x=315, y=190)


# класс окна поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_search()

    # метод для создания виджетов дочернего окна
    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('400x200')
        self.resizable(False, False)
        #  перехватывем события происходящие в риложении
        self.grab_set()
        # перехват фокус
        self.focus_set
        
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50,y=50)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=250,y=50)

        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=250, y=160)

        self.btn_ok = tk.Button(self, text='Найти')
        self.btn_ok.bind('<Button-1>',  lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(),
                          add='+')
        self.btn_ok.place(x=325, y=160)


# класс редактирования 
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Редактирование контакта')
        self.btn_ok.destroy()
        self.btn_upd = tk.Button(self, text='Сохранить')
        self.btn_upd.bind('<Button-1>',
                           lambda ev: self.view.upd_record(self.entry_name.get(),
                                                           self.entry_phone.get(),
                                                           self.entry_email.get(),
                                                           self.entry_salary.get()))
        self.btn_upd.bind('<Button-1>', lambda ev: self.destroy(),
                          add='+')
        self.btn_upd.place(x=315, y=190)

    # метод заполнения формы
    def default_data(self):
        id =  self.view.tree.set(self.view.tree.selection()[0], '#1') 
        self.db.cur.execute('SELECT * FROM users WHERE id = ?', id)
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])
    

# класс БД
class Db:
    # создания соединения, курсора и таблицы (если ее нет)
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT, 
                         salary INTEGER 
            )''')
        
    # метод добавления в ДБ
    def insert_data(self, name,phone, email, salary):
        self.cur.execute('''
                INSERT INTO users (name, phone, email, salary)
                VALUES (?, ?, ?, ?)
        ''', (name, phone, email, salary))
        self.conn.commit()
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Список сотрудников компании')
    root.geometry('790x450')
    root.resizable(False, False)
    db = Db()
    app = Main(root)
    app.pack()

    root.mainloop()

