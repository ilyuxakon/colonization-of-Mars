from requests import put, get


print(get('http://127.0.0.1:5000/api/jobs/1').json())

# Запрос на изменение несуществующей записи
print(put('http://127.0.0.1:5000/api/jobs/999', json={'team_leader': 3}).json())

# Запрос на изменение несуществующего атрибута
print(put('http://127.0.0.1:5000/api/jobs/1', json={'11': 3}).json())

# Запрос на изменение атрибута на неправильный тип данных
print(put('http://127.0.0.1:5000/api/jobs/1', json={'team_leader': 'qwerty'}).json())

# Корректный запрос
print(put('http://127.0.0.1:5000/api/jobs/1', json={'team_leader': 3}).json())