import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
from config import Stats as status, clear


def get_directory():
    while True:
        path_dir = input("Escolha o local de salvamento\n"
                         "1) Digite 1 para escolher um local de salvamento"
                         " personalizado\n"
                         "2) Digite 2 para escolher o local de salvamento"
                         " padrão;\n")
        if path_dir in ("1", ""):
            root = Tk()
            save_dir = askdirectory()
            if save_dir == "":
                clear()
                print(status.create_str_status("Caminho não encontrado!"))
            else:
                user_music = save_dir
                user_video = save_dir
                root.destroy()
                return user_music, user_video
            root.destroy()
        elif path_dir == "2":
            user_profile = os.environ["USERPROFILE"]
            user_music = user_profile + "/Music/"
            user_video = user_profile + "/Videos/"
            return user_music, user_video
        else:
            clear()
            print(status.create_str_status("Opção incorreta!"))
