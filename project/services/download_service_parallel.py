import os
from concurrent.futures import ProcessPoolExecutor
from yt_dlp import YoutubeDL

from pytubefix import YouTube, Playlist

def download_task(videos, output_dir):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'outtmpl': os.path.join("D:\\Programming\\Projeto-ConvertTubeX\\downloadedFiles", '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4'
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([videos])

if __name__ == "__main__":
    output_dir = "./root_dir"
    many_playlists = ["https://www.youtube.com/playlist?list=PL3ziPXJ03rileiamE0jomFTcGMqdwweek"]

    def convert_playlists_to_link(links):
        unique_links = set()
        for link in links:
            if "playlist" in link:
                playlist = Playlist(link)
                for url in playlist.video_urls:
                    unique_links.add(url)
                    print("Added video from playlist: %s", url)
            elif "watch" in link:
                unique_links.add(link)
        return list(unique_links)

    with ProcessPoolExecutor() as executor:
        futures = []
        video_urls = convert_playlists_to_link(many_playlists)
        
        for video_url in video_urls:
            playlist_output_dir = f"{output_dir}/playlist_videos"
            futures.append(executor.submit(download_task, video_url, playlist_output_dir))
        
        # Wait for all the downloads to complete
        for future in futures:
            future.result()
