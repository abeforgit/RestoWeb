from restoweb import app, db, bcrypt
from restoweb.models import User
from flask import url_for, redirect, flash, request, render_template, Response
from flask_login import login_user, logout_user


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if (not request.json):
            return Response(status=400)
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
        return Response(status=200)


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
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
        return Response(status=200)


@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        logout_user()
        return Response(status=200)
