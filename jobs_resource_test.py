from requests import get, post, delete, put
import datetime


print('JobsListResource:')
print('get:')
# Вытягивание списка работ
print(get('http://127.0.0.1:5000/api/v2/jobs').json())

print()

print('post:')


# Создание новой работы с неправильными типом вводных данных
print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={
               'team_leader': 'qwerty',
               'job': 'job', 
               'work_size': 'qwerty',
               'collaborators': 'collaborators',
               'start_date': 12323,
               'end_date': 12334,
               'is_finished': 'qwerty'
           }).json())

print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={
               'team_leader': 1,
               'job': 'job', 
               'work_size': 1,
               'collaborators': 'collaborators',
               'start_date': 12323,
               'end_date': 12334,
               'is_finished': 'qwerty'
           }).json())

# Создание новой работы с корректными данными
print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={
               'team_leader': 1,
               'job': 'job', 
               'work_size': 1,
               'collaborators': 'collaborators',
               'start_date': str(datetime.datetime.now()),
               'end_date': str(datetime.datetime.now()),
               'is_finished': False
           }).json())

print()

print('JobsResource:')
print('get:')

# Получение работы с несуществующим id
print(get('http://127.0.0.1:5000/api/v2/jobs/999').json())

# Получение работы с id неправильного типа
print(get('http://127.0.0.1:5000/api/v2/jobs/qwerty').json())

# Корректное получения данных о работе
print(get('http://127.0.0.1:5000/api/v2/jobs/2').json())

print()

print('delete:')

# Удаление работы с несуществующим id
print(delete('http://127.0.0.1:5000/api/v2/jobs/999').json())

# Удаление работы с id неправильного типа
print(delete('http://127.0.0.1:5000/api/v2/jobs/qwerty').json())

# Корректное удаление работы
print(delete('http://127.0.0.1:5000/api/v2/jobs/7').json())

print()

print('put:')


# Запрос на изменение несуществующей записи
print(put('http://127.0.0.1:5000/api/v2/jobs/999', json={'age': 3}).json())

print(get('http://127.0.0.1:5000/api/v2/jobs/2').json())

# Запрос на изменение несуществующего атрибута
print(put('http://127.0.0.1:5000/api/v2/jobs/2', json={'11': 3}).json())

# Запрос на изменение атрибута на неправильный тип данных
print(put('http://127.0.0.1:5000/api/v2/jobs/2', json={'work_size': 'qwerty'}).json())

# Корректный запрос
print(put('http://127.0.0.1:5000/api/v2/jobs/2', json={'collaborators': '2, 3'}).json())