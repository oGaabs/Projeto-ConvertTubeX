import os
import subprocess
import static_ffmpeg
import concurrent.futures

static_ffmpeg.add_paths(weak=True)

overwrite_output = "-y"
input_file = "-i"
include_only_audio_streams = "-map 0:a"
variable_bit_rate = "-q:a 0"

class ConversionService:
    def __init__(self, max_workers=4):
        self.max_workers = max(max_workers, os.cpu_count())
        
    def build_ffmpeg_command(self, input_filename, output_filename):
        command = [
            "ffmpeg",
            overwrite_output,
            input_file, input_filename, 
            include_only_audio_streams,
            variable_bit_rate,
            output_filename
        ]
        return command

    def _convert_mp4_to_mp3(self, input_path):
        try:
            output_path = os.path.splitext(input_path)[0] + ".mp3"
            ffmpeg_command = self.build_ffmpeg_command(input_path, output_path)

            subprocess.run(ffmpeg_command, shell=True, check=True)
            
            if os.path.exists(output_path):
                os.remove(input_path)
            else:
                print(f"Output file not created for {input_path}.")
                return None
            
            return output_path
        except Exception as e:
            print(f"Error converting {input_path} to MP3: {e}")
            return None

    def convert_mp4_to_mp3(self, video_files, progress_callback=None):
        try:
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self._convert_mp4_to_mp3, file_path) for file_path in video_files]
                results = []
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
                    if progress_callback:
                        progress_callback(1)
                return results
        except Exception as e:
            print(f"Error converting files: {e}")