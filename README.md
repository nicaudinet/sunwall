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

To run the scripts automatically, one can set up a simple systemd service and timer in userland. [This blog post](https://ihaveabackup.net/2016/03/14/wallpaper-changer-with-systemd/) is what I followed to get this to work. For example, for the update script:

**sunwell-update.service**
```
[Unit]
Description=Randomize wallpaper

[Service]
Type=oneshot
ExecStart=/bin/python /home/niki/Projects/sunwall/randomize.py
Environment=DISPLAY=:0.0
```

**sunwell-update.timer**
```
[Unit]
Description=Wallpaper randomize timer

[Timer]
OnCalendar=*-*-* 0:00:00
OnBootSec=10s

[Install]
WantedBy=X.target
```

**X.target**
```
[Unit]
Description=Xorg server start
```

Put all three files in services in `~/.config/systemd/user/` (create it if you need to).

`X.target` is an empty unit which represents the start of the X11 server. We need to start it manually by adding the following:

**~/.xinitrc**
```
systemctl --user start X.target
```

Then, we can enable the timer so that it starts every time the X target is started:

```
systemctl --user enable sunwall-update.timer
```

And with that we're done! If you want to check whether things are going to plan, you can check `systemctl --user` or `journalctl --user -u sunwall-update`. If you want to manually change the wallpaper, just run `systemctl --user start sunwall-update.service`.
