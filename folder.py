import os

# Root structure with file contents
structure = {
    "video-downloader/backend/app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.download import router as download_router

app = FastAPI(title="Terabox Downloader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(download_router, prefix="/api/download", tags=["Download"])

@app.get("/")
def root():
    return {"message": "Terabox Downloader API Running"}
""",

    "terabox-downloader/backend/app/config.py": """import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TERABOX_COOKIE = os.getenv("TERABOX_COOKIE")
    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")
    BASE_URL = "https://www.terabox.com"

settings = Settings()
""",

    "terabox-downloader/backend/app/downloader.py": """import requests
from .config import settings
from .utils import create_directory

def download_file(url: str) -> str:
    create_directory(settings.DOWNLOAD_DIR)

    filename = url.split("/")[-1]
    file_path = f"{settings.DOWNLOAD_DIR}/{filename}"

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return file_path
""",

    "terabox-downloader/backend/app/terabox.py": """import requests
from .config import settings

def fetch_direct_link(terabox_url: str) -> str:
    # Placeholder logic
    headers = {"Cookie": settings.TERABOX_COOKIE}
    response = requests.get(terabox_url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to fetch Terabox data")

    return "https://example.com/video.mp4"  # Replace with real logic
""",

    "terabox-downloader/backend/app/utils.py": """import os

def clean_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print("Cleanup error:", e)

def create_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
""",

    "terabox-downloader/backend/app/schemas.py": """from pydantic import BaseModel

class DownloadRequest(BaseModel):
    url: str

class DownloadResponse(BaseModel):
    status: str
    file_path: str | None = None
    message: str | None = None
""",

    "terabox-downloader/backend/app/routes/download.py": """from fastapi import APIRouter, HTTPException
from ..schemas import DownloadRequest, DownloadResponse
from ..terabox import fetch_direct_link
from ..downloader import download_file

router = APIRouter()

@router.post("/", response_model=DownloadResponse)
def download_video(req: DownloadRequest):

    try:
        direct_link = fetch_direct_link(req.url)
        file_path = download_file(direct_link)

        return DownloadResponse(
            status="success",
            file_path=file_path
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
""",

    "terabox-downloader/backend/requirements.txt": """fastapi
uvicorn
python-dotenv
requests
""",

    "terabox-downloader/backend/Dockerfile": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",

    "terabox-downloader/frontend/public/index.html": """<!DOCTYPE html>
<html>
  <head>
    <title>Terabox Downloader</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
""",

    "terabox-downloader/frontend/src/index.jsx": """import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
""",

    "terabox-downloader/frontend/src/App.jsx": """import React from "react";
import DownloadForm from "./components/DownloadForm";

export default function App() {
  return (
    <div style={{ padding: 40 }}>
      <h1>Terabox Video Downloader</h1>
      <DownloadForm />
    </div>
  );
}
""",

    "terabox-downloader/frontend/src/components/DownloadForm.jsx": """import React, { useState } from "react";
import { downloadVideo } from "../services/api";

export default function DownloadForm() {
  const [url, setUrl] = useState("");
  const [response, setResponse] = useState(null);

  const handleDownload = async () => {
    const res = await downloadVideo(url);
    setResponse(res);
  };

  return (
    <div>
      <input
        placeholder="Enter Terabox URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: "300px", padding: 10 }}
      />
      <button onClick={handleDownload} style={{ padding: 10, marginLeft: 10 }}>
        Download
      </button>

      {response && (
        <pre style={{ marginTop: 20 }}>
          {JSON.stringify(response, null, 2)}
        </pre>
      )}
    </div>
  );
}
""",

    "terabox-downloader/frontend/src/services/api.js": """export async function downloadVideo(url) {
  const res = await fetch("http://localhost:8000/api/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });

  return await res.json();
}
""",

    "terabox-downloader/frontend/package.json": """{
  "name": "terabox-downloader",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "scripts": {
    "start": "vite",
    "build": "vite build"
  }
}
""",

    "terabox-downloader/frontend/Dockerfile": """FROM node:20-alpine

WORKDIR /frontend
COPY . .

RUN npm install
RUN npm run build

EXPOSE 5173
CMD ["npm", "start"]
""",

    "terabox-downloader/docker-compose.yml": """version: "3.8"

services:
  backend:
    build: ./backend
    container_name: terabox-backend
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - ./backend/downloads:/app/downloads

  frontend:
    build: ./frontend
    container_name: terabox-frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
""",

    "terabox-downloader/.env": """TERABOX_COOKIE=your_cookie_here
DOWNLOAD_DIR=./downloads
""",

    "terabox-downloader/README.md": """# Terabox Video Downloader (FastAPI + React)

A web-based downloader for Terabox videos.
"""
}


# Create directories & files
for path, content in structure.items():
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Project structure created successfully!")
