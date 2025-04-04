from flask import Flask
from flask import render_template
from flask import request

from data import db_session, jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
request = request


@app.route('/')
def work_log():
    db_session.global_init('db/mars.db')
    session = db_session.create_session()

    data = list()
    for job in session.query(jobs.Jobs).all():
        data.append({'id': job.id, 'job': job.job, 'leader': job.team_leader, 'duration': job.work_size, 'collaborators': job.collaborators, 'is_finished': 'if finished' if job.is_finished else 'is not finished'})

    return render_template('work_log.html', data=data)



if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')