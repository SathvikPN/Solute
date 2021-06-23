""" Solute - a steganography software tool 

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
            self.grid_rowconfigure(r, weight=1, minsize=2)
        for c in range(DIMENSIONS['Columns']):
            self.grid_columnconfigure(c, weight=1, minsize=2)


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

        # btn_start = tk.Label(text="Center of Workspace")
        # btn_start.grid(row=2, column=0, rowspan=13, columnspan=6)

        # IMAGE SELECTOR SECTION ------------------------------
        step1 = tk.Label(text="Step 1: Input Image")
        step1.grid(row=2, column=1)

        self.step1_path = tk.Entry()
        self.step1_path.grid(row=2, column=2, columnspan=2, sticky='ew')

        self.step1_btn = tk.Button(text="Select File")
        self.step1_btn.config(command=self.image_selector)
        self.step1_btn.grid(row=2, column=4)

        
        # ENCODER Section -------------------------------------
        encode_header = tk.Label(text="ENCODE")
        encode_header.config(font=14)
        encode_header.grid(row=3, column=0, columnspan=3)

        step2_enc = tk.Label(text="Step 2")
        step2_enc.grid(row=4, column=0)

        step2_enc_info = tk.Label(text="Enter text to hide")
        step2_enc_info.grid(row=5, column=0)

        encode_data = tk.Text(height=TEXT_BOX_HEIGHT)
        encode_data.grid(row=6,column=0, rowspan=4, columnspan=3) #   

        step3 = tk.Label(text="Step 3")
        step3.grid(row=10, column=0)

        step3_info = tk.Label(text="Enter Password")
        step3_info.grid(row=11, column=0)

        pwd_enc = tk.Entry()
        pwd_enc.config(show='*')
        pwd_enc.grid(row=11, column=1, columnspan=2)

        # ROW:12 COLUMN:(0,1,2) --> ADD PROGRESS BAR

        encode_btn = tk.Button(text="Encode and Save")
        encode_btn.config(font=10)
        encode_btn.grid(row=13, rowspan=2, column=1)


        # DECODER Section -------------------------------------
        decode_header = tk.Label(text="DECODE")
        decode_header.config(font=14)
        decode_header.grid(row=3, column=3, columnspan=3)

        step2_dec = tk.Label(text="Step 2")
        step2_dec.grid(row=4, column=3)

        step2_dec_info = tk.Label(text="Enter Password")
        step2_dec_info.grid(row=5, column=3)

        pwd_dec = tk.Entry()
        pwd_dec.config(show='*')
        pwd_dec.grid(row=5, column=4, columnspan=2)

        decode_btn = tk.Button(text="Decode")
        decode_btn.grid(row=6, rowspan=2, column=4)

        # ROW:8 COLUMNS:(3,4,5) ---> ADD PROGRESS BAR

        dec_info = tk.Label(text="Decoded data")
        dec_info.grid(row=9, column=3)

        dec_data = tk.Text(height=TEXT_BOX_HEIGHT)
        dec_data.insert('1.0', DECODED_DATA)
        dec_data.grid(row=10, column=3, rowspan=4,columnspan=3 ) # 





    def image_selector(self):
        FILE_TYPES = ([('Image Files',('.png','.jpg','.jpeg'))])
        img_path = filedialog.askopenfilename(filetypes = FILE_TYPES)
        if not img_path:
            messagebox.showerror("No Image found", "Please select an image")
        else:
            self.step1_path.insert('0',img_path)
    



        





# APP TRIGGER -------------------------------------------------
if __name__=='__main__':
    DEBUG = True
    if DEBUG is True:
        DECODED_DATA = "DEBUG Mode Active."
        TEXT_BOX_HEIGHT = 8
        

    app = SoluteApp()
    app.run()