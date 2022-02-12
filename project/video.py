import os

from moviepy.editor import AudioFileClip as AudioClip
from pytube import Playlist, YouTube


class Video:
    """docstring for ClassName."""
    def __init__(self, user_dir, format_type):
        self._user_dir = user_dir
        self._format_type = format_type
        self._video_list = []
        self._video_cont = 0

    @property
    def user_dir(self):
        """The foo property."""
        return self._user_dir

    @user_dir.setter
    def user_dir(self, user_dir):
        if user_dir is not None and os.path.isdir(user_dir):
            self._user_dir = user_dir
        else:
            print("Caminho não encontrado!")

    @property
    def format_type(self):
        """The foo property."""
        return self._format_type

    @format_type.setter
    def format_type(self, format_type):
        if format_type is not None and format_type.lower() in (
                "mp3",
                "audio",
                "mp3",
                "video",
        ):
            self._format_type = format_type.lower()
        else:
            print("Formato não suportado, use (MP3, AUDIO, MP4, VIDEO)!")

    @property
    def video_cont(self):
        """The video_cont property."""
        return self._video_cont

    @video_cont.setter
    def video_cont(self, video_cont):
        if video_cont is not None and video_cont >= 0:
            self._video_cont = video_cont
        else:
            print("Insira apenas números naturais!")

    @property
    def video_list(self):
        """The video_list property."""
        return self._video_list

    @video_list.setter
    def video_list(self, value):
        self._video_list = value

    def add_cont(self):
        self._video_cont += 1

    def sub_cont(self):
        self._video_cont -= 1

    def add(self, video):
        if self.is_playlist(video):
            video = "youtube.com" + video[video.rfind("/"):]
            playlist = Playlist(video)
            for url in playlist.video_urls:
                video = "youtu.be" + url[url.rfind("/"):]
                if self._video_list.count(video) == 0:
                    self._video_list.append(video)
                    self._video_cont += 1
        else:
            video = "youtu.be" + video[video.rfind("/"):]
            if self._video_list.count(video) == 0:
                self._video_list.append(video)
                self._video_cont += 1

    def remove(self, video_link):
        self._video_list.remove(video_link)
        self._video_cont -= 1

    def pop(self, value):
        self._video_list.pop(value)
        self._video_cont -= 1

    def clear_list(self):
        self._video_list.clear()
        self._video_cont = 0
        self._format_type = ""

    def clear(self):
        # Limpa o console e volta pra primeira linha sem precisar importar OS
        print("\033[H\033[J", end="")

    def salva_mp3(self, path, yt, separador):
        subtype: str = "mp4"
        stream = (yt.streams.filter(only_audio=True,
                                    subtype=subtype).order_by("abr").last())
        stream.download(path)
        try:
            self.convert_mp3(path, stream)
            self.clear()
        except Exception as ex:
            print(ex)
            print(
                separador + "Erro ao converter, verifique ",
                path,
                ", o arquivo foi salvo em .mp4, para contornar o erro.\n",
                separador,
            )

    def salva_mp4(self, path, yt):
        stream = (yt.streams.filter(
            file_extension="mp4",
            progressive=True).order_by("resolution").last())
        stream.download(path)
        self.clear()

    def convert_mp3(self, path, stream):
        clip = AudioClip(str(stream.download(path)))
        clip.write_audiofile(
            str(stream.download(path)).replace(".mp4", ".mp3"))
        os.remove(str(stream.download(path)))

    def is_playlist(self, link):
        if link.find("playlist?list=") != -1 and link.find("watch") == -1:
            return True
        return False

    def download_video(self):
        path = self._user_dir
        fmt_type = self._format_type
        separador = "-" * 30 + "\n"
        status = (separador + "Pasta: " + path + "\n"
                  "Formato: " + fmt_type.upper() + "\n"
                  "Quantidade de vídeos: " + str(len(self._video_list)))

        for i in self._video_list:
            try:
                yt = YouTube(i)
                title = yt.title
                self.clear()
                print(status + "\n" + separador)
                print("Baixando Vídeo: " + title)
                print("Link: " + i + "\n")
                if fmt_type in ("mp3", "audio", ""):
                    self.salva_mp3(path, yt, separador)
                elif fmt_type in ("mp4", "video"):
                    self.salva_mp4(path, yt)
                else:
                    print("Formato incorreto ou não disponível!")
            except Exception as erro:
                print("Erro de conexão", erro)
        self.clear_list()
        print(status + "\n" + separador)
