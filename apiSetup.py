import os
from os import path
from canvasapi import Canvas
import gcal

filepath = os.path.join(os.getenv("HOME"), '.canvasCal')
if not path.exists(filepath):
    os.mkdir(filepath)

API_URL = input("Please enter your institution's canvas url (like 'https://example.instructure.com'): ")
API_KEY = input("Please enter your canvas API key: ")
file = open(os.path.join(filepath, 'canvas.txt'), 'w')

file.write(API_URL + '\n')
file.write(API_KEY)
file.close()

canvas = Canvas(API_URL, API_KEY)

calendarid = gcal.createCalendar()
file = open(os.path.join(filepath, 'calendar.txt'), 'w')
file.write(str(calendarid))
file.close()

d = {}
file = open(os.path.join(filepath, 'dict.txt'), 'w')
file.write(str(d))
file.close()

blacklist = []
whitelist = []
for course in canvas.get_courses(enrollment_state='active'):
    print(course.name)
    choice = input('type y if you want to keep this course or anything else to ignore it: ')
    if choice.upper() != 'Y':
        blacklist.append(str(course.id))
    else:
        whitelist.append(course.name)
print()
print("The following courses will be added to your calendar:")
for course in whitelist:
    print(course)

file = open(os.path.join(filepath, 'blacklist.txt'), 'w')
for s in blacklist:
    file.write(str(s) + '\n')
file.close()
