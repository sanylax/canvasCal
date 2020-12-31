import rumps
import main

@rumps.timer(45)
def refresh(sender):
    main.processAssignments()

if __name__ == "__main__":
    rumps.App(name = 'CanvasCal', icon ='icon.png', menu=('CanvasCal',)).run()
