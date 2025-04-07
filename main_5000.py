from flask import Flask
from flask import render_template, redirect
from flask import request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, BooleanField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user

from data import db_session, __all_models


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
request = request

login_manager = LoginManager()
login_manager.init_app(app)

User, Jobs = __all_models.users.User, __all_models.jobs.Jobs
db_session.global_init('db/mars.db')


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    check_password = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me?')
    submit = SubmitField('Submit')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def work_log():
    session = db_session.create_session()

    data = list()
    for job in session.query(Jobs).all():
        data.append({'id': job.id, 'job': job.job, 'leader': job.team_leader, 'duration': job.work_size, 'collaborators': job.collaborators, 'is_finished': 'if finished' if job.is_finished else 'is not finished'})

    return render_template('work_log_5000.html', data=data)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        session = db_session.create_session()

        if form.password.data != form.check_password.data:
            return render_template('register_5000.html', title='Регистрация', form=form, message='Неверный пароль')
        
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register_5000.html', title='Регистрация', form=form, message="Такой пользователь уже есть")
        
        user = User(
            email = form.email.data,
            surname = form.surname.data,
            name = form.name.data,
            age = form.age.data,
            position = form.position.data,
            speciality = form.speciality.data,
            address = form.address.data,
        )
        user.set_password(form.password.data)

        session.add(user)
        session.commit()

        return redirect('/success')        
    
    return render_template('register_5000.html', title='Регистрация', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        
        return render_template('login_5000.html', title='Логин', form=form, message='Неправильный логин или пароль')
    
    return render_template('login_5000.html', title='Логин', form=form)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')