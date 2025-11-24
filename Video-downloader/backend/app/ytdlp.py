import yt_dlp
import os
from .config import TEMP_DIR

class PublicVideoError(Exception):
    """Custom exception for public video download errors."""
    pass

# Path to bundled ffmpeg
FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg.exe")

def download_public_video(url: str, format: str = "mp4") -> str:
    """
    Download a public video using yt-dlp and return local file path.
    format: "mp4" or "mp3"
    """
    if format == "mp3":
        ydl_opts = {
            'outtmpl': os.path.join(TEMP_DIR, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:  # mp4 video
        ydl_opts = {
            'outtmpl': os.path.join(TEMP_DIR, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format == "mp3":
                filename = os.path.splitext(filename)[0] + ".mp3"
            return filename
    except yt_dlp.utils.DownloadError as e:
        raise PublicVideoError(f"Public video download failed: {e}")
    except Exception as e:
        raise PublicVideoError(str(e))
