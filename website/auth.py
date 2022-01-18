from flask import Blueprint, render_template,request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from jinja2 import TemplateNotFound
from .models import Users
from string import punctuation
from . import db

auth = Blueprint('auth', __name__)

def have_special_characters(username):
    for c in punctuation:
        if c in username:
            return True
    return False

@auth.route('/login', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        upassword = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(username=username).first()
        
        # validators
        if not user:
            flash('Username Not Found !')
        elif not check_password_hash(user.upassword, upassword):
            flash("Password Incorrect !")
        else:
            login_user(user, remember=remember) 
            return redirect(url_for('views.notes'))

        return redirect(url_for('auth.login_page'))
    else:
        return render_template('login.html')

@auth.route('/signup', methods=['GET','POST'])
def signup_page():
    if request.method == 'POST':
        username = request.form.get('username')
        upassword = request.form.get('password')
        re_password = request.form.get('re-password')

        user = Users.query.filter_by(username=username).first()
        # validators
        if user:
            flash("Username address already exists")
        elif have_special_characters(username):
            flash("special characters are not allowed")
        elif len(str(username)) < 4:
            flash("Username should be greatter than 4 charaters")
        elif len(upassword) < 8:
            flash("Password should be greatter than 8 charaters")
        elif upassword != re_password:
            flash("Both Password should Match")
        else:
            new_user = Users(username=username,upassword=generate_password_hash(upassword, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login_page'))
        return redirect(url_for('auth.signup_page'))
    else:
        return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))