from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from application import login_manager
from application.models.model import *
from application.forms import SignInForm, SignUpForm


auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """Sign in route"""
    # if request.method == 'GET' request.form is empty, so it equals to form_signin = SignInForm()
    form_signin = SignInForm(formdata=request.form)
    if request.method == 'POST' and form_signin.validate():
        email = request.form['email']
        password = request.form['password']
        user = db.session.scalars(db.select(User).where(User.email == email)).first()
        if user:
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('home.index'))

            flash("Username or password is incorrect", category='bad_creds')
            return redirect(url_for('auth.signin'))

        flash("Such user does not exist", category='bad_creds')

    # if request.method == 'GET' or form is invalid (form.errors is not empty)
    return render_template('auth/signin.html.jinja2', form=form_signin)


@auth_bp.route('/signup', methods = ['GET', 'POST'])
def signup():
    """Sign up route"""
    # if request.method == 'GET' request.form is empty, so it equals to form_signup = SignUpForm()
    form_signup = SignUpForm(formdata=request.form)
    if request.method == 'POST' and form_signup.validate():
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        user = db.session.scalars(db.select(User).where(User.email == email)).first()
        if user is None:
            user = User(name = name, email = email)
            user.set_password(password)
            user.set_role('User')
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home.index'))

        flash("User with this email is already registered", category='bad_creds')
        
    # if request.method == 'GET' or form is invalid (form.errors is not empty)
    return render_template('auth/signup.html.jinja2', form=form_signup)


@auth_bp.route('/signout', methods=['GET'])
def signout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have been succesfully logged out", category='success')
    return redirect(url_for('home.index'))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page', category='unauthorized')
    return redirect(url_for('auth.signin'))