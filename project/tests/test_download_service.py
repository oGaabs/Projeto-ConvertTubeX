import unittest
import os
import shutil
import sys

# Local application imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../services')))
from download_service import YoutubeConverter

class TestYoutubeConverterEndToEnd(unittest.TestCase):

    def setUp(self):
        self.download_dir = os.path.join(os.getcwd(), 'test_downloadedFiles')
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
        os.makedirs(self.download_dir)
        self.converter = YoutubeConverter(self.download_dir, 'MP3')

    def tearDown(self):
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)

    def test_end_to_end_download_single_video(self):
        urls = ["https://www.youtube.com/watch?v=4KCVbn3SIak"]
        self.converter.validate_links(urls)
        unique_video_urls = self.converter.convert_playlists_to_link(urls)
        self.converter.download_videos(unique_video_urls)

        downloaded_files = self.converter.get_downloaded_mp4s()
        self.assertEqual(len(downloaded_files), 1)
        self.assertTrue(downloaded_files[0].endswith(".mp4"))

    def test_end_to_end_download_playlist(self):
        urls = [            
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL9tY0BWXOZFvxqMV_kZboiIMnKsYzH5al",
            "https://www.youtube.com/watch?v=p2AWYanIHkc"
        ]
        self.converter.validate_links(urls)
        unique_video_urls = self.converter.convert_playlists_to_link(urls)
        self.converter.download_videos(unique_video_urls)

        downloaded_files = self.converter.get_downloaded_mp4s()
        self.assertEqual(len(downloaded_files), 11)
        for file in downloaded_files:
            self.assertTrue(file.endswith(".mp4"))
            self.assertTrue(os.path.exists(file))

if __name__ == '__main__':
    unittest.main()