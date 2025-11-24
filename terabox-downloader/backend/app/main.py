from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routes.download import router as download_router
from .config import TEMP_DIR

app = FastAPI(title="Terabox Downloader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve temporary files for download
app.mount("/files", StaticFiles(directory=TEMP_DIR), name="files")
app.include_router(download_router, prefix="/api/download", tags=["Download"])

@app.get("/")
def root():
    return {"message": "Terabox Downloader API Running"}

