import os

from moviepy import *

# Import/Solução temporaria para permitir converter em .exe
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.editor import AudioFileClip as AudioClip
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize
from pytube import YouTube


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
        stream = (
            yt.streams.filter(only_audio=True, subtype=subtype).order_by("abr").last()
        )
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
        stream = (
            yt.streams.filter(file_extension="mp4", progressive=True)
            .order_by("resolution")
            .last()
        )
        stream.download(path)

    def convert_mp3(self, path, stream):
        clip = AudioClip(str(stream.download(path)))
        clip.write_audiofile(str(stream.download(path)).replace(".mp4", ".mp3"))
        os.remove(str(stream.download(path)))

    def download_video(self):
        path = self._user_dir
        fmt_type = self._format_type
        separador = "-" * 30 + "\n"
        status = separador + "Pasta: " + path + "\n" "Formato: " + fmt_type.upper()
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
                else:
                    if fmt_type in ("mp4", "video"):
                        self.salva_mp4(path, yt)
                    else:
                        print("Formato incorreto ou não disponível!")
            except Exception as erro:
                print("Erro de conexão", erro)
        self.clear_list()
