import sys
import unittest
import os
import shutil
import subprocess
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../services')))
from conversion_service import ConversionService

class TestConversionServiceEndToEnd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_audio_dir = os.path.join(os.getcwd(), 'test_audio_files')
        cls.output_dir = os.path.join(os.getcwd(), 'test_output_files')
        if not os.path.exists(cls.test_audio_dir):
            os.makedirs(cls.test_audio_dir)
        if not os.path.exists(cls.output_dir):
            os.makedirs(cls.output_dir)
        cls.sample_audio_urls = [
            "https://download.samplelib.com/mp4/sample-5s.mp4",
            "https://download.samplelib.com/mp4/sample-30s.mp4",
            "https://download.samplelib.com/mp4/sample-20s.mp4",  # Duplicate
            "https://download.samplelib.com/mp4/sample-5s.mp4",
        ]
        cls.sample_audio_paths = [
            os.path.join(cls.test_audio_dir, 'sample_audio_1.mp3'),
            os.path.join(cls.test_audio_dir, 'sample_audio_2.mp3'),
            os.path.join(cls.test_audio_dir, 'sample_audio_3.mp3'),
            os.path.join(cls.test_audio_dir, 'sample_audio_4.mp3')
        ]
        for url, path in zip(cls.sample_audio_urls, cls.sample_audio_paths):
            cls.download_sample_audio(url, path)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_audio_dir):
            shutil.rmtree(cls.test_audio_dir)
        if os.path.exists(cls.output_dir):
            shutil.rmtree(cls.output_dir)

    @staticmethod
    def download_sample_audio(url, output_path):
        response = requests.get(url)
        with open(output_path, 'wb') as file:
            file.write(response.content)

    def setUp(self):
        self.converter = ConversionService()

    def test_build_ffmpeg_command(self):
        input_filename = self.sample_audio_paths[0]
        output_filename = os.path.join(self.output_dir, 'output_audio.mp3')
        command = self.converter.build_ffmpeg_command(input_filename, output_filename)
        expected_command = [
            self.converter.ffmpeg_path,
            '-hide_banner', '-loglevel', 'error',
            '-y',
            '-i', input_filename,
            '-map', '0:a',
            '-q:a', '0',
            output_filename
        ]
        self.assertEqual(command, expected_command)

    def test_audio_conversion(self):
        input_filename = self.sample_audio_paths[0]
        output_filename = os.path.join(self.output_dir, 'output_audio.mp3')
        command = self.converter.build_ffmpeg_command(input_filename, output_filename)
        subprocess.run(command, check=True)
        self.assertTrue(os.path.exists(output_filename))
        self.assertGreater(os.path.getsize(output_filename), 0)

    def test_multiple_audio_conversion(self):
        output_files = []
        self.converter.convert_mp4_to_mp3(self.sample_audio_paths, progress_callback=output_files.append, output_dir=self.output_dir)
        self.assertEqual(len(output_files), len(self.sample_audio_paths))
        
        for index, output in enumerate(output_files, start=1):
            if output:
                output_filename = os.path.join(self.output_dir, f'sample_audio_{index}.mp3')
                self.assertTrue(os.path.exists(output_filename))
                self.assertGreater(os.path.getsize(output_filename), 0)

if __name__ == '__main__':
    unittest.main()