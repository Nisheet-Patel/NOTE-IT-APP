from flask_login import UserMixin
from . import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    upassword = db.Column(db.String(100), nullable=False)
    note = db.relationship('Notes', backref='user')

class Notes(db.Model):
    __searchable__ = ['title', 'body']
    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    is_public = db.Column(db.Integer, nullable=False)
    update_date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    public = db.relationship('Public_Notes', backref='note')

class Public_Notes(db.Model):
    __tablename__ = "public_notes"
    Id =  db.Column(db.Integer, db.ForeignKey('notes.note_id'))
    slug = db.Column(db.String(16), primary_key=True)
    
