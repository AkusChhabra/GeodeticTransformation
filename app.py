"""
Transform Coords GUI V1.0
Made by A.Chhabra

GUI to simplify conversion of MGA94 and GDA2020 grid coordinates to WGS84 geographical coordinates

"""

import os, sys
import tkinter as tk
from subprocess import Popen
from tkinter import filedialog, Menu, Toplevel
from tkinter import ttk
from src.transform_coords import main
from src.checks import *
from PIL import Image, ImageTk

#def resource_path(relative_path):
#    if hasattr(sys, '_MEIPASS'):
#        return os.path.join(sys._MEIPASS, relative_path)
#    return os.path.join(os.path.abspath("."), relative_path)

def upload_file():
    try:
        global file_path
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        compute_btn.config(state="normal")

        tree.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
        scroll_coord_tree.place(x=30+200+2, y=140, height=250)

        try:        
            entry_text.set(file_path)
        except Exception:
            fileUploadFailDialogBox()

        read_file(file_path)

    except Exception:
        noFileFoundDialogBox()

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.split("\t")
                file_data= (line[0].rstrip(), line[1].rstrip())
                tree.insert("", "end", values=file_data)
        fileUploadedDialogBox()
    except ValueError:
        throwError()

def transform():
    try:
        global transformed_data
        transformed_data = main(entry_text.get(), selected_value_grid.get(), selected_value_zone.get())

        for i in range(len(transformed_data)):
            tree_transformed.insert("", "end", values=transformed_data[i])
        notebook.select(frame2)
    except Exception:
        throwError()  

def export_data():
    try:
        global save_path
        save_path = filedialog.asksaveasfilename(
            initialdir="/",
            title="Save File",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("all files", "*.*"))
        )

        if save_path and transformed_data:
            with open(save_path, "w") as file:
                file.write("LATITUDE\tLONGITUDE\n")
                for i in range(len(transformed_data)):
                    line = str(transformed_data[i][0])+ "\t" + str(transformed_data[i][1]) + "\n"
                    file.write(line)
            ask_open_file()
    except ValueError:
        throwError()

def open_file():
        installation_path = check_notepad_plus_plus()
        if installation_path:
            Popen(["C:/Program Files/Notepad++/notepad++.exe", save_path])
        else:
            Popen(["notepad.exe", save_path])

def ask_open_file():
    try:
        # Ask to open file
        open_file_dialog_window = tk.Toplevel(window)
        open_file_dialog_window.title("Open File")
        open_file_dialog_window.geometry("250x150")
        open_file_dialog_window.iconbitmap(os.path.join(os.path.dirname(__file__), "./assets/earth.ico"))
        
        tk.Label(open_file_dialog_window, 
                 text="\nWould you like to open the saved file?").pack()
        tk.Button(open_file_dialog_window, text="Yes", command=lambda: (open_file(), open_file_dialog_window.destroy())).pack(side="left", padx=50)
        tk.Button(open_file_dialog_window, text="No", command=open_file_dialog_window.destroy).pack(side="left", padx=20)

    except ValueError:
        throwError()

def check_notepad_plus_plus():
    paths = [
        r"C:\Program Files\Notepad++\notepad++.exe",
        r"C:\Program Files (x86)\Notepad++\notepad++.exe"
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None

class NewWindow(Toplevel):
    def __init__(self, window=None):
        super().__init__(window)
        self.title("About")
        self.geometry("250x150")
        self.iconbitmap(os.path.join(os.path.dirname(__file__), "./assets/earth.ico"))

        tk.Label(self, 
                text="Made by Akus Chhabra. \n\nTransform MGA94 and GDA2020 grid\ncoordinates into WGS84 \ngeographic coordinates.").pack()


## Initialize window

window = tk.Tk()
window.title("Coordinate Transformer V1.0")

## Set app icon
  
ico = Image.open(os.path.join(os.path.dirname(__file__), "./assets/earth.png"))
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

## Stylize app

style = ttk.Style(window)

window.tk.call('source', os.path.join(os.path.dirname(__file__), './assets/forest-dark.tcl'))
style.theme_use('forest-dark')

## Dimensions and Menubar

xDim, yDim = 700, 475

menubar = Menu(window)
about = Menu(menubar, tearoff=0)
menubar.add_command(label="About", command=lambda: NewWindow(window))

file = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file)
file.add_command(label="Exit", command=window.quit)
window.config(menu=menubar)

original = Image.open(os.path.join(os.path.dirname(__file__), "./assets/Skywise_Gradient.png"))
resized = original.resize((xDim, yDim))
img = ImageTk.PhotoImage(resized)


notebook = ttk.Notebook(window)
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)

frame2.grid_columnconfigure(0, weight=1)
frame2.grid_rowconfigure(0, weight=1)

notebook.add(frame1, text="Input")
notebook.add(frame2, text="Output")
tk.Grid.rowconfigure(window, 0, weight=1)
tk.Grid.columnconfigure(window, 0, weight=1)
notebook.grid(column=0, row=0, sticky=tk.E+tk.W+tk.N+tk.S)

### FRAME 1 CONFIG

## Create label to hold background

bg_label = tk.Label(frame1, image=img)
bg_label.place(relwidth=1, relheight=1)

window.minsize(xDim, yDim)
window.maxsize(xDim, yDim)

entry_text = tk.StringVar()
ent1 = tk.Entry(frame1, width=40, state=tk.DISABLED, textvariable=entry_text)
entry_text.set("Please upload a file.")
ent1.grid(row=2, column=3)


## Select Grid System

label_grid = tk.Label(frame1, text="Select Grid Coordinate System:", font="Inter", fg="white", bg="#011133")
label_grid.grid(row=0, column=0, padx=5, pady=5)

grid_opts = ["MGA94", "GDA2020"]
selected_value_grid = tk.StringVar(frame1)
selected_value_grid.set(grid_opts[0])

dropdown_grid = tk.OptionMenu(frame1, selected_value_grid, *grid_opts)
dropdown_grid.config(font="Inter", fg="white", bg="#a51890",)
dropdown_grid.grid(row=0, column=1, padx=5, pady=5)


## Zone Number

zone_opts = []

for i in range(48, 59):
    zone_opts.append(str(i))

label_grid = tk.Label(frame1, text="Enter Zone Number:", font="Inter", fg="white", bg="#011133")
label_grid.grid(row=1, column=0, padx=5, pady=5)

selected_value_zone = tk.StringVar(frame1)
selected_value_zone.set(zone_opts[0])

dropdown_zone = tk.OptionMenu(frame1, selected_value_zone, *zone_opts)
dropdown_zone.config(font="Inter", fg="white", bg="#a51890",)
dropdown_zone.grid(row=1, column=1, padx=5, pady=5)

## Transform coordinates

compute_btn = tk.Button(frame1, text="Transform", font="Inter", fg="white", bg="#a51890", borderwidth=4, height=5, width=15, 
                        command=transform)
compute_btn.config(state="disabled")
compute_btn.grid(row=3, column=1, padx=5, pady=10)

## Upload Document

label_upload = tk.Label(frame1, font="Inter", fg="white", bg="#011133", text="Upload File:")
label_upload.grid(row=2, column=0, padx=5, pady=5)

upload_btn = tk.Button(frame1, text="Upload Document", font="Inter", fg="white", bg="#a51890", command=upload_file)
upload_btn.grid(row=2, column=1, padx=5, pady=5)

## Display Coordinates

coord_header = ["Easting", "Northing"]
file_data = []

cols = ("Easting", "Northing")
tree = ttk.Treeview(frame1, columns=cols, show='headings')

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

scroll_coord_tree = ttk.Scrollbar(frame1, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll_coord_tree.set)


## FRAME 2 CONFIG

bg_label = tk.Label(frame2, image=img)
bg_label.place(relwidth=1, relheight=1)

coord_header2 = ["Latitude", "Longitude"]
file_data = []

cols2 = ("Latitude", "Longitude")
tree_transformed = ttk.Treeview(frame2, columns=cols2, show='headings')

for col2 in cols2:
    tree_transformed.heading(col2, text=col2)
    tree_transformed.column(col2, width=100, anchor="center")

tree_transformed.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

scroll_coord_tree_output = ttk.Scrollbar(frame2, orient="vertical", command=tree_transformed.yview)
scroll_coord_tree_output.place(x=(30+200+25)*2, y=10, height=yDim-83)

tree_transformed.configure(yscrollcommand=scroll_coord_tree_output.set)


export_btn = tk.Button(frame2, text="Export", font="Inter", fg="white", bg="#a51890", command=export_data)
export_btn.grid(row=0, column=1, padx=50)

window.mainloop()