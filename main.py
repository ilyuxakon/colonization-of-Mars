import flask


app = flask.Flask(__name__)
request = flask.request

@app.route('/')
def title():
    return 'Колонизация Марса'


@app.route('/index')
def slogan():
    return 'И на Марсе будут яблони цвести!'


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
               <img src="{flask.url_for('static', filename='img/mars.png')}">
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
                    <link rel="stylesheet" href="{flask.url_for('static', filename='css/style.css')}">
                    <title>Привет, Яндекс!</title>
                  </head>
                  <body>
                    <h1>Привет, Яндекс!</h1>
                    <img src="{flask.url_for('static', filename='img/mars.png')}">
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
                        <link rel="stylesheet" type="text/css" href="{flask.url_for('static', filename='css/style.css')}" />
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
                              <input type=checkbox class="profession-control" id="1", name="1">Инженер-исследователь<br></input>
                              <input type=checkbox class="profession-control" id="2", name="2">Инженер-строитель<br></input>
                              <input type=checkbox class="profession-control" id="3", name="3">Пилот<br></input>
                              <input type=checkbox class="profession-control" id="4", name="4">Метеоролог<br></input>
                              <input type=checkbox class="profession-control" id="5", name="5">Инженер по жизнеобеспечению<br></input>
                              <input type=checkbox class="profession-control" id="6", name="6">Инженер по радиационной защите<br></input>
                              <input type=checkbox class="profession-control" id="7", name="7">Врач<br></input>
                              <input type=checkbox class="profession-control" id="8", name="8">Экзобиолог<br></input>
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
        f = request.files['file']
        print(f.read())
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
                    <link rel="stylesheet" href="{flask.url_for('static', filename='css/style.css')}">
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
                  <link rel="stylesheet" href="{flask.url_for('static', filename='css/style.css')}">
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')