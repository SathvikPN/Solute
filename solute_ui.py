"""Solute - a steganography software tool

Author: SathvikPN
Project link: https://github.com/SathvikPN/Solute
"""


# Imports -----------------------------------------------------
import tkinter as tk
from tkinter import BitmapImage, messagebox
from tkinter import filedialog


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

        # Header Section
        HEADER = "SOLUTE"
        header = tk.Label(self)
        header.config(text=HEADER)
        header.config(font=('Verdana',20))
        header.pack(side='top')

        # Tagline section
        TAG_LINE = "Simplified steganography tool for your data privacy"
        tagline = tk.Label(self)
        tagline.config(text=TAG_LINE)
        tagline.config(font=('Verdana',12))
        tagline.pack()

        # Load Image
        # self.image = filedialog.askopenfilename(filetypes=[("Image files",".png .jpeg .jpg .bmp")])


        # Footer section
        FOOTER = "Developed by [ SathvikPN ]"
        footer = tk.Label(self)
        footer.config(text=FOOTER)
        footer.pack(side='bottom')


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