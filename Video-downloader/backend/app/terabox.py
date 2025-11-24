import requests
import os
from .config import TERABOX_BDUSS, TERABOX_STOKEN, TEMP_DIR

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

COOKIES = {
    "BDUSS": TERABOX_BDUSS,
    "STOKEN": TERABOX_STOKEN
}

class TeraboxError(Exception):
    """Custom exception for Terabox-related errors."""
    pass

def download_terabox_file(share_url: str) -> str:
    """
    Download a file from Terabox using your account cookies.
    Raises TeraboxError for any failure.
    """
    try:
        share_id = share_url.rstrip("/").split("/")[-1]

        # Step 1: Get file list / metadata
        list_api = f"https://pan.terabox.com/rest/2.0/xpan/share?method=filelist&shareid={share_id}&dir=/"
        resp = requests.get(list_api, cookies=COOKIES, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()

        if "errno" in data and data["errno"] == -6:
            raise TeraboxError("Invalid or expired Terabox cookies. Please renew BDUSS/STOKEN.")

        if "list" not in data or not data["list"]:
            raise TeraboxError("No files found or invalid Terabox link.")

        file_info = data["list"][0]
        filename = file_info["server_filename"]
        file_id = file_info["fs_id"]

        # Step 2: Get download link
        download_api = f"https://pan.terabox.com/rest/2.0/xpan/share?method=download&fs_id={file_id}&shareid={share_id}"
        dl_resp = requests.get(download_api, cookies=COOKIES, headers=HEADERS)
        dl_resp.raise_for_status()
        dl_data = dl_resp.json()

        if "dlink" not in dl_data:
            raise TeraboxError("Failed to retrieve download link. Cookies might be expired.")

        download_url = dl_data["dlink"]

        # Step 3: Download file temporarily
        local_path = os.path.join(TEMP_DIR, filename)
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return local_path

    except requests.exceptions.RequestException as e:
        raise TeraboxError(f"Network error: {e}")
    except Exception as e:
        raise TeraboxError(str(e))
