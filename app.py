import rumps
import main
import os

@rumps.timer(60*60*5)
def refresh(sender):
    rumps.notification("CanvasCal", subtitle = 'Refreshing', message ='')
    file = open(os.path.join(main.filepath, 'index.txt'), 'r')
    numCourses = int(file.readline().strip())
    print(numCourses)
    for i in range(numCourses):
        URL = file.readline().strip()
        KEY = file.readline().strip()
        code, message = main.processAssignments(URL, KEY)
        if code != 0:
            rumps.notification("CanvasCal", subtitle = 'Error', message =code)
        else:
            rumps.notification("CanvasCal", subtitle = 'Updated', message =message)




if __name__ == "__main__":
    rumps.App(name = 'CanvasCal', icon ='icon.png', menu=('CanvasCal',)).run()
