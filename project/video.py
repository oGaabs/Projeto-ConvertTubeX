import os
from concurrent.futures import ThreadPoolExecutor
from time import sleep

from moviepy.editor import AudioFileClip as AudioClip
# Import/Solução temporaria para permitir converter em .exe
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.video.fx.crop import crop
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate

from config import Stats as status
from config import clear
from pytube import Playlist, YouTube


class Video:
    def __init__(self, user_dir, save_type):
        self._user_dir = user_dir
        self._save_type = save_type.upper()
        self._video_list = []
        self._video_cont = 0

    @property
    def user_dir(self):
        return self._user_dir

    @user_dir.setter
    def user_dir(self, user_dir):
        if user_dir is None:
            return print('Caminho inválido')
        if not os.path.isdir(user_dir):
            return print("Caminho não encontrado!")

        self._user_dir = user_dir

    @property
    def save_type(self):
        return self._save_type

    @save_type.setter
    def save_type(self, save_type):
        if save_type is None or save_type.upper() not in ("MP3", "AUDIO", "MP4", "VIDEO"):
            return print("Formato não suportado, use (MP3, AUDIO, MP4, VIDEO)!")

        self._save_type = save_type.upper()

    @property
    def video_cont(self):
        return self._video_cont

    @video_cont.setter
    def video_cont(self, video_cont):
        if video_cont is None or video_cont < 0:
            return print("Insira apenas números naturais!")

        self._video_cont = video_cont

    @property
    def video_list(self):
        return self._video_list

    @video_list.setter
    def video_list(self, arr):
        self._video_list = arr

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
        self._save_type = ""

    def salva_mp3(self, link):
        path = self.user_dir
        yt = YouTube(link)
        stream = (yt.streams.filter(only_audio=True,
                                    subtype="mp4").order_by("abr").last())
        stream.download(path)
        try:
            self.convert_mp3(path, stream)
        except Exception as ex:
            print(ex)
            print(status.create_str_status(
                "Erro ao converter, verifique o caminho ", path,
                ", o arquivo foi salvo em .mp4, para contornar o erro."
            ))
        self.remove(link)

    def salva_mp4(self, link):
        path = self.user_dir
        yt = YouTube(link)
        stream = (yt.streams.filter(
            file_extension="mp4",
            progressive=True).order_by("resolution").last())
        stream.download(path)
        self.remove(link)

    def convert_mp3(self, path, stream):
        clip = AudioClip(str(stream.download(path)))
        clip.write_audiofile(
            str(stream.download(path)).replace(".mp4", ".mp3"), verbose=False, logger=None)
        os.remove(str(stream.download(path)))

    def download_video(self):
        path, file_type, videos = self.user_dir, self.save_type, self.video_list
        videos_length_fixed = self.video_cont
        save_dir = ("Pasta: " + path + "\n"
                    "Formato: " + file_type + "\n")
        clear()
        print(status.create_str_status(status, save_dir +
              "Quantidade de vídeos: " + str(videos_length_fixed)), end="\r")
        try:
            with ThreadPoolExecutor() as executor:
                if file_type in ("MP3", "AUDIO", ""):
                    executor.map(self.salva_mp3, videos)
                elif file_type in ("MP4", "VIDEO"):
                    executor.map(self.salva_mp4, videos)
                else:
                    print("Formato incorreto ou não disponível!")
                pontos = 1
                while True:
                    sleep(1)
                    clear()
                    if pontos == 4:
                        pontos = 1
                    progresso_baixados = str(
                        videos_length_fixed - len(videos)) + "\\" + str(videos_length_fixed)
                    porcentagem = (100 * (videos_length_fixed -
                                   len(videos)) // videos_length_fixed)
                    print(status.create_str_status(status, save_dir + "Quantidade de vídeos: " + progresso_baixados) + "\n"
                          "Baixando" + ("." * pontos) + " \n  | " + ("▰ " * (porcentagem // 5)) + ("▱ " * ((100 - porcentagem) // 5)) + " | " +
                          str(porcentagem) + "%" + " completo\n\n", end="\r")
                    pontos += 1
                    if len(videos) == 0:
                        break
        except Exception as e:
            raise e
        self.clear_list()
        clear()
        print(status.create_str_status(status,
                                       "Pasta: " + path + "\n"
                                       "Formato: " + file_type + "\n"
                                       "Quantidade de vídeos: " + str(len(videos))))

    def is_playlist(self, link):
        if link.find("playlist?list=") == -1 or link.find("watch") != -1:
            return False
        return True
