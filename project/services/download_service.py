import os
import logging
from datetime import datetime
from pytubefix import YouTube, Playlist
from queue import Queue
from threading import Thread

class YoutubeConverter:
    def __init__(self, download_dir, conversion_type):
        self.download_dir = download_dir
        self.queue = Queue()
        self.threads = []
        self.active_downloads = 0
        self.conversion_type = conversion_type

        # Setup logging
        log_filename = datetime.now().strftime("LogConverter_%d-%m-%Y.log")
        logging.basicConfig(filename=log_filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("YoutubeConverter initialized with download_dir: %s and conversion_type: %s", download_dir, conversion_type)

    def set_conversion_type(self, conversion_type):
        self.conversion_type = conversion_type
        logging.info("Conversion type set to: %s", conversion_type)

    def validate_links(self, links):
        for link in links:
            if not ("youtu.be" in link) and not ("youtube.com/" in link):
                logging.error("Invalid link: %s", link)
                raise ValueError(f"Invalid link: {link}")
            logging.info("Validated link: %s", link)
            
    def is_playlist(self, link):
        is_playlist = "list=" in link
        logging.info("Checked if link is playlist: %s, result: %s", link, is_playlist)
        return is_playlist       
   

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
                    video = "youtu.be" + url[url.rfind("/"):]
                    unique_links.add(video)  # Add unique video URLs to the set
                    logging.info("Added video from playlist: %s", video)
            else:
                video = "youtu.be" + link[link.rfind("/"):]
                unique_links.add(video)  # Add unique video URLs for non-playlists
                logging.info("Added video link: %s", video)

        unique_video_links = list(unique_links)
        logging.info("Converted playlists to unique video links: %s", unique_video_links)
        return unique_video_links  # Convert the set back to a list

    def download_videos(self, video_urls, progress_callback=None):
        for url in video_urls:
            self.queue.put(url)
            self.active_downloads += 1
            logging.info("Added video to queue: %s", url)

        optimal_threads = max(4, os.cpu_count())
        for _ in range(min(4, optimal_threads)):  # Up to 4 threads
            thread = Thread(target=self._worker, args=(progress_callback,))
            thread.start()
            self.threads.append(thread)
            logging.info("Started download thread")

        for thread in self.threads:
            thread.join()
            logging.info("Joined download thread")           

    def _worker(self, progress_callback):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                self.download_video(url)
                logging.info("Downloaded video: %s", url)
                if progress_callback:
                    progress_callback(1)
            except Exception as e:
                logging.error("Error downloading video: %s, error: %s", url, str(e))
            finally:
                self.queue.task_done()
                self.active_downloads -= 1
                logging.info("Task done for video: %s", url)

    def download_video(self, video_url):
        try:
            yt = YouTube(video_url)
            logging.info("Initiated YouTube object for URL: %s", video_url)

            if self.conversion_type == 'MP3':
                stream = yt.streams.filter(only_audio=True, subtype="mp4").order_by("abr").last()
                logging.info("Filtered stream for MP3 conversion")
            elif self.conversion_type == 'MP4':
                stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").last()
                logging.info("Filtered stream for MP4 conversion")

            stream.download(self.download_dir)
            logging.info("Downloaded stream to directory: %s", self.download_dir)
        except Exception as e:
            logging.error("Error downloading video: %s, error: %s", video_url, str(e))            

    def get_downloaded_mp4s(self):
        downloaded_files = []
        for filename in os.listdir(self.download_dir):
            if filename.endswith(".mp4"):
                downloaded_files.append(os.path.join(self.download_dir, filename))
                logging.info("Found downloaded MP4: %s", filename)
        return downloaded_files
