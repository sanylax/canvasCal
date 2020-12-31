# pyinstaller --hidden-import="pkg_resources.py2_warn" --hidden-import="googleapiclient" --hidden-import="apiclient"  main.py --windowed --hidden-import plyer.platforms.win.notification --onefile

from canvasapi import Canvas
import ast
import gcal
import os
from os import path
#import pdb
#from plyer.utils import platform
#from plyer import notification


def failed(error):
    #pdb.set_trace(error)
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
    print('Refreshing')
    #pdb.set_trace('Refreshing')
    filepath = os.path.join(os.getenv("HOME"), '.canvasCal')
    print('got here')
    # Canvas API URL
    print('got here')
    if path.exists(os.path.join(filepath, 'canvas.txt')):
        file = open(os.path.join(filepath, 'canvas.txt'), 'r')
        API_URL = file.readline().strip()
        API_KEY = file.readline().strip()
        file.close()
    else:
        failed('canvas.txt')
    print(API_KEY)
    print(API_URL)
    print('got here2')
    # Canvas API key
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)
    if path.exists(os.path.join(filepath, 'dict.txt')):
        file = open(os.path.join(filepath, 'dict.txt'), 'r')
        for s in file:
            d = ast.literal_eval(s)
        file.close()
    else:
        d = {}
    print('got here3')
    if path.exists(os.path.join(filepath, 'calendar.txt')):
        file = open(os.path.join(filepath, 'calendar.txt'), 'r')
        for s in file:
            calendarid = s
        file.close()
    else:
        failed('calendar')
    print('got here')
    blacklist = []
    if path.exists(os.path.join(filepath, 'blacklist.txt')):
        file = open(os.path.join(filepath, 'blacklist.txt'), 'r')
        for s in file:
            blacklist.append(s.strip())
        file.close()

    else:
       failed('blacklist')
    print('got here')
    for course in canvas.get_courses(enrollment_state='active'):
        print(course.name)
        if str(course.id) not in blacklist:
            for assignment in course.get_assignments():
                print(assignment.name)
                if assignment.due_at is not None:
                    if(assignment.id) in d.keys():
                        if((assignment.name,assignment.due_at) != d[assignment.id]):
                            description = getDescription(assignment)
                            #x = 
                            gcal.editEvent(assignment.id, assignment.name, assignment.due_at, description, calendarid)
                            # pdb.set_trace(x)
                            # print(x)
                        else:
                            continue
                    else:
                        print(assignment.name)
                        #exit()
                        #pdb.set_trace(assignment.name)
                        description = getDescription(assignment)
                        gcal.addEvent(assignment.id, assignment.name, assignment.due_at, description, calendarid)   
                    d[assignment.id] = (assignment.name, assignment.due_at)
                else:
                    pass
                    #print(assignment.name)

    file = open(os.path.join(filepath, 'dict.txt'), 'w')
    file.write(str(d))
    file.close()

    file = open(os.path.join(filepath, 'calendar.txt'), 'w')
    file.write(str(calendarid))
    file.close()

    file = open(os.path.join(filepath, 'blacklist.txt'), 'w')
    for s in blacklist:
        file.write(str(s) + '\n')
    file.close()