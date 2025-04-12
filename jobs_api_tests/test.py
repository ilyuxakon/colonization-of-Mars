import requests

response = requests.get('http://127.0.0.1:5000/api/jobs').json()
print(response)

response = requests.get('http://127.0.0.1:5000/api/jobs/1').json()
print(response)

response = requests.get('http://127.0.0.1:5000/api/jobs/999').json()
print(response)

response = requests.get('http://127.0.0.1:5000/api/jobs/qwerty').json()
print(response)