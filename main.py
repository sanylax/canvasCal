from canvasapi import Canvas
#import dateutil.parser
import ast
import gcal
import os.path
from os import path

# Canvas API URL
API_URL = "https://gatech.instructure.com"
# Canvas API key
API_KEY = "rqOi4RFycbD67YL7rRispL5yS9GmqTAHH83hy90A9I6jYuTAAGaWbx85DSJHJ5dJ"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
if path.exists('dict.txt'):
    file = open('dict.txt', 'r')
    for s in file:
        d = ast.literal_eval(s)
else:
    d = {}

if path.exists('calendar.txt'):
    file = open('calendar.txt', 'r')
    for s in file:
        calendarid = s
else:
    calendarid = gcal.createCalendar()

#print(d)
if(True):
    for course in canvas.get_courses(enrollment_state='active'):
        # print(course.name, course.id)
        if course.id == 130456:
            for assignment in course.get_assignments():
                # print(assignment.name, dateutil.parser.isoparse(assignment.due_at))
                if assignment.due_at is not None:
                    #print(assignment.name)
                    if(assignment.id) in d.keys():
                        if((assignment.name,assignment.due_at) != d[assignment.id]):
                            print(gcal.editEvent(assignment.id, assignment.name + '*', assignment.due_at, calendarid))
                        else:
                            continue
                    else:
                        gcal.addEvent(assignment.id, assignment.name, assignment.due_at, calendarid)   
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

else:
    gcal.printCalendars()


#input("Press Enter to exit...")