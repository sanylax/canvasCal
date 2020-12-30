import pystray
from pystray import Menu, MenuItem

from PIL import Image

import main

from threading import Event

image = Image.open("apple.png")

exitEvent = Event()

from plyer import notification
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
        main.processAssignments(failed)
        print("Updated calendar...")
        exitEvent.wait(60 * 60 * 6)

icon = pystray.Icon('test name', image)
icon.title = 'CanvasCal'
icon.menu = Menu(
    MenuItem('CanvasCal', None, enabled=False),
    MenuItem('Exit', lambda: exitAction(icon))
)
icon.run(callback)