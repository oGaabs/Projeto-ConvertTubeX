import os

from pytube import YouTube, Playlist
from queue import Queue
from threading import Thread

class YoutubeConverter:
    def __init__(self, download_dir, conversion_type):
        self.download_dir = download_dir
        self.queue = Queue()
        self.threads = []
        self.active_downloads = 0
        self.conversion_type = conversion_type

    def set_conversion_type(self, conversion_type):
        self.conversion_type = conversion_type

    def validate_links(self, links):
        for link in links:
            if not ("youtu.be" in link) and not ("youtube.com/" in link):
                raise ValueError(f"Invalid link: {link}")
            
    def is_playlist(self, link):
        if link.find("list=") == -1:
            return False
        return True       

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
            else:
                video = "youtu.be" + link[link.rfind("/"):]
                unique_links.add(video)  # Add unique video URLs for non-playlists

        return list(unique_links)  # Convert the set back to a list

    def download_videos(self, video_urls, progress_callback=None):
        for url in video_urls:
            self.queue.put(url)
            self.active_downloads += 1

        optimal_threads = max(4, os.cpu_count())
        for _ in range(min(4, optimal_threads)):  # Up to 4 threads
            thread = Thread(target=self._worker, args=(progress_callback,))
            thread.start()
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()            

    def _worker(self, progress_callback):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                self.download_video(url)
                if progress_callback:
                    progress_callback(1)
            finally:
                self.queue.task_done()
                self.active_downloads -= 1

    def download_video(self, video_url):
        yt = YouTube(video_url)

        if self.conversion_type == 'MP3':
            stream = (yt.streams.filter(only_audio=True, subtype="mp4").order_by("abr").last())
        elif self.conversion_type == 'MP4':
            stream = (yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").last())

        stream.download(self.download_dir)
            

    def get_downloaded_mp4s(self):
        downloaded_files = []
        for filename in os.listdir(self.download_dir):
            if filename.endswith(".mp4"):
                downloaded_files.append(os.path.join(self.download_dir, filename))
        return downloaded_files
