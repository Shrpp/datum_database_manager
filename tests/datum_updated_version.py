from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.simpledialog import *
from tkinter.messagebox import showinfo
import fnmatch
import csv
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


def try_connection(database):
    try:
        sqlite_connection = sqlite3.connect(database)
        cursor = sqlite_connection.cursor()
        sqlite_select_query = f"select * from {table_name};"
        cursor.execute(sqlite_select_query)
        print("Datum has connected successfully")
        cursor.close()
    except sqlite3.Error as error:
        print(f"Datum has error connecting to SQLite: {error}")