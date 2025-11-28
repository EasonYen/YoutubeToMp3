#!/usr/bin/env python3
import yt_dlp
import os

# Test download with user's requested video
url = "https://www.youtube.com/watch?v=HegSBovl24I"  # LBI - Jumping Machine
output_folder = os.path.expanduser("~/Downloads")

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    'ffmpeg_location': '/usr/local/bin',
    'extractor_args': {
        'youtube': {
            'player_client': ['ios', 'android'],
            'player_skip': ['configs', 'webpage'],
            'skip': ['dash', 'hls'],
        }
    },
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    },
    'retries': 10,
    'fragment_retries': 10,
    'skip_unavailable_fragments': True,
}

print(f"Testing download to: {output_folder}")
print(f"URL: {url}")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"Video title: {info['title']}")
        print("Starting download...")
        ydl.download([url])
    print("Download completed successfully!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
