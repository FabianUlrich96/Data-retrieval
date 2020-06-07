from tkinter import Tk
from tkinter.filedialog import askopenfilename


class UserSelection:

    @staticmethod
    def user_input(prompt):
        Tk().withdraw()
        open_file = askopenfilename(title=prompt)
        print(open_file)
        file_name = input("Please enter a file name:") + ".csv"

        return open_file, file_name