# pyinstaller --hidden-import="pkg_resources.py2_warn" --hidden-import="googleapiclient" --hidden-import="apiclient"  main.py --windowed --hidden-import plyer.platforms.win.notification --onefile

from canvasapi import Canvas
import ast
import gcal
from os import path
from plyer.utils import platform
from plyer import notification
def failed():
    notification.notify(
        title='CanvasCal failed to run',
        message='Please run setup.exe',
        app_name='CanvasCal',
        #app_icon='path/to/the/icon.' + ('ico' if platform == 'win' else 'png')
    )

def getDescription(assignment):
    if assignment.html_url and assignment.description:
        description  = f'<a href="{assignment.html_url}">Link to assignment on Canvas</a><br />' + assignment.description
    elif assignment.description:
        description = assignment.description
    elif assignment.html_url:
        description = '<a href="{assignment.html_url}">Link to assignment on Canvas</a>'
    else:
        description = ''
    return description

def processAssignments():
    # Canvas API URL
    if path.exists('canvas.txt'):
        file = open('canvas.txt', 'r')
        API_URL = file.readline().strip()
        API_KEY = file.readline().strip()
        file.close()
    else:
        failed()

    # Canvas API key
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)
    if path.exists('dict.txt'):
        file = open('dict.txt', 'r')
        for s in file:
            d = ast.literal_eval(s)
        file.close()
    else:
        failed()

    if path.exists('calendar.txt'):
        file = open('calendar.txt', 'r')
        for s in file:
            calendarid = s
        file.close()
    else:
        failed()

    blacklist = []
    if path.exists('blacklist.txt'):
        file = open('blacklist.txt', 'r')
        for s in file:
            blacklist.append(s.strip())
        file.close()

    else:
       failed()

    for course in canvas.get_courses(enrollment_state='active'):
        if str(course.id) not in blacklist:
            for assignment in course.get_assignments():
                if assignment.due_at is not None:
                    if(assignment.id) in d.keys():
                        if((assignment.name,assignment.due_at) != d[assignment.id]):
                            description = getDescription(assignment)
                            print(gcal.editEvent(assignment.id, assignment.name, assignment.due_at, description, calendarid))
                        else:
                            continue
                    else:
                        print(assignment.name)
                        description = getDescription(assignment)
                        gcal.addEvent(assignment.id, assignment.name, assignment.due_at, description, calendarid)   
                    d[assignment.id] = (assignment.name, assignment.due_at)
                else:
                    pass
                    #print(assignment.name)

    file = open('dict.txt', 'w')
    file.write(str(d))
    file.close()

    file = open('calendar.txt', 'w')
    file.write(str(calendarid))
    file.close()

    file = open('blacklist.txt', 'w')
    for s in blacklist:
        file.write(str(s) + '\n')
    file.close()