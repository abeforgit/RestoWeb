from restoweb import app, db, bcrypt, login_manager
from restoweb.models import User
from flask import request, Response, jsonify
from flask_login import login_user, logout_user, current_user


@login_manager.request_loader
def load_user_from_request(r):
    # Authorization: Token ABCDEFGHIJKLMNOPQRSTUVWXYZ012345
    tokenheader = r.headers.get('Authorization')
    apikey = tokenheader.split()[-1] if tokenheader else None
    if apikey:
        user = User.query.filter_by(apikey=apikey).first()
        if user:
            return user
    return None


@app.route('/login', methods=['POST'])
def login():
    if not request.json:
        return Response(status=400)

    if not current_user.is_authenticated:
        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            return Response(status=401)
        if not password:
            return Response(status=401)
        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return Response(status=401)
        login_user(user, remember=True)

    return jsonify({"token": current_user.apikey, "username": current_user.username, "is_admin": current_user.admin})


@app.route('/signup', methods=['POST'])
def signup():
    if (not request.json):
        return Response(status=400)
    username = request.json.get('username')
    password = request.json.get('password')

    if not username:
        return Response(status=401)
    if not password:
        return Response(status=401)
    user = User.query.filter_by(username=username).first()
    if user:
        return Response(status=409)

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return jsonify({"token": new_user.apikey}), 201


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return Response(status=200)
