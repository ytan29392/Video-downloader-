import os

def clean_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print("Cleanup error:", e)

def create_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)