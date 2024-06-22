import os
import subprocess
import static_ffmpeg
import concurrent.futures

static_ffmpeg.add_paths(weak=True)

class ConversionService:
    def __init__(self, max_workers=4):
        self.max_workers = max(max_workers, os.cpu_count())
    
    def _convert_mp4_to_mp3(self, file_path):
        try:
            output_file = os.path.splitext(file_path)[0] + ".mp3"
            subprocess.run(["ffmpeg", "-y", "-i",  file_path, "-vn", "-map", "a", output_file], shell=True)
            os.remove(file_path)
            return output_file
        except Exception as e:
            print(f"Error converting {file_path} to MP3: {e}")
            return None

    def convert_mp4_to_mp3(self, video_files, progress_callback=None):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self._convert_mp4_to_mp3, file_path) for file_path in video_files]
                for future in futures:
                    result = future.result()
                    if result and progress_callback:
                        progress_callback(1)
        except Exception as e:
            print(f"Error converting files: {e}")
