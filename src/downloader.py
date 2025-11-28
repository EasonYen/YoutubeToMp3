import yt_dlp
import os

class YoutubeDownloader:
    def __init__(self):
        pass

    def download_video_as_mp3(self, url, output_folder, quality='192', progress_hook=None, ffmpeg_path=None):
        """
        Downloads a YouTube video and converts it to MP3.
        
        Args:
            url (str): The YouTube video URL.
            output_folder (str): The folder to save the MP3.
            quality (str): The audio bitrate (e.g., '128', '192', '320').
            progress_hook (callable): A function to call with progress updates.
            ffmpeg_path (str): Path to the ffmpeg executable.
        """
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            # Critical settings to bypass YouTube restrictions
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android'],
                    'player_skip': ['configs', 'webpage'],
                    'skip': ['dash', 'hls'],
                }
            },
            # Add user agent to avoid detection
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            # Retry settings
            'retries': 10,
            'fragment_retries': 10,
            'skip_unavailable_fragments': True,
        }

        if ffmpeg_path:
            ydl_opts['ffmpeg_location'] = os.path.dirname(ffmpeg_path) if os.path.isfile(ffmpeg_path) else ffmpeg_path

        if progress_hook:
            ydl_opts['progress_hooks'] = [progress_hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True, "下載完成！"
        except Exception as e:
            return False, str(e)
