from flask import Blueprint, render_template,request, redirect, url_for, flash, Markup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from jinja2 import TemplateNotFound
from .models.Users import Users
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
    if current_user.is_authenticated:
        return redirect(url_for("views.notes"))
    
    if request.method == 'POST':
        username = request.form.get('username')
        upassword = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(username=username).first()
        
        # validators
        if not user:
            flash('Username Not Found !', "error")
        elif not check_password_hash(user.upassword, upassword):
            flash("Password Incorrect !", "error")
        else:
            login_user(user, remember=remember) 
            return redirect(url_for('views.notes'))

        return redirect(url_for('auth.login_page'))
    else:
        return render_template('login.html')

@auth.route('/signup', methods=['GET','POST'])
def signup_page():
    if current_user.is_authenticated:
        flash(Markup("You have already logged in. Click <a href='/notes'><u>here</u></a> to view notes"), "info")

    if request.method == 'POST':
        username = request.form.get('username')
        upassword = request.form.get('password')
        re_password = request.form.get('re-password')

        user = Users.query.filter_by(username=username).first()
        # validators
        if user:
            flash("Username already exists", "error")
        elif have_special_characters(username):
            flash("special characters are not allowed in username", "error")
        elif len(str(username)) < 4:
            flash("Username should be greater than 4 characters", "error")
        elif len(upassword) < 8:
            flash("Password should be greater than 8 characters", "error")
        elif upassword != re_password:
            flash("Both Password should Match", "error")
        else:
            new_user = Users(username=username,upassword=generate_password_hash(upassword, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            flash("Account created Successfully. Now Login", "info")
            return redirect(url_for('auth.login_page'))
        return redirect(url_for('auth.signup_page'))
    else:
        return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))