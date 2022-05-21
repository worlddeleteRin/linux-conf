#!/usr/bin/python
import os
import subprocess

home = os.environ.get('HOME')

sway_install_packages = "sway waybar alacritty wl-clipboard dunst bemenu"

def install_sway():
    subprocess.run(
        f"sudo pacman -S {sway_install_packages}",
        shell=True
    )

def config_sway():
    subprocess.run(
        f"mkdir -p {home}/.config/sway",
        shell=True
    )
    subprocess.run(
        f"cp sway/config {home}/.config/sway/",
        shell=True
    )

def config_waybar():
    subprocess.run(
        f"cp -r sway/waybar {home}/.config/",
        shell=True
    )

def config_alacritty():
    subprocess.run(
        f"mkdir -p {home}/.config/alacritty",
        shell=True
    )
    subprocess.run(
        f"cp sway/alacritty.yml {home}/.config/alacritty/", shell=True)

def main():
    install_sway()
    config_sway()
    config_waybar()
    config_alacritty()
    pass

if __name__ == '__main__':
    main()
