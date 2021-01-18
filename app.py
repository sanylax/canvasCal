import pystray
from pystray import Menu, MenuItem

from PIL import Image

import main

from threading import Event

image = Image.open("apple.png")

exitEvent = Event()

from plyer import notification
from os.path import expanduser
import os
home = expanduser("~")
global filepath
filepath = os.path.join(home, '.canvasCal')

def failed():
    notification.notify(
        title='CanvasCal failed to run',
        message='Please run setup.exe',
        app_name='CanvasCal',
        #app_icon='path/to/the/icon.' + ('ico' if platform == 'win' else 'png')
    )

def exitAction(icon):
    icon.visible = False
    exitEvent.set()
    icon.stop()

def callback(icon):
    icon.visible = True
    while icon.visible and not exitEvent.is_set():
        file = open(os.path.join(main.filepath, 'index.txt'), 'r')
        numSchools = int(file.readline().strip())
        print(numSchools)
        for _ in range(numSchools):
            URL = file.readline().strip()
            KEY = file.readline().strip()
            code = main.processAssignments(URL, KEY)
            if code != 0:
                #rumps.notification("CanvasCal", subtitle = 'Error', message =code)
                print(code)
        icon.visible = True
        exitEvent.wait(60 * 60 * 6)
        print("Updated calendar...")



    


icon = pystray.Icon('test name', image)
icon.title = 'CanvasCal'
icon.menu = Menu(
    MenuItem('CanvasCal', None, enabled=False),
    MenuItem('Exit', lambda: exitAction(icon))
)
icon.run(callback)