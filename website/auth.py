from flask import Blueprint, render_template
from jinja2 import TemplateNotFound

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login_page():
    return render_template('login.html')

@auth.route('/signup')
def signup_page():
    return render_template('signup.html')