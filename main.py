# pyinstaller --hidden-import="pkg_resources.py2_warn" --hidden-import="googleapiclient" --hidden-import="apiclient"  main.py --windowed --hidden-import plyer.platforms.win.notification --onefile

from canvasapi import Canvas
import ast
import gcal
import os
from os import path
from canvasapi import Canvas


def failed(error):
    filepath = os.path.join(os.getenv("HOME"), '.canvasCal')
    file = open(file = open(os.path.join(filepath, 'errorlog.txt'), 'w'))
    file.write(error)
    file.close()
    

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
    print('Refreshing Events')
    filepath = os.path.join(os.getenv("HOME"), '.canvasCal')
    # Canvas API URL
    if path.exists(os.path.join(filepath, 'canvas.txt')):
        file = open(os.path.join(filepath, 'canvas.txt'), 'r')
        API_URL = file.readline().strip()
        API_KEY = file.readline().strip()
        file.close()
    else:
        failed('canvas')
    # Canvas API key
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)
    if path.exists(os.path.join(filepath, 'dict.txt')):
        file = open(os.path.join(filepath, 'dict.txt'), 'r')
        for s in file:
            events = ast.literal_eval(s)
        file.close()
    else:
        events = {}

    if path.exists(os.path.join(filepath, 'calendar.txt')):
        file = open(os.path.join(filepath, 'calendar.txt'), 'r')
        for s in file:
            calendarid = s
        file.close()
    else:
        failed('calendar')

    blacklist = []
    if path.exists(os.path.join(filepath, 'blacklist.txt')):
        file = open(os.path.join(filepath, 'blacklist.txt'), 'r')
        for s in file:
            blacklist.append(s.strip())
        file.close()
    else:
        failed('blacklist')

    for course in canvas.get_courses(enrollment_state='active'):
        if str(course.id) not in blacklist:
            for assignment in course.get_assignments():
                if assignment.due_at is not None:
                    if(assignment.id) in events.keys():
                        if((assignment.name,assignment.due_at) != events[assignment.id]):
                            description = getDescription(assignment)
                            gcal.editEvent(assignment.id, assignment.name, assignment.due_at, description, calendarid)
                        else:
                            continue
                    else:
                        description = getDescription(assignment)
                        gcal.addEvent(assignment.id, assignment.name, assignment.due_at, description, calendarid)   
                    events[assignment.id] = (assignment.name, assignment.due_at)
                else:
                    pass

    file = open(os.path.join(filepath, 'dict.txt'), 'w')
    file.write(str(events))
    file.close()

    file = open(os.path.join(filepath, 'calendar.txt'), 'w')
    file.write(str(calendarid))
    file.close()

    file = open(os.path.join(filepath, 'blacklist.txt'), 'w')
    for s in blacklist:
        file.write(str(s) + '\n')
    file.close()