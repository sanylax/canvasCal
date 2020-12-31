import rumps
import time
import main

def timez():
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())


@rumps.timer(45)
def a(sender):
    main.processAssignments()
    




if __name__ == "__main__":
    rumps.App(name = 'CanvasCal', icon = 'apple.png', menu=('CanvasCal',)).run()
