# pyinstaller --hidden-import="pkg_resources.py2_warn" --hidden-import="googleapiclient" --hidden-import="apiclient"  main.py --windowed --hidden-import plyer.platforms.win.notification --onefile

import ast
import os
from os import path
from canvasapi import Canvas
import gcal
from datetime import datetime
from os.path import expanduser
home = expanduser("~")
global filepath
filepath = os.path.join(home, '.canvasCal')

def log(code, message):
    file = open(os.path.join(filepath, 'errorlog.txt'), 'w')
    now = datetime.now().strftime('%m/%d/%Y	%H:%M%S')
    file.write(now + ' ' + code + '\n')
    file.close()
    return code
    

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

def processAssignments(API_URL, API_KEY):
    gcal.loadPickle()
    print('Refreshing Events')
   
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)
    institutionName = canvas.search_accounts(**{'domain':API_URL[8:-1]})[0]['name']
    courseDir = os.path.join(filepath, institutionName.replace(' ', '_'))

    if path.exists(os.path.join(courseDir, 'dict.txt')):
        file = open(os.path.join(courseDir, 'dict.txt'), 'r')
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
        return log('calendar')

    blacklist = []
    if path.exists(os.path.join(courseDir, 'blacklist.txt')):
        file = open(os.path.join(courseDir, 'blacklist.txt'), 'r')
        for s in file:
            blacklist.append(s.strip())
        file.close()
    else:
        return log('blacklist')

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
                        print(assignment.name)
                    events[assignment.id] = (assignment.name, assignment.due_at)
                else:
                    pass

    file = open(os.path.join(courseDir, 'dict.txt'), 'w')
    file.write(str(events))
    file.close()

    file = open(os.path.join(courseDir, 'calendar.txt'), 'w')
    file.write(str(calendarid))
    file.close()

    file = open(os.path.join(courseDir, 'blacklist.txt'), 'w')
    for s in blacklist:
        file.write(str(s) + '\n')
    file.close()

    log('0', institutionName)
    return 0, institutionName