# Imports -----------------------------------------------------

import tkinter as tk
from tkinter import Menu, messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter import font

try:
    import core
except ImportError:
    from solute import core
# -------------------------------------------------------------

# Options 
TEXT_BOX_HEIGHT = 8
PADDINGS = {'padx':10, 'pady':10}

class SoluteApp(tk.Tk):
    """ Root Window of application """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Root page configuration -----------------------------
        self.geometry('800x600')
        self.minsize(width=650, height=550)
        
        self.style = ttk.Style(self)
        self.style.theme_use('winnative')

        self.title("Solute")
        self.protocol("WM_DELETE_WINDOW", self.exit)


        # Layout Configuration --------------------------------
        DIMENSIONS = {"Rows":16, "Columns":6}
        for r in range(DIMENSIONS['Rows']):
            if r==2 or r==3:
                self.grid_rowconfigure(r, weight=1, pad=30)
            self.grid_rowconfigure(r, weight=1, minsize=2)
        for c in range(DIMENSIONS['Columns']):
            self.grid_columnconfigure(c, weight=1, minsize=2)

            
        # Icon section ----------------------------------------
        self.iconbitmap('assets/favicon_solute.ico')


        # Menubar Section -------------------------------------
        menubar = Menu(self)
        file = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=file)
        file.add_command(label="About", command=self.developer_info)
        self.config(menu=menubar)


        # Header Section --------------------------------------
        HEADER = "SOLUTE"
        header = tk.Label(self)
        header.config(text=HEADER)
        header.config(font=('Verdana',16))
        header.config(pady=1)
        header.grid(row=0, column=0, columnspan=6, sticky='nsew')


        # Tagline section -------------------------------------
        TAG_LINE = "--- Simplified steganography tool for your data privacy ---"
        tagline = tk.Label(self)
        tagline.config(text=TAG_LINE)
        # tagline.config(font=('Verdana',12))
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

    def developer_info(self):
        messagebox.showinfo(
            "Developer Info",
            "[Name] SathvikPN\n[GitHub] https://github.com/SathvikPN/Solute"
        )


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

        # SEPARATOR 
        # ttk.Separator(orient=VERTICAL).grid(column=2, row=4, rowspan=10, sticky='ns')

        # ENCODER Section -------------------------------------
        encode_header = tk.Label(text="ENCODE")
        encode_header.config(font=('Verdana',14,'bold'))
        encode_header.grid(row=3, column=0, columnspan=3, sticky='s')


        step2_enc = tk.Label(text="Step 2")
        step2_enc.grid(row=4, column=0, sticky='w', **PADDINGS)

        step2_enc_info = tk.Label(text="Enter text to hide")
        step2_enc_info.grid(row=5, column=0, sticky='w', **PADDINGS)

        self.encode_data = tk.Text(height=TEXT_BOX_HEIGHT)
        self.encode_data.grid(row=6,column=0, rowspan=4, columnspan=3, **PADDINGS) #   

        step3 = tk.Label(text="Step 3")
        step3.grid(row=10, column=0, sticky='w', **PADDINGS)

        step3_info = tk.Label(text="Enter Password")
    
        step3_info.grid(row=11, column=0, sticky='w', **PADDINGS)

        self.pwd_enc = tk.Entry()
        self.pwd_enc.config(show='*')
        self.pwd_enc.grid(row=11, column=1, columnspan=2, sticky='w', **PADDINGS)

        # ROW:12 COLUMN:(0,1,2) --> ADD PROGRESS BAR

        encode_btn = tk.Button(text="Encode and Save")
        encode_btn.config(font=8)
        encode_btn.config(command=self.save_encode)
        encode_btn.grid(row=13, rowspan=2, column=0, columnspan=3, sticky='ns')
        


        # DECODER Section -------------------------------------
        decode_header = tk.Label(text="DECODE")
        decode_header.config(font=('Verdana',14,'bold'))
        decode_header.grid(row=3, column=3, columnspan=3, sticky='s')

        step2_dec = tk.Label(text="Step 2")
        step2_dec.grid(row=4, column=3, sticky='w', **PADDINGS)

        step2_dec_info = tk.Label(text="Enter Password")
        step2_dec_info.grid(row=5, column=3, sticky='w', **PADDINGS)

        self.pwd_dec = tk.Entry()
        self.pwd_dec.config(show='*')
        self.pwd_dec.grid(row=5, column=4, columnspan=2, sticky='ew', **PADDINGS)

        decode_btn = tk.Button(text="Decode")
        decode_btn.config(font=8)
        decode_btn.config(command=self.decode)
        decode_btn.grid(row=6, column=4, sticky='ns')

        # ROW:7 COLUMNS:(3,4,5) ---> ADD PROGRESS BAR

        dec_info = tk.Label(text="Decoded data")
        dec_info.grid(row=8, column=3, sticky='w', **PADDINGS)

        self.dec_data = tk.Text(height=TEXT_BOX_HEIGHT)
        self.dec_data.grid(row=10, column=3, rowspan=4,columnspan=3,sticky='w', **PADDINGS ) # 





    def image_selector(self):
        self.step1_path.delete('0', 'end')
        FILE_TYPES = ([('Image Files',('.png','.jpg','.jpeg'))])
        self.img_path = filedialog.askopenfilename(filetypes = FILE_TYPES)
        if not self.img_path:
            messagebox.showwarning("No Image found", "Please select an image")
        else:
            self.step1_path.insert('0',self.img_path)
            return self.step1_path

    def save_encode(self):
        # self.step1_path = tk.Entry()
        # self.encode_data = tk.Text(height=TEXT_BOX_HEIGHT)
        # self.pwd_enc = tk.Entry()
        self.enc_img = filedialog.asksaveasfilename(title='Save file') # filetypes=[("PNG", ".png")]
        self.enc_img = self.enc_img+'.png'
        try:
            core.encode_img(
                self.step1_path.get(),
                self.encode_data.get("1.0","end-1c"),
                self.enc_img,
                self.pwd_enc.get()
            )
            messagebox.showinfo(
                title="Encode SUCCESS",
                message="Encoded image generated successfully.\nYay!"
            )

            self.step1_path.delete('0', 'end')
            self.encode_data.delete("1.0", "end")
            self.pwd_enc.delete('0','end')
        
        except core.DataOverflowError:
            messagebox.showwarning(
                title="Data Overflow",
                message="Data size is too big to fit inside this image"
            )

        except core.ReadImageError:
            messagebox.showerror(
                title="No Image Selected",
                message="Please select a source image to hide data."

            )


    
    def decode(self):
        # self.pwd_dec = tk.Entry()
        self.dec_data.delete("1.0","end")
        if not self.step1_path.get().endswith('.png'):
            messagebox.showinfo(
                "Incorrect Image",
                "Please select the valid image to decode\nPNG format image."
            )
            self.step1_path.delete('0','end')
        else:
            try:
                self.dec_data.insert(
                    "1.0", 
                    core.decode_img(self.step1_path.get(), self.pwd_dec.get())
                )
                messagebox.showinfo(
                    title="Decode SUCCESS",
                    message="Data extracted successfully from the image.\nYay!"
                )

            except core.PasswordError:
                messagebox.showerror(
                    title="Incorrect Credentials",
                    message="Please ensure correct image and correct password is entered."
                )
                self.pwd_dec.delete('0', 'end')

            except core.ReadImageError:
                messagebox.showerror(
                    title="No Image Selected",
                    message="Please select an image to decode"
                )






# APP TRIGGER -------------------------------------------------
if __name__=='__main__':
    app = SoluteApp()
    app.run()