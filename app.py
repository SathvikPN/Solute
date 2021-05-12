#!/usr/bin/python3
"""
Graphical User Interface for Steganography Application
Author: Sathvik PN
GitHub: https://github.com/SathvikPN
"""

from src import core, utility, custom_exceptions 

from PyQt5 import QtCore, QtGui, QtWidgets



# -----------------------------------------------
class UI_MainWindow():

    # Function to display Message/Error/Information 
    def display_msg(self, title, msg, ico_type=None):
        MsgBox = QtWidgets.QMessageBox()
        MsgBox.setText(msg)
        MsgBox.setWindowTitle(title)

        if ico_type == 'err':
            ico = QtWidgets.QMessageBox.critical
        else:
            ico = QtWidgets.QMessageBox.information

        MsgBox.setIcon(ico)
        MsgBox.exec()

    # Method to choose input file 
    def get_file(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', '', "Image files (*.jpg *.png *.bmp)")[0]
        if file_path != '':
            self.lineEdit.setText(file_path)

    
    # To display save file dialog
    def save_file(self):
        output_path = QtWidgets.QFileDialog.getSaveFileName(None, "Save encoded file", '', "PNG File (*.png)")[0]
        return output_path


    # Encode and Save File 
    def encode(self):
        input_path = self.lineEdit.text()
        text = self.plainTextEdit.toPlainText()
        password = self.lineEdit_2.text()

        if input_path == '':
            window_title = "ERROR - No file chosen"
            window_text = "You must select input image file"
            window_icon = "err"
            self.display_msg(window_title,window_text,window_icon)

        elif text == '':
            window_title = "Text data is Empty"
            window_text = "Please enter some text to encode..."
            window_icon = "info"
            self.display_msg(window_title, window_text, window_icon)

        elif password == '':
            window_title = "ERROR - Password NOT set"
            window_text = "Please enter a password for security"
            window_icon = "err"
            self.display_msg(window_title, window_text, window_icon)
        
        else:
            output_path = self.save_file()
            if output_path == '':
                self.display_msg("Operation cancelled","Operation cancelled by user!")
            else:
                try:
                    loss = core.encode(input_path, text, output_path, password, self.progressBar)
                except core.FileError as fe:
                    self.display_msg("File Error", str(fe),"err")
                except core.DataOverflowError as doe:
                    self.display_msg("Data Overflow Error", str(doe), "err")
                else:
                    window_title = "Success"
                    window_text = "Encoded Successfully! \n\nImage Data loss {:.4f} %".format(loss)
                    self.display_msg(window_title, window_text)
                    self.progressBar.setValue(0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())