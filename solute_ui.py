"""Solute - a steganography software tool

Author: SathvikPN
Project link: https://github.com/SathvikPN/Solute
"""


# Imports -----------------------------------------------------
import tkinter as tk
from tkinter import messagebox


# Root Window of Application
class SoluteApp(tk.Tk):
    """ Home Page of application """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Root page configuration 
        self.geometry('800x550')
        self.minsize(width=650, height=450)

        self.title("Solute")
        self.protocol("WM_DELETE_WINDOW", self.exit)
    

    def exit(self):
        # Exit Confirmation Message box
        TITLE = "Exit"
        MESSAGE = "Are you sure want to exit?"
        
        sure = messagebox.askyesno(TITLE, MESSAGE )
        if sure is True:
            self.destroy()


    def run(self):
        self.mainloop()



if __name__=='__main__':
    app = SoluteApp()
    app.run()