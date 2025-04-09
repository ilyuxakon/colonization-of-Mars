from flask import Flask
from flask import render_template, redirect
from flask import request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, BooleanField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

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
    submit = SubmitField('Sign in')


class AddJob(FlaskForm):
    job = StringField('Job Title', validators=[DataRequired()])
    team_leader = IntegerField('Team Leader id', validators=[DataRequired()])
    work_size = IntegerField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
@login_required
def work_log():
    session = db_session.create_session()

    data = list()
    for job in session.query(Jobs).all():
        data.append({'id': job.id, 'job': job.job, 'leader': job.team_leader, 'leader_name': f'{job.team_lead.name} {job.team_lead.surname}', 'duration': job.work_size, 'collaborators': job.collaborators, 'is_finished': 'if finished' if job.is_finished else 'is not finished'})
    
    return buffer('work_log_5000.html', data=data, current_user_id=current_user.id)


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

        login_user(user, remember=False)
        return redirect('/')       
    
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


@app.route('/addjob', methods=['POST', 'GET'])
@login_required
def addjob():
    form = AddJob()
    if form.validate_on_submit():
        session = db_session.create_session()

        if session.query(Jobs).filter(Jobs.job == form.job.data,
                                      Jobs.team_leader == form.team_leader.data,
                                      Jobs.work_size == form.work_size.data,
                                      Jobs.collaborators == form.collaborators.data,
                                      Jobs.is_finished == form.is_finished.data).first():
            return buffer('addjob_5000.html', title='Adding a job', form=form, message='Эта работа уже существует')
        
        job = Jobs(
            job = form.job.data,
            team_leader = form.team_leader.data,
            work_size = form.work_size.data,
            collaborators = form.collaborators.data,
            is_finished = form.is_finished.data
        )

        session.add(job)
        session.commit()

        return buffer('addjob_5000.html', title='Adding a job', form=form, message='Работа добавлена')
    
    return buffer('addjob_5000.html', title='Adding a job', form=form)


@app.route('/editjob/<job_id>', methods=['POST', 'GET'])
@login_required
def editjob(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()

    if current_user.id != 1 and current_user.id != job.team_leader:
        return redirect('/')

    form = AddJob()

    if form.validate_on_submit():
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data

        session.commit()
        return buffer('addjob_5000.html', title='Edit a job', form=form, message='Работа отредактирована')

    else:
        form.job.data = job.job
        form.team_leader.data = job.team_leader
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished

    return buffer('addjob_5000.html', title='Edit a job', form=form)


@app.route('/deletejob/<job_id>')
@login_required
def deletejob(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()

    if current_user.id == 1 or current_user.id == job.team_leader:
        session.delete(job)
        session.commit()

    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


def buffer(*arg, **args):
    return render_template(*arg, **args, username=f'{current_user.name} {current_user.surname}' if current_user.is_authenticated else 'Вы неавторизованны')

if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')