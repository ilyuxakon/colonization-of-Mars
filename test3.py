from requests import delete, get


# Запрос с неправильным индексом 
print(delete('http://127.0.0.1:5000/api/jobs/999').json())

# Запрос с неправильным типом данных в id
print(delete('http://127.0.0.1:5000/api/jobs/qwerty').json())

# Правильный запрос
print(delete('http://127.0.0.1:5000/api/jobs/9').json())

print(get('http://127.0.0.1:5000/api/jobs').json())