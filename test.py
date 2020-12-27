import pystray
from pystray import Menu, MenuItem

import time
from PIL import Image

import main

image = Image.open("apple.png")

def exit(icon):
    icon.visible = False
    icon.stop()

def callback(icon):
    icon.visible = True
    while icon.visible:
        main()
        print("Updated calendar...")
        time.sleep(60 * 60 * 6)

icon = pystray.Icon('test name', image)
icon.menu = Menu(
    MenuItem('Exit', lambda: exit(icon))
)
icon.run(callback)