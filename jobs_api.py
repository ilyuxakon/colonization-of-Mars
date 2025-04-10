import flask
from flask import jsonify, make_response
from flask import request

from data import db_session
from data.jobs import Jobs

import datetime


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>')
def get_one_job(job_id):   
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    return jsonify(
        {
            'job': job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    
    session = db_session.create_session()
    
    try:
        job = Jobs(
            team_leader=int(request.json['team_leader']),
            job=str(request.json['job']),
            work_size=int(request.json['work_size']),
            collaborators=str(request.json['collaborators']),
            start_date=datetime.datetime.fromisoformat(request.json['start_date']),
            end_date=datetime.datetime.fromisoformat(request.json['end_date']),
            is_finished=bool(request.json['is_finished'])
        )

        session.add(job)
        session.commit()

    except Exception as error:
        return make_response(jsonify({'error': str(error)}), 400)

    return jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    
    elif not any(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    
    try:
        for key in ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']:
            if key in request.json:
                if key == 'team_leader' or key == 'work_size':
                    setattr(job, key, int(request.json[key]))

                elif key == 'job' or key == 'collaborators':
                    setattr(job, key, str(request.json[key]))

                elif key == 'start_date' or key == 'end_date':
                    setattr(job, key, datetime.datetime.fromisoformat(request.json[key]))
                
                else:
                    job.is_finished = bool(request.json['is_finished'])
        
        session.commit()

    except Exception as error:
        return make_response(jsonify({'error': str(error)}), 400)

    return get_one_job(job_id)