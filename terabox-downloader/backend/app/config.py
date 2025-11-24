import os
from dotenv import load_dotenv

# Specify the full path to your .env
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(dotenv_path)

TERABOX_BDUSS = os.getenv("TERABOX_BDUSS")
TERABOX_STOKEN = os.getenv("TERABOX_STOKEN")
TEMP_DIR = os.getenv("TEMP_DIR", "./backend/temp")

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
