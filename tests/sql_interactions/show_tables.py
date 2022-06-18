from tkinter import filedialog as fd
import os
import sqlite3

file_path = fd.askopenfilename(
    title='Import Database',
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


if __name__ == "__main__":
    table = Table(filePath)
    for i in table.show_tables()[0]:    
        table_name = i
    print(f'These are the tables on the database file: {table_name}')
