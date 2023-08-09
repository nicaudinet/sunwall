from pathlib import Path
import os

basepath = Path("/home/niki/Wallpapers")

def get_scene():
    filename = basepath / ".scene"
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            theme = file.read().strip()
        return theme
    else:
        raise ValueError(f"Filename {filename} not found")