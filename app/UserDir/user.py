from flask_jwt import JWT
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, request, jsonify
from app.UserDir.c_user import User
from app import app, db

mod_auth = Blueprint('auth', __name__, url_prefix='/api')

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user

@mod_auth.route('/register', methods=['POST'])
def register():
    data = request.get_json(True);
    user = User(username=data['username'], password=generate_password_hash(data['password']))
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Username not unique"), 400
    return jsonify(message="Success registrating"), 200

def identity(payload):
    return User.query.filter_by(id=payload['identity']).first()

jwt = JWT(app, authenticate, identity)