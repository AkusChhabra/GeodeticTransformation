"""
Transform Coords GUI V1.0
Made by A.Chhabra

GUI to simplify conversion of MGA94 and GDA2020 grid coordinates to WGS84 geographical coordinates

"""

import tkinter as tk
from tkinter import filedialog, Menu, Toplevel
from tkinter import ttk
import tkinter.font as tkFont
from transform_coords import main
from PIL import Image, ImageTk

def throwError():
    raise ValueError("An error has occurred.")

def upload_file():
    try:
        global file_path
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        entry_text.set(file_path)
        read_file(file_path)
    except ValueError:
        throwError()  

def read_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.split("\t")
            file_data= (line[0].rstrip(), line[1].rstrip())
            tree.insert("", "end", values=file_data)

def transform():
    try:
        main(entry_text.get(), selected_value_grid.get(), selected_value_zone.get())
    except ValueError:
        throwError()  

class NewWindow(Toplevel):
    def __init__(self, window=None):
        super().__init__(window)
        self.title("About")
        self.geometry("250x150")

        tk.Label(self, 
                text="Made by Akus Chhabra. \n\nTransform MGA94 and GDA2020 grid\ncoordinates into WGS84 \ngeographic coordinates.").pack()

def donothing():
    return


## Initialize window

window = tk.Tk()

window.title("Coordinate Transformer V1.0")

xDim, yDim = 700, 400

menubar = Menu(window)
about = Menu(menubar, tearoff=0)
menubar.add_command(label="About", command=lambda: NewWindow(window))

file = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file)
#file.add_command(label="New", command=donothing)
#file.add_command(label="Open", command=donothing)
#file.add_command(label="Save", command=donothing)
file.add_separator()
file.add_command(label="Exit", command=window.quit)
window.config(menu=menubar)

original = Image.open("./assets/Skywise_Gradient.png")
resized = original.resize((xDim, yDim))
img = ImageTk.PhotoImage(resized)


## Create label to hold background

bg_label = tk.Label(window, image=img)
bg_label.place(relwidth=1, relheight=1)

window.minsize(xDim, yDim)
window.maxsize(xDim, yDim)

entry_text = tk.StringVar()
ent1 = tk.Entry(window, width=40, state=tk.DISABLED, textvariable=entry_text)
entry_text.set("Please upload a file.")
ent1.grid(row=2, column=3)


## Select Grid System

label_grid = tk.Label(window, text="Select Grid Coordinate System:", font="Inter", fg="white", bg="#011133")
label_grid.grid(row=0, column=0, padx=5, pady=5)

grid_opts = ["MGA94", "GDA2020"]
selected_value_grid = tk.StringVar(window)
selected_value_grid.set(grid_opts[0])

dropdown_grid = tk.OptionMenu(window, selected_value_grid, *grid_opts)
dropdown_grid.config(font="Inter", fg="white", bg="#a51890",)
dropdown_grid.grid(row=0, column=1, padx=5, pady=5)


## Zone Number

zone_opts = []

for i in range(48, 59):
    zone_opts.append(str(i))

label_grid = tk.Label(window, text="Enter Zone Number:", font="Inter", fg="white", bg="#011133")
label_grid.grid(row=1, column=0, padx=5, pady=5)

selected_value_zone = tk.StringVar(window)
selected_value_zone.set(zone_opts[0])

dropdown_zone = tk.OptionMenu(window, selected_value_zone, *zone_opts)
dropdown_zone.config(font="Inter", fg="white", bg="#a51890",)
dropdown_zone.grid(row=1, column=1, padx=5, pady=5)


## Upload Document

label_upload = tk.Label(window, font="Inter", fg="white", bg="#011133", text="Upload File:")
label_upload.grid(row=2, column=0, padx=5, pady=5)

upload_btn = tk.Button(window, text="Upload Document", font="Inter", fg="white", bg="#a51890", command=upload_file)
upload_btn.grid(row=2, column=1, padx=5, pady=5)

## Display Coordinates

coord_header = ["Easting", "Northing"]
file_data = []

cols = ("Easting", "Northing")
tree = ttk.Treeview(window, columns=cols, show='headings')

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

tree.grid(row=3, column=0, padx=5, pady=5)



## Transform coordinates

compute_btn = tk.Button(window, text="Transform", font="Inter", fg="white", bg="#a51890", borderwidth=4, height=5, width=15, 
                        command=transform)
compute_btn.grid(row=3, column=1, padx=5, pady=10)

window.mainloop()