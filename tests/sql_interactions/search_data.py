from tkinter import filedialog as fd
import os
import sqlite3

file_path = fd.askopenfilename(
    title="Import Database",
    filetypes=(("Data Base File (.db)", "*.db"), ("All Files", "*.*"))
)

filePath = os.fspath(file_path)


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


def search_data():
    """
    It searches for a value in a column and returns the row where the value is found
    """
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


if __name__ == "__main__":
    search_data()
