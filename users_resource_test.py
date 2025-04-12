from requests import get, post, delete, put


print('UsersListResource:')
print('get:')
# Вытягивание списка пользователей
print(get('http://127.0.0.1:5000/api/v2/users').json())

print()

print('post:')


# Создание нового пользователя с неправильными типом вводных данных
print(post('http://127.0.0.1:5000/api/v2/users',
           json={
               'name': True,
               'surname': False,
               'age': 'qwerty',
               'position': 'a',
               'speciality': 'a',
               'email': False,
               'city_from': 'A',
               'password': '123',
               'check_password': '123',
           }).json())

# Создание нового пользователя с разными паролями
print(post('http://127.0.0.1:5000/api/v2/users',
           json={
               'name': 'qwerty',
               'surname': 'qwerty',
               'age': 21,
               'position': 'a',
               'speciality': 'a',
               'email': 'qwerty',
               'city_from': 'A',
               'password': '123',
               'check_password': '1234'
           }).json())

# Создание нового пользователя с корректными данными
print(post('http://127.0.0.1:5000/api/v2/users',
           json={
               'name': 'qwerty',
               'surname': 'qwerty',
               'age': 21,
               'position': 'a',
               'speciality': 'a',
               'email': 'qwerty',
               'city_from': 'A',
               'password': '123',
               'check_password': '123'
           }).json())

print()

print('UsersResource:')
print('get:')

# Получение пользователя с несуществующим id
print(get('http://127.0.0.1:5000/api/v2/users/999').json())

# Получение пользователя с id неправильного типа
print(get('http://127.0.0.1:5000/api/v2/users/qwerty').json())

# корректное получения данных о пользователе
print(get('http://127.0.0.1:5000/api/v2/users/1').json())

print()

print('delete:')

# Удаление пользователя с несуществующим id
print(delete('http://127.0.0.1:5000/api/v2/users/999').json())

# Удаление пользователя с id неправильного типа
print(delete('http://127.0.0.1:5000/api/v2/users/qwerty').json())

# корректное удаление пользователя
print(delete('http://127.0.0.1:5000/api/v2/users/5').json())

print()

print('put:')


# Запрос на изменение несуществующей записи
print(put('http://127.0.0.1:5000/api/v2/users/999', json={'age': 3}).json())

print(get('http://127.0.0.1:5000/api/v2/users/2').json())

# Запрос на изменение несуществующего атрибута
print(put('http://127.0.0.1:5000/api/v2/users/2', json={'11': 3}).json())

# Запрос на изменение атрибута на неправильный тип данных
print(put('http://127.0.0.1:5000/api/v2/users/2', json={'age': 'qwerty'}).json())

# Корректный запрос
print(put('http://127.0.0.1:5000/api/v2/users/2', json={'address': 'module_5'}).json())