"""Solute - a steganography software tool

Author: SathvikPN
Project link: https://github.com/SathvikPN/Solute
"""


# Imports -----------------------------------------------------
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
# -------------------------------------------------------------

class SoluteApp(tk.Tk):
    """ Root Window of application """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Root page configuration -----------------------------
        self.geometry('800x600')
        self.minsize(width=650, height=550)

        self.title("Solute")
        self.protocol("WM_DELETE_WINDOW", self.exit)


        # Layout Configuration --------------------------------
        DIMENSIONS = {"Rows":16, "Columns":6}
        for r in range(DIMENSIONS['Rows']):
            self.grid_rowconfigure(r, weight=1)
        for c in range(DIMENSIONS['Columns']):
            self.grid_columnconfigure(c, weight=1)


        # Header Section --------------------------------------
        HEADER = "SOLUTE"
        header = tk.Label(self)
        header.config(text=HEADER)
        header.config(font=('Verdana',16))
        header.config(pady=1)
        header.grid(row=0, column=0, columnspan=6, sticky='nsew')


        # Tagline section -------------------------------------
        TAG_LINE = "Simplified steganography tool for your data privacy"
        tagline = tk.Label(self)
        tagline.config(text=TAG_LINE)
        tagline.config(font=('Verdana',12))
        tagline.grid(row=1, column=0, columnspan=6, sticky='n')
         
        
        # Workspace Area --------------------------------------
        # Configure container inside root window 
        # Container frame serves pages
        container = tk.Frame(self)
        container.grid(row=2, column=0, rowspan=13, columnspan=6)

        self.frames = {}
        self.pages = [Workspace]
        for F in self.pages:    
            # IF_CASE: F=Workspace() ==> page_name=F.__class__.__name__
            # THIS_CASE: F = Workspace
            page_name = F.__name__ 
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

        # Display Starting page in container
        self.show_frame("Workspace")


        # Footer section --------------------------------------
        FOOTER = "Developed by [ SathvikPN ]"
        footer = tk.Label(self)
        footer.config(text=FOOTER)
        footer.grid(row=15, column=0, columnspan=6, sticky='s')


    def show_frame(self, page_name):
        """ Display passed page 
        
        Multiple pages are stacked at same container
        raises passed page to top of stack which is displayed
        """
        frame = self.frames[page_name]
        frame.tkraise()


    def exit(self):
        # Exit Confirmation Message box
        TITLE = "Exit"
        MESSAGE = "Are you sure want to exit?"

        sure = messagebox.askyesno(TITLE, MESSAGE )
        if sure is True:
            self.destroy()


    def run(self):
        self.mainloop()



# Workspace Area ----------------------------------------------

class Workspace(tk.Frame):
    """ Workspace of the Application """
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        btn_start = tk.Label(text="Center of Workspace")
        btn_start.grid(row=2, column=0, rowspan=13, columnspan=6)



# APP TRIGGER -------------------------------------------------
if __name__=='__main__':
    app = SoluteApp()
    app.run()