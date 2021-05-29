from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from werkzeug.urls import url_parse

from app.auth import bp
from app.auth.forms import (
    LoginForm,
    RegistrationForm,
    EditProfileForm,
    ResetPasswordRequestForm,
    ResetPasswordForm
)
from app import db
from app.models import User, Order
from app.auth.send_mail import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """ Login """
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.profile')
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout')
@login_required
def logout():
    """ Logout """
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """ Register """
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('auth.profile'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/profile')
@login_required
def profile():
    """ Profile """
    orders = Order.query.filter_by(user=current_user)
    return render_template('auth/profile.html', title='Profile', orders=orders)


@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """ Edit profile """
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('auth/edit_profile.html', title='Edit Profile', form=form)


@bp.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    """ Request for reset password """
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        print('f')
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """ Reset password """
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Reset password', form=form)
