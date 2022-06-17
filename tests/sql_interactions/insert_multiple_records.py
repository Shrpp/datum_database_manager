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


if __name__ == "__main__":
    insert_multiple_records()
