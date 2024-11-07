import os
import subprocess
import concurrent.futures
from static_ffmpeg import run

class ConversionService:
    OVERWRITE_OUTPUT = "-y"
    INPUT_FILE = "-i"
    INCLUDE_ONLY_AUDIO_STREAMS = ["-map", "0:a"]
    VARIABLE_BIT_RATE = ["-q:a", "0"]
    VERBOSE = ["-hide_banner", "-loglevel", "error"]
    DEBUG_MODE = False
    

    def __init__(self, max_workers=4):
        self.max_workers = max(max_workers, os.cpu_count())
        self.ffmpeg_path, _ffprobe = run.get_or_fetch_platform_executables_else_raise()

    def build_ffmpeg_command(self, input_filename, output_filename):
        command = [
            self.OVERWRITE_OUTPUT,
            self.INPUT_FILE, input_filename,
            *self.INCLUDE_ONLY_AUDIO_STREAMS,
            *self.VARIABLE_BIT_RATE,
            output_filename
        ]
        if self.DEBUG_MODE is False:
            command = [self.ffmpeg_path, *self.VERBOSE, *command]
        return command

    def _convert_mp4_to_mp3(self, input_path):
        output_path = os.path.splitext(input_path)[0] + ".mp3"
        ffmpeg_command = self.build_ffmpeg_command(input_path, output_path)

        try:
            subprocess.run(ffmpeg_command, shell=True, check=True)
            
            if os.path.exists(output_path):
                os.remove(input_path)
                
                return output_path
            else:
                print(f"Output file not created for {input_path}.")
                return None
            
        except Exception as e:
            print(f"Error converting {input_path} to MP3: {e}")
            return None

    def convert_mp4_to_mp3(self, video_files, progress_callback=None):
        try:
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self._convert_mp4_to_mp3, file_path) for file_path in video_files]
                for future in futures:
                    result = future.result()
                    if result and progress_callback:
                        progress_callback(1)
        except Exception as e:
            print(f"Error converting files: {e}")