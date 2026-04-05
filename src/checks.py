"""

Create dialog boxes to provide user feedback on improper inputs

"""

from tkinter.messagebox import showinfo

def throwError():
    raise ValueError("An error has occurred.")

def noFileFoundDialogBox():
    showinfo("Error", "Could not find file location.")

def fileUploadedDialogBox():
    showinfo("Success", "File successfully uploaded.")

def fileUploadFailDialogBox():
    showinfo("Error", "File was not uploaded.")
