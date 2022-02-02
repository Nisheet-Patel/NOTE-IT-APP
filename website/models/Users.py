from flask_login import UserMixin
from website import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    upassword = db.Column(db.String(100), nullable=False)
    note = db.relationship('Notes', backref='user')