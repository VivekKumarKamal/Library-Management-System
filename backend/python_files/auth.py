from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, db
from functools import wraps
from passlib.hash import pbkdf2_sha256 as sha256



auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def sign_up():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)

    return jsonify({'message': 'User registered successfully', 'access_token': access_token}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_hash(password, sha256.hash(password)):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.id)

    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'is_librarian': user.is_librarian
    }
    print(access_token)
    return jsonify({'access_token': access_token, 'user': user_data}), 200


@auth.route('/api/current-user', methods=['GET'])
@jwt_required()
def current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'is_librarian': user.is_librarian
        }
        return jsonify(user_data), 200
    return jsonify({'message': 'User not found'}), 404


@auth.route('/api/user/profile', methods=['GET', 'PUT'])
@jwt_required()
def user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if request.method == 'GET':
        return jsonify({
            'name': user.name,
            'email': user.email
        }), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        if 'name' in data:
            user.name = data['name']
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200


def librarian_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or not current_user.is_librarian:
            return jsonify(message="Librarian access required"), 403
        return fn(*args, **kwargs)
    return wrapper


def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.is_librarian:
            return jsonify(message="Reader access required"), 403
        return fn(*args, **kwargs)
    return wrapper