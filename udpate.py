import requests
from datetime import datetime, timedelta
import os
from pathlib import Path

from lib import basepath, get_scene

# Update the wallpaper based on the specified scene and time of day

def get_api_key():
    filename = basepath / ".api_key"
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            theme = file.read().strip()
        return theme
    else:
        raise ValueError(f"Filename {filename} not found")

def get_sunset_times():
    # Send request to ipgeolocation
    baseurl = "https://api.ipgeolocation.io/astronomy"
    apikey = get_api_key()
    params = {"apiKey": apikey}
    response = requests.get(baseurl, params=params)
    data = response.json()
    # Parse sunrise and sunset times for today
    now = datetime.now()
    sunrise = datetime.strptime(data["sunrise"], "%H:%M")
    sunrise = now.replace(
        hour=sunrise.hour,
        minute=sunrise.minute,
        second=0,
        microsecond=0
    )
    sunset = datetime.strptime(data["sunset"], "%H:%M")
    sunset = now.replace(
        hour=sunset.hour,
        minute=sunset.minute,
        second=0,
        microsecond=0
    )
    return sunrise, sunset

def update_wallpaper(scene, timeofday):
    scene_day = scene + "-" + timeofday
    filename = scene_day + ".png"
    wallpaper_path = basepath / scene / scene_day / filename
    command = " ".join([
        "/usr/bin/gsettings",
        "set", "org.gnome.desktop.background",
        "picture-uri", f"file://{wallpaper_path}"
    ])
    os.system(command)

if __name__ == "__main__":

    scene = get_scene()

    sunrise, sunset = get_sunset_times()
    delta = timedelta(minutes=30)
    now = datetime.now()
    is_night = now < sunrise - delta or now > sunset + delta
    is_day = now > sunrise + delta and now < sunset - delta
    if is_night:
        timeofday = 'night'
    elif is_day:
        timeofday = 'day'
    else:
        timeofday = 'sunset'

    print(f"Updating wallpaper with {scene}-{timeofday}")
    update_wallpaper(scene, timeofday)