from app.terabox import download_terabox_file, TeraboxError
from app.ytdlp import download_public_video, PublicVideoError

def download_file(url: str, format: str = "mp4") -> str:
    """
    Detect link type and download accordingly:
    - Terabox links → use cookies
    - Public video links → use yt-dlp
    Returns path to downloaded file.
    """
    try:
        if "terabox.com" in url.lower():
            # Terabox download
            return download_terabox_file(url)
        else:
            # Public video download
            return download_public_video(url)
    except (TeraboxError, PublicVideoError) as e:
        # Known errors
        raise e
    except Exception as e:
        raise Exception(f"Download failed: {e}")
