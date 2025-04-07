from flask import Flask
from flask import render_template, redirect
from flask import request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired

from data import db_session, jobs, users


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
request = request

db_session.global_init('db/mars.db')


class Register_Form(FlaskForm):
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



@app.route('/')
def work_log():
    session = db_session.create_session()

    data = list()
    for job in session.query(jobs.Jobs).all():
        data.append({'id': job.id, 'job': job.job, 'leader': job.team_leader, 'duration': job.work_size, 'collaborators': job.collaborators, 'is_finished': 'if finished' if job.is_finished else 'is not finished'})

    return render_template('work_log.html', data=data)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = Register_Form()

    if form.validate_on_submit():
        session = db_session.create_session()

        if form.password.data != form.check_password.data:
            return render_template('register.html', title='Регистрация', form=form, message='Неверный пароль')
        
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Такой пользователь уже есть")
        
        user = users.User(
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
    
    return render_template('register.html', title='Регистрация', form=form)
        

if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')