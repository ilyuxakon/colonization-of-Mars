from requests import post, get
import datetime


# Пустой запрос:
print(post('http://localhost:5000/api/jobs', json={}).json())

# Запрос с пропуском полей:
print(post('http://localhost:5000/api/jobs',
           json={'team_leader': 1}).json())

# Запрос с неправильным типом данных:
print(post('http://localhost:5000/api/jobs',
           json={'team_leader': 'Заголовок',
                 'job': 'Работа',
                 'work_size': 1,
                 'collaborators': '2, 3',
                 'start_date': str(datetime.datetime.now()),
                 'end_date': str(datetime.datetime.now()),
                 'is_finished': False}).json())

# Правильный запрос
print(post('http://localhost:5000/api/jobs',
           json={'team_leader': 1,
                 'job': 'Работа',
                 'work_size': 1,
                 'collaborators': '2, 3',
                 'start_date': str(datetime.datetime.now()),
                 'end_date': str(datetime.datetime.now()),
                 'is_finished': False}).json())

print(get('http://127.0.0.1:5000/api/jobs').json())