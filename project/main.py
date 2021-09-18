"""
Esse script utiliza pytube e moviepy para baixar videos do youtube,
fique claro que você esta sujeito a licença desses dois softwares.
O download do arquivo mp3/mp4 é feito utilizando a URL do vídeo de origem
contudo, caso queira utilizar o conteudo para meio não pessoal,
é preciso pedir permissão para o autor.
Você é plenamente responsável pelo uso do script
e está sujeito à lei do seu país, o script é de uso livre, lembrando que
não damos qualquer garantia ou direitos sobre os videos, não é preciso
fazer atribuição do script, mas aprecio a mesma.

Autor: Gabriel
Date: 18/09/21

"""

from searchdir import get_directory
from status import Stats
from video import Video


def main():
    def pega_video():
        end_list = False
        video_cont = 0

        while end_list is False:
            video = input("#> Digite o link do video ou end para finalizar: ")
            if (video_cont != 0) and (video in ("", "end")):
                end_list = True
            else:
                if ("youtu.be" in video) or ("youtube.com/" in video):
                    vid.add(video)
                    video_cont += 1
                else:
                    if video_cont == 0:
                        clear()
                        print(status.status_list)
                        print("Nenhum link foi inserido!\n")
                    else:
                        clear()
                        print(status.status_list)
                        print("Formato de link invalido, tente novamente!\n")
        clear()
        status.add("Quantidade de vídeos: " + str(video_cont))

    def clear():
        # Limpa o console e volta pra primeira linha sem precisar importar OS
        print("\033[H\033[J", end="")

    clear()
    separador = "-" * 30 + "\n"
    user_music = ""
    user_video = ""
    status = Stats()

    while True:
        try:
            print(
                separador + "Bem-vindo ao ConvertTube, conversor de video"
                "do youtube criado em python."
            )

            if user_video == "" or user_music == "":
                user_music, user_video = get_directory()

            clear()
            status.add("Musica: " + user_music + "\n" "Video: " + user_video)

            print(status.status_list)

            format_type = ""
            while format_type == "":

                format_type = input("Digite o tipo (mp3 ou audio," "mp4 ou video): ")
                clear()

                if format_type == "":
                    format_type = "MP3"
                format_type = format_type.upper()

                if format_type in ("MP3", "AUDIO", ""):
                    vid = Video(user_music, "mp3")
                    status.add("Formato: " + format_type)
                    print(status.status_list)
                    pega_video()
                    print(status.status_list)
                else:
                    if format_type in ("MP4", "VIDEO"):
                        vid = Video(user_video, "mp4")
                        status.add("Formato: " + format_type)
                        print(status.status_list)
                        pega_video()
                        print(status.status_list)
                    else:
                        print(status.status_list)
                        print("Formato ", format_type, " incorreto ou indisponível!")
                        format_type = ""
        except Exception as erro:
            print(erro)
            input("Ocorreu um erro:\n" "Pressione enter para continuar")

        vid.download_video()
        clear()
        print(status.status_list + "\nConversão FINALIZADA!")
        input("Pressione 'enter' para recomeçar, ou feche o programa.")
        status.clear_list()
        clear()


if __name__ == "__main__":
    main()
