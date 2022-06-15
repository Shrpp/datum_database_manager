# v1.0

# --------------------Libraries--------------------

# Importing all the libraries that are needed for the program to run.
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

# --------------------Variables-------------------
# Creating a window with the title "CRUD".
root=tk.Tk()
root.title("Datum: Database Manager v1.0")

# Creating a frame and packing it to the root window.
frame = Frame(root)
frame.pack(pady=20)

# Changing the style of the treeview.
style = ttk.Style()
style.theme_use("clam")
style.map("Treeview")

# A string that is used to ask the user what column he wants to modify.
optionMenu = """
    ¿Qué columna deseas modificar?
                    
        1- Nombre del Suceso
        2- Fecha del Suceso
        3- Descripción del Suceso
        4- Agentes               
"""
# An empty list.
mydata = []

# Asking the user to select a file and then it is saving the path of the file in a variable.
file_path = fd.askopenfilename(title='Importar Base de Datos', filetypes=(("Data Base File (.db)", "*.db"), ("All Files", "*.*")))
filePath = os.fspath(file_path)

# -------------------- Functional Code --------------------

def tryConnection():
    """
    If the file exists and the file extension is .db, then show a messagebox saying "Successfully
    Connected to SQLite"
    """
    try:
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
        sqlite_select_Query = "select * from registros;"
        cursor.execute(sqlite_select_Query)
        messagebox.showinfo("!", "Se ha conectado correctamente a SQLite")
        cursor.close()
    except sqlite3.Error as error:
        tError = "Error al conectar a la base de datos de SQLite: " + str(error)
        messagebox.showerror("Error", tError)

def showTables():
    """
    It connects to the database, then it selects the name of the tables from the sqlite_sequence table,
    then it displays the names of the tables in a messagebox.
    """
    try:
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
        sqlite_select_Query = "select name from sqlite_sequence;"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        tRecord = "Estas son las tablas disponibles: " + str(record)
        messagebox.showinfo("!", tRecord)
        cursor.close()
    except sqlite3.Error as error:
        tError = "Error al conectar a la base de datos de SQLite: " + str(error)
        messagebox.showerror("Error", tError)

def destroyApp():
    """

    If the user clicks the "yes" button, the program will close.
    """
    value=messagebox.askquestion("?","Seguro que quieres salir?")
    if value=="yes":
        root.destroy()

def displayData():
    """
    It connects to the database, selects all the rows from the table, and then inserts them into the
    treeview.
    """
    try:
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
        sqlite_insert_query = "SELECT * FROM registros"
        cursor.execute(sqlite_insert_query)
        rows = cursor.fetchall()
        for arows in tree.get_children():
            tree.delete(arows)
        for row in rows:
            tree.insert("", tk.END, values=row)
        global mydata
        mydata = rows
    except sqlite3.Error as error:
        e = "Imposible mostrar filas de la tabla de SQLite: " + str(error)
        messagebox.showerror("!", e)
    finally:
        sqliteConnection.close()
        

def deletingRows():
    """
    It deletes a row from the database based on the ID the user inputs.
    """
    try:
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
        
        idInput = askstring("?", 'What ID do you want to delete?')
        
        sqlite_insert_query =  "DELETE from registros where id = ?;"
        cursor.execute(sqlite_insert_query, idInput)
        sqliteConnection.commit()
        tRows = "Un total de "+ str(cursor.rowcount) + " filas han sido eliminadas correctamente de la tabla de Registros"
        messagebox.showinfo("Total Rows", tRows)
        cursor.close()
    except sqlite3.Error as error:
        tError = "Imposible borrar filas de la tabla de SQLite: " + str(error)
        messagebox.showerror("Error", tError)
    finally:
        sqliteConnection.close()

def insertMultipleRecords():
    """
    It takes the values from the user and inserts them into the database.
    """
    try:
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
        
        arrayList=[]
        input1thValues = askstring('?', '¿Qué nombre tiene este suceso?: ')
        input2thValues = askstring('?', '¿En qué fecha sucedió el suceso?: ')
        input3thValues = askstring('?', '¿Qué sucedió exactamente?: ')
        input4thValues = askstring('?', '¿Quienes estuvieron en el suceso?: ')
        arrayList.extend([input1thValues, input2thValues, input3thValues, input4thValues])
    
        sqlite_insert_query = """INSERT INTO registros(event_name, event_date, event_desc, agents) VALUES (?, ?, ?, ?)"""
        cursor.executemany(sqlite_insert_query, ([arrayList]))
        sqliteConnection.commit()
        insertV = "Un total de "+str(cursor.rowcount)+" filas se han insertado correctamente en la tabla Registros"
        messagebox.showinfo("Insert Values", insertV)
        cursor.close()
    except sqlite3.Error as error:
        e = "Imposible insertar valores en la tabla de SQLite:" + str(error)
        messagebox.showerror("!", e)
    finally:
        sqliteConnection.close()

def searchData():
    """
    It searches for a value in a column and returns the row where the value is found
    """
    try:
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
        
        selectOption = askstring('?', '¿En cual columna deseas buscar?: ')
        selectValue = askstring('?', 'Coloca el valor que deseas buscar')
        sqlite_insert_query = "SELECT * FROM registros where " + selectOption + " = '" + selectValue + "'"

        cursor.execute(sqlite_insert_query)
        oneRow = cursor.fetchall()
        for arows in tree.get_children():
            tree.delete(arows)
        for row in oneRow:
            tree.insert("", tk.END, values=row)
        insertV = "Un total de 1 fila ha sido mostrada dentro de la tabla satisfactoriamente"
        messagebox.showinfo("Insert Values", insertV)
    except sqlite3.Error as error:
        e = "Imposible buscar los valores de la tabla de SQLite:" + str(error)
        messagebox.showerror("!", e)
    finally: 
        sqliteConnection.close()
        
def modifyRows():
    """
    It takes the user's input, and uses it to modify the selected row in the database
    """
    try:
        sqliteConnection = sqlite3.connect(filePath)
        cursor = sqliteConnection.cursor()
        
# Asking the user to input a number, and then it is assigning a value to the variable selectedOption
# based on the number the user inputs.
        selectOption = askstring('?', optionMenu)
        for n in selectOption:
            if n == '1':
                selectedOption = 'event_name'
            elif n == '2':
                selectedOption = 'event_date'
            elif n == '3':
                selectedOption = 'event_desc'
            elif n == '4':
                selectedOption = 'agents'
            else:
                messagebox.showerror('!', 'Elige una opción correcta')
                break
    
# Asking the user to input the ID of the row he wants to modify.
        for v in selectedOption:    
            if v != None:
                idInput=askinteger('?', 'Indica el ID de la fila que deseas modificar: ')
                break
            else:
                break

# Asking the user to input the new values for the selected column.
        for v in selectedOption:          
            if v != None:
                valueInput=askstring('?', 'Indica los nuevos valores: ')
                break
            else:
                break

        sqlite_insert_query = "UPDATE registros SET " + str(selectedOption) + " = '" + str(valueInput) + "' WHERE id = " + str(idInput)     
        cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        insertV = "El total de "+str(cursor.rowcount)+" filas han sido modificadas satisfactoriamente"
        messagebox.showinfo("Success", insertV)
        cursor.close()
    except sqlite3.Error as error:
        e = "Imposible modificar valores de la tabla de SQLite:" + str(error)
        messagebox.showerror("!", e)
    finally: 
        sqliteConnection.close()      
        
def export2CSV():
    """
    It opens a file dialog, asks the user to select a location, then writes the data to a csv.
    """
    if len(mydata) < 1:
        messagebox.showerror("No Data", "No hay Data disponible para exportar")
        return False
    fln = fd.asksaveasfilename(initialdir=os.getcwd(), title='Exportar CSV', filetypes=(("CSV File (.csv)", "*.csv"), ("All Files", "*.*")))
    with open(fln, mode='w') as myFile:
        exp_writer = csv.writer(myFile, delimiter=',')
        for i in mydata:
            exp_writer.writerow(i)
    messagebox.showinfo("Data Exportada", "Tu data ha sido exportada a "+ os.path.basename(fln) + " de forma correcta.")
            
## ---------Tkinter ------------

# Creating a menu bar with the options "Test Connection", "Show Tables", and "Exit".
menubar=Menu(root) 
menuFile=Menu(menubar, tearoff=0)
menuFile.add_command(label="Probar conexión", command=tryConnection)
menuFile.add_command(label="Mostrar tablas", command=showTables)
menuFile.add_command(label="Salir", command=destroyApp)
menubar.add_cascade(label="Archivo", menu=menuFile)

# Creating a menu bar with the options "Insert Values", "Delete Rows", "Fetch One" and "Modify Rows".
menuGeneral=Menu(menubar, tearoff=0)
menuGeneral.add_command(label="Insertar Valores", command=insertMultipleRecords)
menuGeneral.add_command(label="Eliminar filas", command=deletingRows)
menuGeneral.add_command(label="Modificar Filas", command=modifyRows)
menuGeneral.add_command(label="Buscar", command=searchData)
menubar.add_cascade(label="General",menu=menuGeneral)

# Creating a treeview with the columns "id", "event_name", "event_date", "event_desc", and "agents".
tree = ttk.Treeview(frame, column=("id", "event_name", "event_date", "event_desc", "agents"), show='headings')
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

# Creating a scrollbar and packing it to the right side of the frame.
sb = Scrollbar(frame, orient=VERTICAL)
sb.pack(side=RIGHT, fill=Y)

# Creating a button that calls the function displayData() when it is clicked.
button1 = tk.Button(text="Refrescar data", command=displayData)
button1.pack(padx=10, pady=0)

button2 = tk.Button(text="Exportar a Excel", command=export2CSV)
button2.pack(padx=10, pady=10)

# Configuring the menu bar, the treeview, and the scrollbar.
root.config(menu=menubar)
tree.config(yscrollcommand=sb.set)
sb.config(command=tree.yview)

root.mainloop()

