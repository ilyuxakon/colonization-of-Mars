from flask import Flask
from flask import url_for, render_template, redirect
from flask import request

from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

import os
import json
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
request = request


class LoginForm(FlaskForm):
    astronaut_id = StringField('id астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    captain_id = StringField('id капитана', validators=[DataRequired()])
    captain_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')

  
class GaleryForm(FlaskForm):
    img = MultipleFileField('Выберите файл', validators=[FileRequired()])
    submit = SubmitField('Отправить')


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base_8080.html', title=title)


@app.route('/promotion')
def promotion():
    return '<br>'.join(['Человечество вырастает из детства.',
                        'Человечеству мала одна планета.',
                        'Мы сделаем обитаемыми безжизненные пока планеты.',
                        'И начнем с Марса!',
                        'Присоединяйся!'])


@app.route('/image_mars')
def hello_mars():
    return f'''<h1>Жди нас, Марс!</h1>
               <img src="{url_for('static', filename='img/mars.png')}">
               <p>Вот она какая, красная планета</p>'''


@app.route('/promotion_image')
def promotion_image():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                    crossorigin="anonymous">
                    <link rel="stylesheet" href="{url_for('static', filename='css/style.css')}">
                    <title>Привет, Яндекс!</title>
                  </head>
                  <body>
                    <h1>Привет, Яндекс!</h1>
                    <img src="{url_for('static', filename='img/mars.png')}">
                    <div class="alert alert-dark" role="alert">
                      Человечество вырастает из детства.
                    </div>
                    <div class="alert alert-success" role="alert">
                      Человечеству мала одна планета.
                    </div>
                    <div class="alert alert-secondary" role="alert">
                      Мы сделаем обитаемыми безжизненные пока планеты.
                    </div>
                    <div class="alert alert-warning" role="alert">
                      И начнем с Марса!
                    </div>
                    <div class="alert alert-danger" role="alert">
                      Присоединяйся!
                    </div>
                  </body>
                </html>'''


@app.route('/astronaut_selection', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return f'''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet"
                          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                          integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                          crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        <title>Пример формы</title>
                      </head>
                      <body>
                        <center><h1>Анкета претендента</h1></center>
                        <center><h2>на участие в миссии</h2></center>
                        <div>
                          <form class="login_form" method="post" enctype="multipart/form-data">
                            <input type="surname" class="form-control" id="surname" placeholder="Введите фамилию" name="surname">
                            <input type="name" class="form-control" id="name" placeholder="Введите имя" name="name">
                            <label></label>
                            <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                            <br>
                            <div class="education-group">
                              <label for="education">Какое у вас образование</label>
                              <br>
                              <select class="education-control" id="education" name="education">
                                <option>Начальное</option>
                                <option>Основное общее</option>
                                <option>Среднее общее</option>
                                <option>Среднее профессиональное</option>
                                <option>Высшее</option>
                              </select>
                            </div>
                            <br>
                            <div class="profession-group">
                              <label for="profession">Какие у Вас есть профессии?</label>
                              <br>
                              <input type=checkbox class="profession-control" id="1", name="Инженер-исследователь">Инженер-исследователь<br></input>
                              <input type=checkbox class="profession-control" id="2", name="Инженер-строитель">Инженер-строитель<br></input>
                              <input type=checkbox class="profession-control" id="3", name="Пилот">Пилот<br></input>
                              <input type=checkbox class="profession-control" id="4", name="Метеоролог">Метеоролог<br></input>
                              <input type=checkbox class="profession-control" id="5", name="Инженер по жизнеобеспечению">Инженер по жизнеобеспечению<br></input>
                              <input type=checkbox class="profession-control" id="6", name="Инженер по радиационной защите">Инженер по радиационной защите<br></input>
                              <input type=checkbox class="profession-control" id="7", name="Врач">Врач<br></input>
                              <input type=checkbox class="profession-control" id="8", name="Экзобиолог">Экзобиолог<br></input>
                            </div>
                            <br>
                            <div class="form-group">
                              <label for="form-check">Укажите пол</label>
                              <div class="form-check">
                                <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                <label class="form-check-label" for="male">Мужской</label>
                              </div>
                              <div class="form-check">
                                <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                  <label class="form-check-label" for="female">Женский</label>
                              </div>
                            </div>
                            <br>
                            <div class="form-group">
                              <label for="about">show me your motivation!</label>
                              <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                            </div>
                            <br>
                            <div class="form-group">
                              <label for="photo">Приложите фотографию</label>
                              <input type="file" class="form-control-file" id="photo" name="file">
                            </div>
                            <br>
                            <div class="form-group form-check">
                              <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                              <label class="form-check-label" for="acceptRules">Готовы остаться на Марсе?</label>
                            </div>
                            <br>
                            <button type="submit" class="btn btn-primary">Отправить</button>
                          </form>
                        </div>
                      </body>
                    </html>'''
                        
    elif request.method == 'POST':
        dictionary = dict()
        dictionary['surname'] = request.form.get('surname')
        dictionary['name'] = request.form.get('name')
        dictionary['education'] = request.form.get('education')
        dictionary['sex'] = request.form.get('sex')
        dictionary['motivation'] = request.form.get('about')
        dictionary['ready'] = request.form.get('accept')

        dictionary['profession'] = []
        for prof in ['Инженер-исследователь', 'Инженер-строитель', 'Пилот', 'Метеоролог',
                     'Инженер по жизнеобеспечению', 'Инженер по радиационной защите', 'Врач', 'Экзобиолог']:
            if request.form.get(prof) == 'on':
                dictionary['profession'].append(prof)

        with open('templates/json/person.json', 'w', encoding='utf-8') as file:
            json.dump(dictionary, file)

        return "Форма отправлена"
    
  
@app.route('/choice/<planet_name>')
def choice(planet_name):
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                    crossorigin="anonymous">
                    <link rel="stylesheet" href="{url_for('static', filename='css/style.css')}">
                    <title>Привет, Яндекс!</title>
                  </head>
                  <body>
                    <h1>Моё предложение: {planet_name}</h2>
                    <div class="alert alert-light" role="alert">Эта планета близка к земле;</div>
                    <div class="alert alert-success" role="alert">На ней много необходимых ресурсов;</div>
                    <div class="alert alert-secondary" role="alert">На ней есть вода и атмосфера;</div>
                    <div class="alert alert-warning" role="alert">На ней есть небольшое магнитное поле;</div>
                    <div class="alert alert-danger" role="alert">Наконец она просто красива!</div>
                  </body>
                </html>'''


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def result(nickname, level, rating):
    return f'''<!doctype html>
              <html lang="en">
                <head>
                  <meta charset="utf-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                  <link rel="stylesheet" 
                  href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                  integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                  crossorigin="anonymous">
                  <link rel="stylesheet" href="{url_for('static', filename='css/style.css')}">
                  <title>Привет, Яндекс!</title>
                </head>
                <body>
                  <h1>Результаты отбора</h2>
                  <h6>Претендент на участие в миссии {nickname}:</h6>
                  <div class="alert alert-success" role="alert">Поздравляем! Ваш рейтинг после {level} этапа отбора</div>
                  <h6>составляет {rating}!</h6>
                  <div class="alert alert-warning" role="alert">Желаем удачи</div>
                </body>
              </html>'''


@app.route('/load_photo', methods=['POST', 'GET'])
def load_photo():
    global image
    if request.method == 'GET':
        return f'''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet"
                          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                          integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                          crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        <title>Пример формы</title>
                      </head>
                      <body>
                        <center><h1>Загрузка фотографии</h1></center>
                        <center><h2>для участия в миссии</h2></center>
                        <div>
                          <form class="login_form" method="post" enctype="multipart/form-data">
                            <div class="form-group">
                              <label for="photo">Приложите фотографию</label>
                              <br>
                              <br>
                              <input type="file" class="form-control-file" id="photo" name="file">
                            </div>
                            <br>
                            {"<img src=static/img/user_photo.png>" if os.path.exists('static/img/user_photo.png') else ''}
                            <br>
                            <button type="submit" class="btn btn-primary">Отправить</button>
                          </form>
                        </div>
                      </body>
                    </html>'''
                        
    elif request.method == 'POST':
        f = request.files['file']
        f.save('static/img/user_photo.png')
        return "Форма отправлена"


@app.route('/carousel')
def carousel():
    return f'''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet"
                          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                          integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                          crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
                          integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
                          crossorigin="anonymous"></script>
                        <title>Пример формы</title>
                      </head>
                      <body>
                        <center><h1>Пейзажи Марса</h1></center>
                        <div id="carouselExample" class="carousel slide">
                          <div class="carousel-inner">
                            <div class="carousel-item active">
                              <center><img src="{url_for('static', filename='img/1.png')}" class="d-block w-95"></center>
                            </div>
                            <div class="carousel-item">
                              <center><img src="{url_for('static', filename='img/2.png')}" class="d-block w-95"></center>
                            </div>
                            <div class="carousel-item">
                              <center><img src="{url_for('static', filename='img/3.png')}" class="d-block w-95"></center>
                            </div>
                            <div class="carousel-item">
                              <center><img src="{url_for('static', filename='img/4.png')}" class="d-block w-95"></center>
                            </div>
                            <div class="carousel-item">
                              <center><img src="{url_for('static', filename='img/5.png')}" class="d-block w-95"></center>
                            </div>
                          </div>
                          <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Previous</span>
                          </button>
                          <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Next</span>
                          </button>
                        </div>
                      </body>
                    </html>'''


@app.route('/list_prof/<list>')
def list_prof(list):
    list_professions = [
        "инженер-исследователь",
        "пилот",
        "строитель",
        "экзобиолог",
        "врач", 
        "инженер по терраформированию",
        "климатолог",
        "специалист по радиационной защите",
        "астрогеолог",
        "гляциолог",
        "инженер жизнеобеспечения",
        "метеоролог",
        "оператор марсохода",
        "киберинженер",
        "штурман", 
        "пилот дронов"
        ]
    return render_template('list_prof_8080.html', list=list, list_professions=list_professions, title='list of professions')


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    with open('templates/json/person.json', 'r', encoding='utf-8') as file:
        dictionary = json.load(file)
    dictionary['title'] = 'Анкета'

    return render_template('auto_answer_8080.html', **dictionary)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        astronaut_id = form.astronaut_id.data
        astronaut_password = form.astronaut_password.data
        captain_id = form.captain_id.data
        captain_password = form.captain_password.data

        with open('templates/json/crew.json', 'r', encoding='utf-8') as file:
            json_file = json.load(file)

            if astronaut_password == json_file[astronaut_id]['password'] and\
                captain_password == json_file[captain_id]['password'] and\
                ('captain' in json_file[captain_id]['roles'] or\
                'co-captain' in json_file[captain_id]['roles']):
                return redirect('/success')
    
    return render_template('login_8080.html', form=form)


@app.route('/success')
def succes():
    return '<h1>Hello world</h1>'


@app.route('/distribution')
def distribution():
    with open('templates/json/crew.json', 'r', encoding='utf-8') as file:
        json_file = json.load(file)

        crew = list()
        for crewmember in json_file.values():
            name = crewmember['name'] + ' ' + crewmember['surname']
            crew.append(name)

            if 'captain' in crewmember['roles']:
                crew.insert(0, name)
                crew.pop()

    return render_template('distribution_8080.html', crew=crew)


@app.route('/table/<sex>/<age>')
@app.route('/table_param/<sex>/<age>')
def table(sex, age):
    param = dict()
    if int(age) <= 21:
        param['img'] = url_for('static', filename='img/child_martian.jpg')

        if sex == 'male':
            param['color'] = '#b0c4de'

        else:
            param['color'] = '#ffa07a'

    else:
        param['img'] = url_for('static', filename='img/adult_martian.jpg')

        if sex == 'male':
            param['color'] = '#007ff0'

        else:
            param['color'] = '#ff4500'

    return render_template('table_8080.html', **param)


@app.route('/galery', methods=["GET", "POST"])
def galery():
    form = GaleryForm()
    if form.validate_on_submit():
        for f in form.img.data:
          filename = secure_filename(f.filename)
          f.save(os.path.join(app.root_path, 'static\img\galery', filename))
    
    files = os.listdir('static/img/galery')
    if len(files) == 0: files = False
    return render_template('galery_8080.html', title='Галерея', files=files, form=form)


@app.route('/member')
def member():
    with open('templates/json/crew.json', 'r', encoding='utf-8') as file:
      person = json.load(file)
      return render_template('member_8080.html', title='Член экипажа', person=person)


@app.route('/training/<prof>')
def training(prof):
    if 'инженер' in prof.lower() or 'строитель' in prof.lower():
        prof = 1
        
    else: prof = 0
    
    return render_template('training_8080.html', prof=prof)  
  
def custom_filter(crew):
    person = random.choice(list (crew.values()))
    param = dict()
    param['name'], param['surname'], param['photo'] = person['name'], person['surname'], person['photo']
    param['roles'] = ', '.join(sorted(person['roles']))
    return param

app.jinja_env.filters['custom_filter'] = custom_filter

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')