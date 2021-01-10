import os
from os import path
import gcal
from canvasapi import Canvas


filepath = os.path.join(os.getenv("HOME"), '.canvasCal')
if not path.exists(filepath):
    #print('folder doesnt exist')
    os.mkdir(filepath)
# else:
#     print('folder exists')

API_DICT = {}
gcal.createPickle()
while True:
    API_URL = input("Please enter your institution's canvas url (like 'https://example.instructure.com'): ")
    API_KEY = input("Please enter your canvas API key: ")
    API_DICT[API_URL] = API_KEY
    if input('Type y to add another institution or any other button to exit').lower() != 'y':
        break


file = open(os.path.join(filepath, 'index.txt'), 'w')
file.write(len(API_DICT))
for URL,KEY in API_DICT.items():
    file.write(URL + '\n')
    file.write(KEY)

file.close()

calendarid = gcal.createCalendar()
file = open(os.path.join(filepath, 'calendar.txt'), 'w')
file.write(str(calendarid))
file.close()

for URL,KEY in API_DICT.items():
    canvas = Canvas(URL, KEY)
    courseDir = os.path.join(filepath, URL)
    os.mkdir(courseDir)

    d = {}
    file = open(os.path.join(courseDir, 'dict.txt'), 'w')
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

    file = open(os.path.join(courseDir, 'blacklist.txt'), 'w')
    for s in blacklist:
        file.write(str(s) + '\n')
    file.close()
