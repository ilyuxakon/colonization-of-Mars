import flask
from flask import jsonify, make_response
from flask import request

from data import db_session
from data.users import User


blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from', 'modified_date'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>')
def get_one_user(user_id):   
    session = db_session.create_session()
    user = session.query(User).get(user_id)

    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from', 'modified_date'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from', 'password', 'check_password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    if request.json['password'] != request.json['check_password']:
        return make_response(jsonify({'error': 'Password error'}), 400)
    
    session = db_session.create_session()
    
    try:
        user = User(
            surname=str(request.json['surname']),
            name=str(request.json['name']),
            age=int(request.json['age']),
            position=str(request.json['position']),
            speciality=str(request.json['speciality']),
            address=str(request.json['address']),
            email=str(request.json['email']),
            city_from=str(request.json['city_from'])
        )
        user.set_password(str(request.json['password']))
        
        session.add(user)
        session.commit()

    except Exception as error:
        return make_response(jsonify({'error': str(error)}), 400)

    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)

    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)

    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    
    elif not any(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from', 'password', 'check_password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    
    try:
        for key in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from', 'password', 'check_password']:
            if key in request.json:
                if key == 'surname' or key == 'name' or key == 'position' or key == 'speciality' or key == 'address' or key == 'email' or key == 'city_from':
                    setattr(user, key, str(request.json[key]))

                elif key == 'age':
                    user.age =  int(request.json[key])

                elif key == 'password':
                    if request.json[key] == request.json['check_password']:
                        user.set_password(str(request.json[key]))

                    else:
                        return make_response(jsonify({'error': 'Password error'}), 400)
        
        session.commit()

    except Exception as error:
        return make_response(jsonify({'error': str(error)}), 400)

    return get_one_user(user_id)