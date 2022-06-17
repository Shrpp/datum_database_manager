from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.simpledialog import *
import csv
import os
import sqlite3

file_path = fd.askopenfilename(
    title="Import Database",
    filetypes=(("Data Base File (.db)", "*.db"), ("All Files", "*.*"))
)

filePath = os.fspath(file_path)

root = tk.Tk()
root.title("Datum: Database Manager v2.0")

frame = Frame(root)
frame.pack(pady=20)

style = ttk.Style()
style.theme_use("clam")
style.map("Treeview")

mydata = []

optionMenu = """
    Which field do you want to modify?

        1- First Field
        2- Second Field
        3- Third Field
        4- Fourth Field               
"""


class Table:

    def __init__(self, database):
        self.database = database

    def tables(self):
        try:
            sqlite_connection = sqlite3.connect(self.database)
            cursor = sqlite_connection.cursor()
            sqlite_select_query = "select name from sqlite_sequence;"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            cursor.close()
        except sqlite3.Error as error:
            messagebox.showerror("!", f"Datum has error connecting to SQLite: {error}")
        return record


table = Table(filePath)
tables = table.tables()

for i in tables[0]:
    table_name = i


def try_connection():
    try:
        sqlite_connection = sqlite3.connect(filePath)
        cursor = sqlite_connection.cursor()
        sqlite_select_query = f"select * from {table_name};"
        cursor.execute(sqlite_select_query)
        messagebox.showinfo("!", "Datum has connected successfully")
        cursor.close()
    except sqlite3.Error as error:
        messagebox.showerror("!", f"Datum has error connecting to SQLite: {error}")


def show_tables():
    if table_name is not None:
        messagebox.showinfo("Success", f"These are the available tables: {table_name}")
    else:
        messagebox.showerror("!", f"Datum has error connecting to SQLite")


def deleting_rows():
    try:
        id_input = int(input('What ID do you want to delete?:'))

        sqlite_connection = sqlite3.connect(filePath)
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = f"DELETE from {table_name} where id = {id_input};"
        cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()
        print(f"Total {cursor.rowcount} rows has been successfully deleted from {table_name} table")
        sqlite_connection.close()
    except sqlite3.Error as error:
        print(f"Error to deleting rows of {table_name} in SQLite: {error}")
    finally:
        sqlite_connection.close()


def insert_multiple_records():
    try:
        sqlite_connection = sqlite3.connect(filePath)
        cursor = sqlite_connection.cursor()

        array_list = []
        input_first_values = input('First Value: ')
        input_second_values = input('Second Value: ')
        input_third_values = input('Third Value: ')
        input_fourth_values = input('Fourth Value: ')
        array_list.extend([input_first_values, input_second_values, input_third_values, input_fourth_values])

        sqlite_query = f"INSERT INTO {table_name}(event_name, event_date, event_desc, agents) VALUES (?, ?, ?, ?)"
        cursor.executemany(sqlite_query, ([array_list]))
        sqlite_connection.commit()
        print(f"Total {cursor.rowcount} rows has been inserted successfully in {table_name} table")
        cursor.close()
    except sqlite3.Error as error:
        print(f"Error to deleting rows of {table_name} in SQLite: {error}")
    finally:
        sqlite_connection.close()


def search_data():
    try:
        sqlite_connection = sqlite3.connect(filePath)
        cursor = sqlite_connection.cursor()

        select_option = input('What field do you want search?: ')
        select_value = input('What value do you want search: ')
        sqlite_insert_query = f"SELECT * FROM {table_name} where {select_option} = {select_value}"
        cursor.execute(sqlite_insert_query)
        rows = cursor.fetchall()
        print(rows)
        print(f"Total {cursor.rowcount} rows has been showed successfully")
    except sqlite3.Error as error:
        print(f"Error showing {cursor.rowcount} rows on SQLite: {error}")
    finally:
        sqlite_connection.close()


def modify_rows():
    try:
        sqlite_connection = sqlite3.connect(filePath)
        cursor = sqlite_connection.cursor()

        select_option = input(optionMenu)
        for n in select_option:
            if n == '1':
                selected_option = 'event_name'
            elif n == '2':
                selected_option = 'event_date'
            elif n == '3':
                selected_option = 'event_desc'
            elif n == '4':
                selected_option = 'agents'
            else:
                print(f"Invalid option")
                break

        for v in selected_option:
            if v is not None:
                id_input = int(input("Which ID you want to modify?: "))
                break
            else:
                break

        for v in selected_option:
            if v is not None:
                value_input = input('Type the new value: ')
                break
            else:
                break

        sqlite_insert_query = f"UPDATE {table_name} SET {selected_option} = {value_input} WHERE id = {id_input}"
        cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()
        print(f"Total {cursor.rowcount} rows has been modified successfully on SQLite")
        cursor.close()
    except sqlite3.Error as error:
        print(f"Error on modify rows in {table_name} table on SQLite: {error}")
    finally:
        sqlite_connection.close()


def export_to_csv():
    if len(mydata) < 1:
        messagebox.showerror("No Data", "There is no data to export")
        return False
    fln = fd.asksaveasfilename(initialdir=os.getcwd(), title='Export CSV',
                               filetypes=(("CSV File (.csv)", "*.csv"), ("All Files", "*.*")))
    with open(fln, mode='w') as myFile:
        exp_writer = csv.writer(myFile, delimiter=',')
        for x in mydata:
            exp_writer.writerow(x)
    messagebox.showinfo("Data Exported", f"Your data has been exported to {os.path.basename(fln)} successfully.")


def destroy_app():
    value = messagebox.askquestion("?", "Are you sure do you want to exit?")
    if value == "yes":
        root.destroy()


def display_data():
    try:
        sqlite_connection = sqlite3.connect(filePath)
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = f"SELECT * FROM {table_name}"
        cursor.execute(sqlite_insert_query)
        rows = cursor.fetchall()
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert("", tk.END, values=row)
        global mydata
        mydata = rows
    except sqlite3.Error as error:
        messagebox.showerror("!", f"Error displaying data on SQLite: {error}")
    finally:
        sqlite_connection.close()


menubar = Menu(root)
menu_file = Menu(menubar, tearoff=0)
menu_file.add_command(label="Test Connection", command=try_connection)
menu_file.add_command(label="Show Tables", command=show_tables)
menu_file.add_command(label="Exit", command=destroy_app)
menubar.add_cascade(label="File", menu=menu_file)

menu_general = Menu(menubar, tearoff=0)
menu_general.add_command(label="Insert Values", command=insert_multiple_records)
menu_general.add_command(label="Deleting Rows", command=deleting_rows)
menu_general.add_command(label="Modify Rows", command=modify_rows)
menu_general.add_command(label="Search", command=search_data)
menubar.add_cascade(label="General", menu=menu_general)

tree = ttk.Treeview(frame, columns=("id", "event_name", "event_date", "event_desc", "agents"), show='headings')
tree.column("#1", anchor='center')
tree.heading("#1", text="id")
tree.column("#2", anchor='center')
tree.heading("#2", text="event_name")
tree.column("#3", anchor='center')
tree.heading("#3", text="event_date")
tree.column("#4", anchor='center')
tree.heading("#4", text="event_desc")
tree.column("#5", anchor='center')
tree.heading("#5", text="agents")
tree.pack(side='left', fill=Y)

sb = Scrollbar(frame, orient=VERTICAL)
sb.pack(side=RIGHT, fill=Y)

button1 = tk.Button(text="Refresh Data", command=display_data)
button1.pack(padx=10, pady=0)

button2 = tk.Button(text="Export to Excel (.csv)", command=export_to_csv)
button2.pack(padx=10, pady=10)

root.config(menu=menubar)
tree.config(yscrollcommand=sb.set)
sb.config(command=tree.yview)

root.mainloop()
