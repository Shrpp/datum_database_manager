from tkinter import filedialog as fd
import os
import sqlite3

file_path = fd.askopenfilename(
    title="Import Database",
    filetypes=(("Data Base File (.db)", "*.db"), ("All Files", "*.*"))
)

filePath = os.fspath(file_path)

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

    def show_tables(self):
        """
        It connects to the database, then it selects the name of the tables from the sqlite_sequence table,
        then it displays the names of the tables in a messagebox.
        """
        try:
            sqlite_connection = sqlite3.connect(self.database)
            cursor = sqlite_connection.cursor()
            sqlite_select_query = "select name from sqlite_sequence;"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            cursor.close()
        except sqlite3.Error as error:
            print(f"Datum has error connecting to SQLite: {error}")
        return record


table = Table(filePath)
tables = table.show_tables()

for i in tables[0]:
    table_name = i


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
