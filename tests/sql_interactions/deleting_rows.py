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


def deleting_rows():
    """
    It deletes a row from the database based on the ID the user inputs.
    """
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


if __name__ == "__main__":
    deleting_rows()
