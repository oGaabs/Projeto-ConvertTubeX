import os
import logging
import re
import shutil
from datetime import datetime
from yt_dlp import YoutubeDL
from pytubefix import YouTube, Playlist
from concurrent.futures import ProcessPoolExecutor

class YoutubeConverter:
    DEBUG_MODE = False
    
    def __init__(self, download_dir, conversion_type):
        self.download_dir = download_dir
        self.conversion_type = conversion_type

        # Setup logging
        log_filename = datetime.now().strftime("LogConverter_%d-%m-%Y.txt")
        logging.basicConfig(filename=log_filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("YoutubeConverter initialized with download_dir: %s and conversion_type: %s", download_dir, conversion_type)

    def set_conversion_type(self, conversion_type):
        self.conversion_type = conversion_type
        logging.info("Conversion type set to: %s", conversion_type)

    def validate_links(self, links):
        for link in links:
            if "youtu.be" not in link and "youtube.com/" not in link and not link.startswith("http"):
                logging.error("Invalid link: %s", link)
                raise ValueError(f"Invalid link: {link}")
            logging.info("Validated link: %s", link)

            
    def is_playlist(self, link):
        is_playlist = "list=" in link
        logging.info("Checked if link is playlist: %s, result: %s", link, is_playlist)
        return is_playlist       

    def is_ytvideo(self, link):
        is_video = link.startswith("https://www.youtube.com/watch?v=")
        logging.info("Checked if link is playlist: %s, result: %s", link, is_video)
        return is_video 

    def convert_playlists_to_link(self, links):
        """Converts playlist URLs to video URLs and removes duplicates.

        Args:
            links: A list of playlist or video URLs.

        Returns:
            A new list containing unique video URLs.
        """
        unique_links = set()  # Create a set to efficiently store unique elements
        for link in links:
            if self.is_playlist(link):
                video = "youtube.com" + link[link.rfind("/"):]
                playlist = Playlist(video)
                for url in playlist.video_urls:
                    video = "https://youtube.com" + url[url.rfind("/"):]
                    unique_links.add(video)  # Add unique video URLs to the set
                    logging.info("Added video from playlist: %s", video)
            elif self.is_ytvideo(link):
                video = "https://youtube.com" + link[link.rfind("/"):]
                unique_links.add(video)  # Add unique video URLs for non-playlists
                logging.info("Added video link: %s", video)

        unique_video_links = list(unique_links)
        logging.info("Converted playlists to unique video links: %s", unique_video_links)
        return unique_video_links  # Convert the set back to a list

    def download_task(self, videos, output_dir):
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            
        try:
            yt = YouTube(videos)
            logging.info("Initiated YouTube object for URL: %s", videos)
            if self.conversion_type == 'MP3':
                stream = yt.streams.filter(only_audio=True, subtype="mp4").order_by("abr").last()
            else:  # Assume MP4
                stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").last()
            stream.download(self.download_dir)
            logging.info("Downloaded video via pytubefix: %s", videos)
        except Exception as e:
            logging.error("Error with pytubefix, falling back to yt_dlp for URL: %s", videos)
            
            self.alternative_download_video(videos)
                
    def alternative_download_video(self, video_url):
        ydl_opts = {
            'outtmpl':  os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'format': 'bestaudio[ext=mp4]/mp4' if self.conversion_type == 'MP3' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'concurrent_fragment_downloads': True,  # Enable multi-threaded fragment downloads
            'concurrent_fragments': 4,  # Number of threads used for fragment downloads
            'restrictfilenames': True,  # Restrict filenames to only ASCII characters, and avoid "&" and spaces
            'retries': 3,
        }
        if self.DEBUG_MODE:
            ydl_opts['verbose'] = True
            ydl_opts['debug_printtraffic'] = True
            ydl_opts['logger'] = logging.getLogger()

        logging.info("Configured yt_dlp options for %s conversion", self.conversion_type)

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            logging.info("Downloaded video via yt_dlp: %s", video_url)
        except Exception as e:
            logging.error("Error downloading with yt_dlp for URL: %s, error: %s", video_url, str(e))

    def download_videos(self, video_urls, progress_callback=None):
        with ProcessPoolExecutor() as executor:
            futures = []

            for video_url in video_urls:
                playlist_output_dir = f"{self.download_dir}"
                futures.append(executor.submit(self.download_task, video_url, playlist_output_dir))
            
            # Wait for all the downloads to complete
            for future in futures:
                future.result()
                if progress_callback:
                    progress_callback(1)

    def get_downloaded_mp4s(self):
        downloaded_files = []
        for filename in os.listdir(self.download_dir):
            if filename.endswith(".mp4"):
                downloaded_files.append(os.path.join(self.download_dir, filename))
                logging.info("Found downloaded MP4: %s", filename)
        return downloaded_files

def main():
    download_dir = os.path.join(os.getcwd(), 'downloadedFiles')
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)

    converter = YoutubeConverter(download_dir, 'MP3')
    urls = [
        "https://www.youtube.com/watch?v=4KCVbn3SIak",
    ]

    try:
        converter.validate_links(urls)
        unique_video_urls = converter.convert_playlists_to_link(urls)
        converter.download_videos(unique_video_urls)
        downloaded_files = converter.get_downloaded_mp4s()
        logging.info("Downloaded files: %s", downloaded_files)
    except Exception as e:
        logging.error("Error: %s", str(e))

if __name__ == "__main__":
    main()