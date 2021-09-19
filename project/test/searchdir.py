import os
from tkinter import Tk
from tkinter.filedialog import askdirectory


def clear():
    # Limpa o console e volta pra primeira linha sem precisar importar OS
    print("\033[H\033[J", end="")


def get_directory():
    separador = "-" * 30 + "\n"
    while True:
        path_dir = input(separador + "\nEscolha o local de salvamento\n"
                         "1) Digite 1 para escolher um local de salvamento"
                         " personalizado\n"
                         "2) Digite 2 para escolher o local de salvamento"
                         " padrão;\n")
        if path_dir in ("1", ""):
            root = Tk()
            save_dir = askdirectory()
            if save_dir == "":
                clear()
                print(separador + "Caminho não encontrado!")
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
            print(separador + "Opção incorreta!")
