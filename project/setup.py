import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "includes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="ConvertTubeX",
    version="1.0",
    description="Youtube Converter MP4/MP3",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)