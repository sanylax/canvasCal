import os
import rumps
import main


@rumps.timer(45)
def refresh(sender):
    main.processAssignments()
    
if __name__ == "__main__":
    filepath = os.path.join(os.getenv("HOME"), '.canvasCal')
    rumps.App(name = 'CanvasCal', icon = os.path.join(filepath, 'apple.png'), menu=('CanvasCal',)).run()
