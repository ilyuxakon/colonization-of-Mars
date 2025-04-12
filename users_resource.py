from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.users import User


parser = reqparse.RequestParser()
parser.add_argument('surname')
parser.add_argument('name')
parser.add_argument('age', type=int)
parser.add_argument('position')
parser.add_argument('speciality')
parser.add_argument('address')
parser.add_argument('email')
parser.add_argument('city_from')
parser.add_argument('password')
parser.add_argument('check_password')


class UsersResource(Resource):

    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
                        only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from', 'modified_date'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})
    
    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)

        try:
            for key in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from', 'password', 'check_password']:
                if args[key] is not None:
                    if key == 'surname' or key == 'name' or key == 'position' or key == 'speciality' or key == 'address' or key == 'email' or key == 'city_from':
                        setattr(user, key, str(args[key]))

                    elif key == 'age':
                        user.age =  int(args[key])

                    elif key == 'password':
                        if args[key] == args['check_password']:
                            user.set_password(str(args[key]))

                        else:
                            return abort(400, message='Password error')
        
            session.commit()

        except Exception as error:
            return abort(400, message=str(error))
        
        return self.get(user_id)
            

class UsersListResource(Resource):

    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
                        only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from', 'modified_date'))
                        for item in users]})

    def post(self):
        args = parser.parse_args()

        if args['password'] == args['check_password']:
                try:
                    session = db_session.create_session()
                    user = User(
                        surname=str(args['surname']),
                        name=str(args['name']),
                        age=int(args['age']),
                        position=str(args['position']),
                        speciality=str(args['speciality']),
                        address=str(args['address']),
                        email=str(args['email']),
                        city_from=str(args['city_from'])
                    )
                    user.set_password(str(args['password']))

                    session.add(user)
                    session.commit()
                
                except Exception as error:
                    return abort(400, message=str(error))
                
                return jsonify({'id': user.id})
            
        return abort(400, message='Password error')


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")