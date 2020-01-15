from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import User, Abbonati
from blog.users.forms import (RegistrationForm, LoginForm,
                                   RequestResetForm, ResetPasswordForm)
from blog.users.utils import save_pic, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account creato per {form.username.data}', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title="Registrazione", form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You were successfully logged in', 'info')

            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login fallito', 'danger')
    return render_template('login.html', title="Log In", form=form)


@users.route('/logout')
def logout():
    logout_user()
    flash('You were successfully logged out', 'info')
    return redirect(url_for('main.index'))


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Ti abbiamo inviato un'email per resettare la password", 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password Request", form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Il token non è valido o potrebbe essere scaduto", "warning")
        return redirect(url_for('users.reset_request')) 
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash(f'Password modificata, prova ad accedere', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title="Reset Password", form=form)