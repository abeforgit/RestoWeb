from restoweb import app, db, bcrypt
from restoweb.models import User
from flask import url_for, redirect, flash, request, render_template
from flask_login import login_user, logout_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            flash('Username cannot be empty')
        if not password:
            flash('Password cannot be empty')
        if not username or not password:
            return redirect(url_for('login'))
        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            flash('Incorrect credentials, please try again')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        flash('Succesfully logged in')
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            flash('Username cannot be empty')
        if not password:
            flash('Password cannot be empty')
        if not username or not password:
            return redirect(url_for('signup'))
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username is already taken')
            return redirect(url_for('signup'))

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration succeeded')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        print('logging out')
        logout_user()
        return redirect(url_for('index'))
    else:
        return render_template('logout.html')
    return 'Logout'
