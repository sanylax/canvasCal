from canvasapi import Canvas
import dateutil.parser

import quickstart

# Canvas API URL
API_URL = "https://gatech.instructure.com"
# Canvas API key
API_KEY = "rqOi4RFycbD67YL7rRispL5yS9GmqTAHH83hy90A9I6jYuTAAGaWbx85DSJHJ5dJ"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

for course in canvas.get_courses(enrollment_state='active'):
    # print(course.name, course.id)
    if course.id == 130456:
        for assignment in course.get_assignments():
            # print(assignment.name, dateutil.parser.isoparse(assignment.due_at))
            if assignment.due_at is not None:
                print(assignment.name, dateutil.parser.isoparse(assignment.due_at))
                quickstart.main(assignment.id, assignment.name, assignment.due_at)
            else:
                print(assignment.name)

print()
input("Press Enter to exit...")