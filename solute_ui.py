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

        # Layout Management
        total_rows = 7
        total_columns = 4

        for r in range(total_rows):
            self.grid_rowconfigure(r, pad=10)

        for c in range(total_columns):
            self.grid_columnconfigure(c, pad=10)

        self.grid_columnconfigure((1,2), weight = 4)


        # Header Section
        HEADER = "SOLUTE"
        header = tk.Label(self)
        header.config(text=HEADER)
        header.config(font=('Verdana',20))
        header.grid(row=0, column=0, columnspan=3)

        # Tagline section
        TAG_LINE = "Simplified steganography tool for your data privacy"
        tagline = tk.Label(self)
        tagline.config(text=TAG_LINE)
        tagline.config(font=('Verdana',12))
        tagline.grid(row=1, column=0, columnspan=3, sticky='n')


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