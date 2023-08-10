#! /bin/bash

systemctl --user enable --now sunwall-update.timer
systemctl --user enable --now sunwall-randomize.timer
