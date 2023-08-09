Two small scripts to have a more interactive wallpaper:
 - `update.py` - Update the wallpaper based on the time of day and the scene
 - `randomize.py` - Randomize the scene based on available scenes

Beautiful scenic and minimalistic wallpapers from Pixel True [here](https://www.pixeltrue.com/scenic-illustrations).

Scenes are saved in `~/Wallpapers`. They require the following directory struture:
```
SCENE_NAME
    SCENE_NAME-day
        SCENE_NAME-day.png
    SCENE_NAME-night
        SCENE_NAME-night.png
    SCENE_NAME-sunset
        SCENE_NAME-sunset.png
```
This which follows the structure of (some) of the wallpapers downloaded from Pixel True.

The `~/Wallpapers` directory also contains:
 - `.api_key` - the API key for ipgeolocation.io, the service used for sunrise and sunset times
 - `.scene` - the current scene

To run the scripts automatically, one can set up a simple systemd service and timer. For example, for the update script:

*sunwell-update.service*
```
[Unit]
Description=Randomize wallpaper

[Service]
Type=oneshot
ExecStart=/bin/python /home/niki/Projects/sunwall/randomize.py
```

*sunwell-update.timer*
```
[Unit]
Description=Wallpaper randomize timer

[Timer]
OnCalendar=*-*-* 0:00:00
OnBootSec=10s

[Install]
WantedBy=timers.target
```

Put the services in `/etc/systemd/system/` (you will need sudo rights). Then:

```
sudo systemd daemon-reload
sudo systemd enable --now sunwall-update.timer
```