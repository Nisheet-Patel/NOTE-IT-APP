from flask import Blueprint, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
from .models import Notes, Public_Notes, Users
from . import db
from secrets import token_urlsafe 
import datetime

__DATETIME__ = datetime.datetime.now().strftime("%d %m %Y %X")
views = Blueprint('views',__name__)
__PUBLIC_NOTE_KEY__ = 10

@views.route('/')
def home():
    return render_template('index.html')
    

@views.route('/notes')
def notes():
    search_value = request.args.get('search-value')
    if search_value:
        notes = db.session.query(Notes,Public_Notes).join(Public_Notes, Public_Notes.Id == Notes.note_id, isouter=True).filter(Notes.user_id == '2').filter(Notes.title.contains(search_value) | Notes.body.contains(search_value)).order_by(Notes.update_date.desc())
        print(search_value)
        print(notes)
        return render_template('main-page.html', notes=notes)

    notes = db.session.query(Notes,Public_Notes).join(Public_Notes, Public_Notes.Id == Notes.note_id, isouter=True).filter(Notes.user_id == '2')

    return render_template('main-page.html', notes=notes)

@views.route('/shared')
def shared():
    notes = db.session.query(Notes,Public_Notes).join(Public_Notes, Public_Notes.Id == Notes.note_id).filter(Notes.user_id == '2')

    return render_template('main-page.html', notes=notes)

@views.route('/notes/<noteid>')
def note(noteid):
    note = Notes.query.get(noteid)
    if note.is_public:
        public_note_ = Public_Notes.query.filter_by(Id=noteid).first().slug
    else:
        public_note_ = None
    return render_template('note-private.html',note=note, note_key=public_note_)


@views.route('/add-note', methods=['GET', 'POST'])
def add_note_page():
    if request.method == 'POST':

        is_public = 1 if request.form.get('is-public') == 'on' else 0
        user_id = 2

        note = Notes(
            title = request.form.get('note-title'),
            body = request.form.get('note-body'),
            is_public = is_public,
            update_date = __DATETIME__,
            user_id = user_id
        )
        db.session.add(note)
        db.session.commit()
        print("NOTE ID :",note.note_id)

        if is_public:        
            pnote = Public_Notes(Id=note.note_id, slug=token_urlsafe(__PUBLIC_NOTE_KEY__))
            db.session.add(pnote)
            db.session.commit()

        return redirect(url_for('views.notes'))
    else:
        return render_template('add-note.html')

@views.route('/edit-note/<noteid>', methods=['GET','POST'])
def edit_page_page(noteid):
    if request.method == 'POST':
        is_public = 1 if request.form.get('is-public') == 'on' else 0

        note = Notes.query.get(noteid)

        if is_public != note.is_public:
            # Add
            if is_public:
                pnote = Public_Notes(Id=note.note_id, slug=token_urlsafe(__PUBLIC_NOTE_KEY__))
                db.session.add(pnote)
                db.session.commit()
            else:
                # remove
                pnote = Public_Notes.query.filter_by(Id=noteid).first()
                db.session.delete(pnote)
                db.session.commit()

        note.title = request.form.get('note-title')
        note.body = request.form.get('note-body')
        note.is_public = is_public
        update_date = __DATETIME__

        db.session.commit()

        return redirect(url_for('views.notes') + f'/{note.note_id}')
    else:
        note = Notes.query.get(noteid)
        checked = "checked" if note.is_public else "unchecked"
        return render_template('edit-note.html', note=note, checked=checked)


@views.route('/delete/<noteid>')
def delete_note(noteid):
    note = Notes.query.get(noteid)
    if note.is_public:
        pnote = Public_Notes.query.filter_by(Id=noteid).first()
        db.session.delete(pnote)
        db.session.commit()
    db.session.delete(note)
    db.session.commit()

    return redirect(url_for('views.notes'))

@views.route('/public/<note_key>')
def public_note(note_key):
    public_note_ = Public_Notes.query.get(note_key)
    if public_note_:
        note = Notes.query.get(public_note_.Id)
        return render_template('note-public.html', note=note, note_key=note_key)
    else:
        # 404 Error
        pass
