from fastapi import APIRouter, HTTPException, Query
from app.downloader import download_file
from app.terabox import TeraboxError
from app.ytdlp import PublicVideoError

# router = APIRouter(prefix="/download", tags=["Download"])
router = APIRouter(tags=["Download"])

@router.get("/")
def download_endpoint(
    url: str = Query(..., description="Terabox or public video link"),
    format: str = Query("mp4", description="mp4 or mp3")
):
    try:
        file_path = download_file(url, format)
        return {"message": "Download complete", "file_path": file_path}
    except (TeraboxError, PublicVideoError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")