from datetime import timedelta
from flask import Flask, request, jsonify
import os
import uuid

from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "RqVJ*735DAs=" 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

users_db = {
    'user1': {'password': 'parola1', 'role': 'admin'},
    'user2': {'password': 'parola2', 'role': 'owner'},
    'user3': {'password': 'parolaX', 'role': 'owner'}
}

active_tokens = {}

@app.route("/")
def hello():
    return """
    <h1>Bine ai venit!</h1>
    """

@app.route('/auth', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_db.get(username)
    if user and user['password'] == password:
        token = create_access_token(identity={'username': username, 'role': user['role']})
        active_tokens[token] = user['role']
        return jsonify(token=token), 200
    else:
        return jsonify(message='Nume sau parola gresita'), 401

@app.route('/auth/jwtStore', methods=['GET'])
@jwt_required()
def validate():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify(message='Token lipsa sau invalid'), 401

    token = auth_header.split()[1]
    role = active_tokens.get(token)
    if role:
        return jsonify(role=role), 200
    else:
        return jsonify(message='Token-ul nu exista sau e expirat'), 404

@app.route('/auth/jwtStore', methods=['DELETE'])
@jwt_required()
def logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify(message='Token lipsa sau invalid'), 401

    token = auth_header.split()[1]
    if token in active_tokens:
        del active_tokens[token]
        return jsonify(message='Logout cu succes'), 200
    else:
        return jsonify(message='Token-ul nu exista sau a expirat'), 404


if __name__ == "__main__":
    app.run()