"""Solute - a steganography software tool

Author: SathvikPN
Project link: https://github.com/SathvikPN/Solute
"""


# Imports -----------------------------------------------------
import tkinter as tk
from tkinter import BitmapImage, Frame, messagebox
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

        # Layout Configuration 
        self.grid_rowconfigure((0,1,9), weight=1)
        self.grid_rowconfigure((2,3,4,5,6,7,8), weight=2)
        self.grid_columnconfigure((0,1), weight=1)

        # Header Section
        HEADER = "SOLUTE"
        header = tk.Label(self)
        header.config(text=HEADER)
        header.config(font=('Verdana',20))
        header.grid(row=0, column=0, columnspan=2)

        # Tagline section
        TAG_LINE = "Simplified steganography tool for your data privacy"
        tagline = tk.Label(self)
        tagline.config(text=TAG_LINE)
        tagline.config(font=('Verdana',12))
        tagline.grid(row=1, column=0, columnspan=2)
        tagline.grid_anchor('s')

        # Load Image
        # self.image = filedialog.askopenfilename(filetypes=[("Image files",".png .jpeg .jpg .bmp")])


        # Configure container inside root window 
        # Container frame serves pages
        container = tk.Frame(self)
        container.grid(row=2, column=0)

        # Footer section
        FOOTER = "Developed by [ SathvikPN ]"
        footer = tk.Label(self)
        footer.config(text=FOOTER)
        footer.grid(row=9, column=0, columnspan=2, pady=5, sticky='s')
        



        self.frames = {}
        self.pages = [Workspace]
        for F in self.pages:    
            # THIS_CASE: F = Workspace
            page_name = F.__name__ 
            # IF_CASE: F=Workspace() ==> page_name=F.__class__.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

        # Display Starting page in container
        self.show_frame("Workspace")


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

class Workspace(tk.Frame):
    """ Dynamic content of the app served here """
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        btn_start = tk.Label(text="Center of Workspace")
        btn_start.grid(row=2, column=0, rowspan=7, columnspan=2)

        
if __name__=='__main__':
    app = SoluteApp()
    app.run()