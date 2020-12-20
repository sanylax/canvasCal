import http.client
import mimetypes
import json

conn = http.client.HTTPSConnection("gatech.instructure.com")
payload = ''
headers = {
  'Authorization': 'Bearer 2096~rqOi4RFycbD67YL7rRispL5yS9GmqTAHH83hy90A9I6jYuTAAGaWbx85DSJHJ5dJ'
}
conn.request("GET", "/api/v1/courses/140580/assignments", payload, headers)
res = conn.getresponse()
data = res.read()
print(data)

courses = user.get_courses()