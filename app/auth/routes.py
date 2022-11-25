from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.auth import bp
from app.auth.forms import UserRegForm, UserLoginForm
from app.models import User
from app import db


@bp.route('/')
def index():
    return redirect(url_for('auth/index.html'))


@bp.route('/reg', methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = UserRegForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/reg.html', title='Регистрация', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Авторизация', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
