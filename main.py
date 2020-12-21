from canvasapi import Canvas
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

for course in canvas.get_courses(enrollment_state='active'):
    if course.id == 130456:
        for assignment in course.get_assignments():
            if assignment.due_at is not None:
                if(assignment.id) in d.keys():
                    if((assignment.name,assignment.due_at) != d[assignment.id]):
                        print(gcal.editEvent(assignment.id, assignment.name, assignment.due_at, assignment.description, calendarid))
                    else:
                        continue
                else:
                    gcal.addEvent(assignment.id, assignment.name, assignment.due_at, assignment.description, calendarid)   
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

input("Press Enter to exit...")