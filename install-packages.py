#!/usr/bin/python
import subprocess

packages = [
    "git", "wl-clipboard", "chromium",
    "alacritty", "sway", "openssh",
    "neovim", "nodejs", "vlc",
    "imv", "grim", "waybar",
    "wofi", "pyenv"
]

def install():
    global packages
    pkg_str = ' '.join(packages)
    subprocess.run(
        f'yes | sudo pacman -S {pkg_str}',
        shell=True
    )

if __name__ == '__main__':
    install()
