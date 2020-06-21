from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re


class UserSelection:

    @staticmethod
    def user_input(prompt):
        Tk().withdraw()
        open_file = askopenfilename(title=prompt)
        print(open_file)

        return open_file

    @staticmethod
    def save_name():
        file_name = input("Please enter a file name:")
        replacements = [(":", "_"), ("/", "_"), ("\\?", ""), ("<", ""), (">", ""), ("\\*", "_"), ("\\|", ""), ("\\\\", "_"), ('"', "")]
        for pattern, replacement in replacements:
            file_name = re.sub(pattern, replacement, file_name)

        return file_name

    @staticmethod
    def check_input(file_path):
        if file_path.endswith('.csv'):
            return True
        else:
            print(file_path + " :does not end with .csv, chose another one")
            return False


