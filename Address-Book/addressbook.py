import sqlite3
from sqlite3 import Error
from tkinter import *
import tkinter.messagebox

class AddressBook:
    def __init__(self, root):
        self.root = root
        self.root.geometry('600x370')
        self.root.title('AddressBook')
        self.list_of_names = []
        self.name = StringVar()
        self.number = StringVar()
        self.conn = self.create_connection(r"./Address-Book/addressbook.db")
        
        if self.conn:
            self.create_table()
        else:
            print("Error! Cannot create the database connection.")
            
        self.setup_ui()

    def create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.execute('''SELECT * FROM tasks''')
            for row in cursor:
                self.list_of_names.append(row[1])
            return conn
        except Error as e:
            print(e)
        return None

    def create_table(self):
        create_table_sql = """CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                phone_no TEXT NOT NULL
                             );"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print(e)

    def on_click_added(self):
        tkinter.messagebox.showinfo("Info", f"{self.name.get()} got added")

    def on_click_deleted(self):
        tkinter.messagebox.showinfo("Info", f"{self.name.get()} got deleted")

    def create_task(self):
        if self.name.get() in self.list_of_names or not self.validate_input():
            return

        sql = '''INSERT INTO tasks (name, phone_no) VALUES (?, ?)'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (self.name.get(), self.number.get()))
            self.conn.commit()
            self.on_click_added()
            self.list_of_names.append(self.name.get())
        except Error as e:
            print(e)

    def validate_input(self):
        if not self.name.get() or not self.number.get() or len(self.number.get()) != 10:
            self.show_error("Name and Phone Number must be valid and Phone Number should be 10 digits.")
            return False
        return True

    def show_error(self, message):
        top = Toplevel(self.root)
        top.geometry('200x100')
        Label(top, text=message).pack()
        Button(top, text='Back', command=top.destroy).pack()

    def select_task_by_name(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE name=?", (self.name.get(),))
            rows = cursor.fetchall()
            if rows:
                self.number.set(rows[0][2])
            else:
                self.show_error(f"{self.name.get().upper()} NOT FOUND!")
        except Error as e:
            print(e)

    def update_task(self):
        if self.name.get() not in self.list_of_names or not self.validate_input():
            self.show_error(f"{self.name.get().upper()} NOT FOUND!")
            return
        
        sql = '''UPDATE tasks SET phone_no = ? WHERE name = ?'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (self.number.get(), self.name.get()))
            self.conn.commit()
        except Error as e:
            print(e)

    def delete_task(self):
        if self.name.get() not in self.list_of_names:
            self.show_error(f"{self.name.get().upper()} NOT FOUND!")
            return
        
        sql = 'DELETE FROM tasks WHERE name=?'
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (self.name.get(),))
            self.conn.commit()
            self.list_of_names.remove(self.name.get())
            self.on_click_deleted()
        except Error as e:
            print(e)

    def select_all_tasks(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()

            top = Toplevel(self.root)
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    e = Entry(top, width=15, fg='Gray20')
                    e.grid(row=i, column=j)
                    e.insert(END, value)
            Button(top, text='OK', command=top.destroy).grid(row=i+1, column=j)
        except Error as e:
            print(e)

    def exit_app(self):
        self.root.destroy()

    def reset_fields(self):
        self.name.set('')
        self.number.set('')

    def setup_ui(self):
        Label(self.root, text='NAME', font='Times 15 bold').place(x=130, y=20)
        Entry(self.root, textvariable=self.name, width=42).place(x=200, y=25)
        Label(self.root, text='PHONE NO ', font='Times 15 bold').place(x=130, y=70)
        Entry(self.root, textvariable=self.number, width=35).place(x=242, y=73)

        Button(self.root, text="ADD", font='Times 14 bold', bg='dark gray', command=self.create_task, width=8).place(x=130, y=110)
        Button(self.root, text="EDIT", font='Times 14 bold', bg='dark gray', command=self.update_task, width=8).place(x=260, y=108)
        Button(self.root, text="DELETE", font='Times 14 bold', bg='dark gray', command=self.delete_task, width=8).place(x=390, y=107)
        Button(self.root, text="VIEW ALL", font='Times 14 bold', bg='dark gray', command=self.select_all_tasks, width=12).place(x=160, y=191)
        Button(self.root, text="VIEW BY NAME", font='Times 14 bold', bg='dark gray', command=self.select_task_by_name, width=13).place(x=330, y=190)
        Button(self.root, text="EXIT", font='Times 14 bold', bg='dark gray', command=self.exit_app, width=8).place(x=200, y=280)
        Button(self.root, text="RESET", font='Times 14 bold', bg='dark gray', command=self.reset_fields, width=8).place(x=320, y=280)


if __name__ == "__main__":
    root = Tk()
    app = AddressBook(root)
    root.mainloop()
