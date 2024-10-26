import os
import logging
from datetime import datetime
import shutil
from yt_dlp import YoutubeDL
from pytubefix import YouTube, Playlist
import asyncio

class YoutubeConverter:
    def __init__(self, download_dir, conversion_type):
        self.download_dir = download_dir
        self.conversion_type = conversion_type
        os.makedirs(self.download_dir, exist_ok=True)

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
            if not ("youtu.be" in link) and not ("youtube.com/" in link) and not link.startswith("http"):
                logging.error("Invalid link: %s", link)
                raise ValueError(f"Invalid link: {link}")
            logging.info("Validated link: %s", link)

    def is_playlist(self, link):
        return "list=" in link

    def is_ytvideo(self, link):
        return link.startswith("https://www.youtube.com/watch?v=")

    def convert_playlists_to_link(self, links):
        unique_links = set()
        for link in links:
            if self.is_playlist(link):
                playlist = Playlist(link)
                for url in playlist.video_urls:
                    unique_links.add(url)
                    logging.info("Added video from playlist: %s", url)
            elif self.is_ytvideo(link):
                unique_links.add(link)
                logging.info("Added video link: %s", link)
        return list(unique_links)

    def download_videos(self, video_urls, progress_callback=None):
        # Wrap the async call within `asyncio.run()` to execute it in this synchronous context.
        asyncio.run(self._download_videos_async(video_urls, progress_callback))

    async def _download_videos_async(self, video_urls, progress_callback=None):
        tasks = [self.download_video_yt(url, progress_callback) for url in video_urls]
        await asyncio.gather(*tasks)
        
    async def download_video_yt(self, url, progress_callback=None):
        try:
            yt = YouTube(url)
            logging.info("Initiated YouTube object for URL: %s", url)
            if self.conversion_type == 'MP3':
                stream = yt.streams.filter(only_audio=True, subtype="mp4").order_by("abr").last()
            else:  # Assume MP4
                stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").last()
            stream.download(self.download_dir)
            logging.info("Downloaded video via pytubefix: %s", url)
            if progress_callback:
                progress_callback(1)
        except Exception as e:
            logging.error("Error with pytubefix, falling back to yt_dlp for URL: %s", url)
            await self.alternative_download_video(url, progress_callback)

    async def alternative_download_video(self, url, progress_callback=None):
        """Download video using yt_dlp without async context manager."""
        ydl_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4'
        }
        if self.conversion_type == 'MP3':
            ydl_opts['format'] = 'bestaudio[ext=mp4]/mp4'
        else:
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'

        try:
            # Run yt_dlp in a separate thread
            await asyncio.to_thread(self.run_yt_dlp_download, ydl_opts, url)
            logging.info("Downloaded video via yt_dlp: %s", url)
            if progress_callback:
                progress_callback(1)
        except Exception as e:
            logging.error("Error downloading with yt_dlp for URL: %s, error: %s", url, str(e))

    def run_yt_dlp_download(self, ydl_opts, url):
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    async def download_videos_yt(self, video_urls, progress_callback=None):
        tasks = [self.download_video_yt(url, progress_callback) for url in video_urls]
        await asyncio.gather(*tasks)

    def get_downloaded_mp4s(self):
        return [os.path.join(self.download_dir, f) for f in os.listdir(self.download_dir) if f.endswith(".mp4")]

async def main():
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
        await converter.download_videos_yt(unique_video_urls, progress_callback=None)
        downloaded_files = converter.get_downloaded_mp4s()
        logging.info("Downloaded files: %s", downloaded_files)
    except Exception as e:
        logging.error("Error: %s", str(e))

if __name__ == "__main__":
    asyncio.run(main())
