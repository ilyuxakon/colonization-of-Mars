from flask import Flask
from flask import render_template, redirect, abort, make_response, jsonify

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, BooleanField
from wtforms.validators import DataRequired

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_restful import Api

from requests import get

from data import db_session, __all_models
import jobs_api
import users_api
import users_resource
import jobs_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.register_blueprint(jobs_api.blueprint)
app.register_blueprint(users_api.blueprint)

api = Api(app)
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')

login_manager = LoginManager()
login_manager.init_app(app)

User, Jobs, Department = __all_models.users.User, __all_models.jobs.Jobs, __all_models.departments.Department
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


class AddDepartment(FlaskForm):
    title = StringField('Department Title', validators=[DataRequired()])
    chief = IntegerField('Chief', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = EmailField('Department Email', validators=[DataRequired()])
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


@app.route('/editjob/<int:job_id>', methods=['POST', 'GET'])
@login_required
def editjob(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()

    if not job:
        abort(404)
    
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


@app.route('/deletejob/<int:job_id>')
@login_required
def deletejob(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()

    if not job:
        abort(404)

    if current_user.id == 1 or current_user.id == job.team_leader:
        session.delete(job)
        session.commit()

    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/department')
@login_required
def department():
    session = db_session.create_session()

    data = list()
    for department in session.query(Department).all():
        data.append({'id': department.id, 'title': department.title, 'chief': department.chief, 'chief_name': f'{department.chief_u.name} {department.chief_u.surname}', 'members': department.members, 'email': department.email})
    
    return buffer('department_log_5000.html', data=data, current_user_id=current_user.id)


@app.route('/adddepartment', methods=['POST', 'GET'])
@login_required
def adddepartment():
    form = AddDepartment()
    if form.validate_on_submit():
        session = db_session.create_session()

        if session.query(Department).filter(Department.title == form.title.data,
                                      Department.chief == form.chief.data,
                                      Department.members == form.members.data,
                                      Department.email == form.email.data).first():
            return buffer('adddepartment_5000.html', title='Adding a department', form=form, message='Этот Департамент уже существует')
        
        department = Department(
            title = form.title.data,
            chief = form.chief.data,
            members = form.members.data,
            email = form.email.data,
        )

        session.add(department)
        session.commit()

        return buffer('adddepartment_5000.html', title='Adding a department', form=form, message='Департамент добавлен')
    
    return buffer('adddepartment_5000.html', title='Adding a department', form=form)


@app.route('/editdepartment/<int:department_id>', methods=['POST', 'GET'])
@login_required
def editdepartment(department_id):
    session = db_session.create_session()
    department = session.query(Department).filter(Department.id == department_id).first()

    if not department:
        abort(404)

    if current_user.id != 1 and current_user.id != department.chief:
        return redirect('/')

    form = AddDepartment()

    if form.validate_on_submit():
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data

        session.commit()
        return buffer('adddepartment_5000.html', title='Edit a department', form=form, message='Департамент отредактирован')

    else:
        form.title.data = department.title
        form.chief.data = department.chief
        form.members.data = department.members
        form.email.data = department.email

    return buffer('adddepartment_5000.html', title='Edit a department', form=form)


@app.route('/deletedepartment/<int:department_id>')
@login_required
def deletedepartment(department_id):
    session = db_session.create_session()
    department = session.query(Department).filter(Department.id == department_id).first()

    if not department:
        abort(404)

    if current_user.id == 1 or current_user.id == department.chief:
        session.delete(department)
        session.commit()

    return redirect('/department')


@app.route('/users_show/<int:user_id>')
@login_required
def users_show(user_id):
    user = get(f'http://127.0.0.1:5000/api/users/{user_id}')
    
    if not user.ok:
        abort(404)

    user = user.json()

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": user['user']['city_from'],
        "format": "json"}

    response = get(geocoder_api_server, params=geocoder_params)

    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    lowerCorner, upperCorner = toponym['boundedBy']['Envelope']['lowerCorner'], toponym['boundedBy']['Envelope']['upperCorner']

    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "bbox": f'{','.join(lowerCorner.split())}~{','.join(upperCorner.split())}',
        "apikey": apikey,
        "maptype": 'map'

    }

    map_api_server = "https://static-maps.yandex.ru/v1"
    # ... и выполняем запрос
    response = get(map_api_server, params=map_params)

    data = {
        'name': user['user']['name'],
        'surname': user['user']['surname'],
        'city_name': user['user']['city_from'],
        'img': response.url
    }

    return buffer('users_show_5000.html', data=data, current_user_id=current_user.id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(500)
def bad_request(_):
    return make_response(jsonify({'error': 'Eternal server error'}), 500)


def buffer(*arg, **args):
    return render_template(*arg, **args, username=f'{current_user.name} {current_user.surname}' if current_user.is_authenticated else 'Вы неавторизованны')


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')