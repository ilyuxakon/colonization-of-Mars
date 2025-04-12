from flask import jsonify
from flask_restful import reqparse, abort, Resource

import datetime

from data import db_session
from data.jobs import Jobs


parser = reqparse.RequestParser()
parser.add_argument('team_leader', type=int)
parser.add_argument('job')
parser.add_argument('work_size', type=int)
parser.add_argument('collaborators')
parser.add_argument('start_date')
parser.add_argument('end_date')
parser.add_argument('is_finished', type=bool)


class JobsResource(Resource):

    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
                        only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})
    
    def put(self, job_id):
        abort_if_job_not_found(job_id)
        args = parser.parse_args()
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)

        try:
            for key in ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']:
                if args[key] is not None:
                    if key == 'team_leader' or key == 'work_size':
                        setattr(job, key, int(args[key]))

                    elif key == 'job' or key == 'collaborators':
                        setattr(job, key, str(args[key]))

                    elif key == 'start_date' or key == 'end_date':
                        setattr(job, key, datetime.datetime.fromisoformat(args[key]))
                    
                    else:
                        job.is_finished = bool(args['is_finished'])
        
            session.commit()

        except Exception as error:
            return abort(400, message=str(error))
        
        return self.get(job_id)
            

class JobsListResource(Resource):

    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
                        only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
                        for item in jobs]})

    def post(self):
        args = parser.parse_args()

        try:
            session = db_session.create_session()
            job = Jobs(
                team_leader=int(args['team_leader']),
                job=str(args['job']),
                work_size=int(args['work_size']),
                collaborators=str(args['collaborators']),
                start_date=datetime.datetime.fromisoformat(args['start_date']),
                end_date=datetime.datetime.fromisoformat(args['end_date']),
                is_finished=bool(args['is_finished'])
            )

            session.add(job)
            session.commit()
        
        except Exception as error:
            return abort(400, message=str(error))
        
        return jsonify({'id': job.id})


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")