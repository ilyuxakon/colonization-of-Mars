import flask


app = flask.Flask(__name__)


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')