from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from .models import Notes, Public_Notes
from . import db

views = Blueprint('views',__name__)
__PUBLIC_NOTE_KEY__ = 20

Notes = Notes.Notes
Public_Notes = Public_Notes.Public_Notes

@views.route('/')
def home():
    return render_template('index.html')
    
    
@views.route('/notes')
def notes():
    if not current_user.is_authenticated:
        flash("login to view Notes", "info")
        return redirect(url_for("auth.login_page"))

    search_value = request.args.get('search-value')
    if search_value:
        notes = Notes.Search(search_value)
        return render_template('main-page.html', notes=notes, search_value=search_value)

    notes = Notes.All(current_user.id)

    return render_template('main-page.html', notes=notes)

@views.route('/shared')
def shared():
    if not current_user.is_authenticated:
        flash("login to view Notes", "info")
        return redirect(url_for("auth.login_page"))

    notes = Public_Notes.All(current_user.id)

    return render_template('main-page.html', notes=notes, for_shared=True)

@views.route('/notes/<noteid>')
def note(noteid):
    if not current_user.is_authenticated:
        flash("login to view Notes", "info")
        return redirect(url_for("auth.login_page"))

    note = Notes.query.get(noteid)
    if note.user_id == current_user.id:
        if note.is_public:
            public_note_ = Public_Notes.Get_Slug(noteid)
        else:
            public_note_ = None
        return render_template('note-private.html',note=note, note_key=public_note_)
    else:
        return abort(404)

@views.route('/add-note', methods=['GET', 'POST'])
@login_required
def add_note_page():
    if request.method == 'POST':

        is_public = 1 if request.form.get('is-public') == 'on' else 0

        Notes.Add(
            request.form.get('note-title'),
            request.form.get('note-body'),
            is_public,
            current_user.id
        )

        return redirect(url_for('views.notes'))
    else:
        return render_template('add-note.html')

@views.route('/edit-note/<noteid>', methods=['GET','POST'])
@login_required
def edit_page_page(noteid):
    if request.method == 'POST':
        is_public = 1 if request.form.get('is-public') == 'on' else 0

        note = Notes.Edit(
            noteid, 
            request.form.get('note-title'), request.form.get('note-body'), 
            is_public, 
            current_user.id
            )

        if note:
            return redirect(url_for('views.notes') + f'/{note.note_id}')
        else:
            return abort(401)
    else:
        note = Notes.Get(noteid)
        if note.user_id == current_user.id:
            checked = "checked" if note.is_public else "unchecked"
            return render_template('edit-note.html', note=note, checked=checked)
        else:
            return abort(404)

@views.route('/delete/<noteid>')
@login_required
def delete_note(noteid):
    note = Notes.Delete(noteid, current_user.id)
    if note:
        return redirect(url_for('views.notes'))
    else:
        return abort(404)

@views.route('/public/<note_key>')
def public_note(note_key):
    public_note_ = Public_Notes.query.get(note_key)
    if public_note_:
        note = Notes.query.get(public_note_.Id)
        return render_template('note-public.html', note=note, note_key=note_key)
    else:
        return abort(404)

@views.route('/about')
def about():
    return render_template('about-page.html')