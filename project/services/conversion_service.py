import os
import subprocess
import static_ffmpeg
import concurrent.futures

static_ffmpeg.add_paths(weak=True)

class ConversionService:
    def __init__(self, max_workers=4):
        self.max_workers = max(max_workers, os.cpu_count())
    
    def _convert_mp4_to_mp3(self, file_paths):
        try:
            output_files = []
            for file_path in file_paths:
                output_file = os.path.splitext(file_path)[0] + ".mp3"
                output_files.append(output_file)
            
            # Process the files
            cmd = ["ffmpeg", "-threads", "0", "-y"]
            for file_path in file_paths:
                cmd.extend(["-i", file_path])
                
            cmd.extend(["-vn", "-map", "a"])
            cmd.extend(output_files)
            
            subprocess.run(cmd, shell=True, check=True)
            for file_path in file_paths:
                os.remove(file_path)
                
            return output_files
        except subprocess.CalledProcessError as e:
            print(f"Error converting files: {e}")
            return None
        except Exception as e:
            print(f"Error converting {file_path} to MP3: {e}")
            return None

    def convert_mp4_to_mp3(self, video_files, progress_callback=None):
        try:
            chunk_size = (len(video_files) + self.max_workers - 1) // self.max_workers
            chunks = [video_files[i:i + chunk_size] for i in range(0, len(video_files), chunk_size)]
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self._convert_mp4_to_mp3, chunk) for chunk in chunks]
                  
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result and progress_callback:
                        progress_callback(len(result))
        except Exception as e:
            print(f"Error converting files: {e}")
