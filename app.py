import rumps
import time
import main
import os
from os import path
#import Foundation
#from Foundation import NSAutoreleasePool

def timez():
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())


@rumps.timer(45)
def a(sender):
    main.processAssignments()
    




if __name__ == "__main__":
    filepath = os.path.join(os.getenv("HOME"), '.canvasCal')
    #file = open('bruh.xyz', 'w')
    #file.close()
    rumps.App(name = 'CanvasCal', icon = os.path.join(filepath, 'apple.png'), menu=('CanvasCal',)).run()
