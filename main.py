from canvasapi import Canvas
import ast
import gcal
import os.path
from os import path

# Canvas API URL
if path.exists('canvas.txt'):
    file = open('canvas.txt', 'r')
    API_URL = file.readline().strip()
    API_KEY = file.readline().strip()
else:
    API_URL = input("Please enter your institution's canvas url (like 'https://example.instructure.com'): ")
    API_KEY = input("Please enter your canvas API key: ")
    file = open('canvas.txt', 'w')
    file.write(API_URL + '\n')
    file.write(API_KEY)

# Canvas API key
# exit()
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

blacklist = []
if path.exists('courseBlacklist.txt'):
    for s in file:
        blacklist.append(s)





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