import rumps
import main

@rumps.timer(60*60*5)
def refresh(sender):
    rumps.notification("CanvasCal", subtitle = 'Refreshing', message ='')
    main.processAssignments()

if __name__ == "__main__":
    rumps.App(name = 'CanvasCal', icon ='icon.png', menu=('CanvasCal',)).run()
