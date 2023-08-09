from pathlib import Path
import os
import random

from lib import basepath, get_scene

# Choose a different random scene from the ones available at basepath

if __name__ == "__main__":
    scenes = [f for f in os.listdir(basepath) if not f.startswith('.')]
    try: scenes.remove(get_scene())
    except ValueError: pass
    scene = random.choice(scenes)
    with open(basepath / ".scene", "w") as file:
        file.write(scene)