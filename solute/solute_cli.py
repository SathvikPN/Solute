try:
    import core
except ImportError:
    from solute import core 
import inspect


def command_line_interface():
    """ Command Line Interface for the appliction """

    file_info = inspect.cleandoc("""
    ***********************************************************************************
    Solute Application
        Description: Hide text inside an image with additional text encryption layer.
        
    """)
    print(file_info, end='\n\n')


    # -----------------------------------------------------------------------------------
    menu = inspect.cleandoc("""
    ----- MENU -----
    [1]. ENCODE (encrypt data - generate encoded image)
    [2]. DECODE (decrypt data - from encoded image)

    Select your choice(1/2) : 
    """)

    choice = input(menu)

    def data_canvas():
        """ Decorate space for input text data """

        print(inspect.cleandoc("""
        Enter Secret Text Data : (leave blank line to finish)
        ----------------------------------------------------------------
        """))

        datalines = []
        while True:
            line = input()
            if line:
                datalines.append(line)
            else:
                break
        data = '\n'.join(datalines)

        print(inspect.cleandoc("""
        ----------------------------------------------------------------
        """))
        return data

    if choice == "1":
        img = input('Enter cover image name (path with extension): ')
        data = data_canvas()
        pwd = input('Enter password: ')
        enc_img = input('Enter path for output image (.png extension): ')

        try:
            core.encode_img(input_img=img, text=data, output_img=enc_img, password=pwd)

        except core.ReadImageError:
            print(inspect.cleandoc(f"""
            -------------------------------------------------
            ERROR: {core.ReadImageError}
            DETAILS: Cover image path with extension is INVALID.
            -------------------------------------------------
            """))
            exit()

        except core.DataOverflowError:
            print(inspect.cleandoc(f"""
            -------------------------------------------------
            ERROR: {core.DataOverflowError}
            DETAILS: No sufficient storage available in this image
                     for the supplied text data.
            -------------------------------------------------
            """))
            exit()
        
        except core.SaveImageError:
            print(inspect.cleandoc(f"""
            -------------------------------------------------
            ERROR: {core.SaveImageError}
            DETAILS: Save image location with extension is INVALID.
            -------------------------------------------------
            """))
            exit()

        
        print(inspect.cleandoc(f"""
        -------------------------------------------------
        ENCODING SUCCESSFUL
        Generated the encoded image successfully.
        -------------------------------------------------
        """))

    
    elif choice == '2':
        img_file = input('Enter encoded_image path (with image extension): ')
        pwd = input('Enter password: ')
        if not img_file.endswith('.png'):
            print(inspect.cleandoc(f"""
            -------------------------------------------------
            ERROR: {core.ReadImageError}
            DETAILS: Valid cover image will be in PNG format (*.png)
            -------------------------------------------------
            """))
            exit()            

        try:
            decoded_data = core.decode_img(image_path=img_file, password=pwd)

        except core.ReadImageError:
            print(inspect.cleandoc(f"""
            -------------------------------------------------
            ERROR: {core.ReadImageError}
            DETAILS: image path with extension is INVALID.
            -------------------------------------------------
            """))
            exit()

        except core.PasswordError:
            print(inspect.cleandoc(f"""
            -------------------------------------------------
            ERROR: {core.PasswordError}
            DETAILS: INVALID Password
            -------------------------------------------------
            """))
            exit()
        
        print(inspect.cleandoc(f"""
        
Decoded Data:
-------------------------------------------------
{decoded_data}
-------------------------------------------------
"""))

    else:
        print("INVALID choice.")

if __name__=="__main__":
    command_line_interface()