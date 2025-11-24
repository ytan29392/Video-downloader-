from pydantic import BaseModel

class DownloadRequest(BaseModel):
    url: str

class DownloadResponse(BaseModel):
    status: str
    file_path: str | None = None
    message: str | None = None
