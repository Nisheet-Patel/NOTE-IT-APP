from website import db
from . import Public_Notes
from secrets import token_urlsafe 
import datetime
__PUBLIC_NOTE_KEY__ = 20

class Notes(db.Model):
    __searchable__ = ['title', 'body']
    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    is_public = db.Column(db.Integer, nullable=False)
    update_date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    public = db.relationship('Public_Notes', backref='note')

    @staticmethod
    def All(user_id):
        # return all notes with public slug of given user_id
        PUBLIC_NOTES = Public_Notes.Public_Notes # to avoid circular imports
        notes = db.session.query(Notes,PUBLIC_NOTES).join(PUBLIC_NOTES, PUBLIC_NOTES.Id == Notes.note_id, isouter=True).filter(Notes.user_id == user_id)

        return notes
    
    @staticmethod
    def Get(note_id):
        return Notes.query.get(note_id)
    
    @staticmethod
    def Search(search_value):
        PUBLIC_NOTES = Public_Notes.Public_Notes
        db.session.query(Notes,PUBLIC_NOTES).join(PUBLIC_NOTES, PUBLIC_NOTES.Id == Notes.note_id, isouter=True).filter(Notes.user_id == current_user.id).filter(Notes.title.contains(search_value) | Notes.body.contains(search_value)).order_by(Notes.update_date.desc())

    @staticmethod
    def Add(title, body, is_public, user_id):
        PUBLIC_NOTES = Public_Notes.Public_Notes
        note = Notes(
            title = title,
            body = body,
            is_public = is_public,
            update_date = datetime.datetime.now().strftime("%d %m %Y %X"),
            user_id = user_id
        )
        db.session.add(note)
        db.session.commit()

        if is_public:
            pnote = PUBLIC_NOTES(Id=note.note_id, slug=token_urlsafe(__PUBLIC_NOTE_KEY__))
            db.session.add(pnote)
            db.session.commit()

    @staticmethod
    def Edit(note_id, title, body, is_public, user_id):
        PUBLIC_NOTES = Public_Notes.Public_Notes

        note = Notes.Get(note_id)
        if note.user_id == user_id:
            if is_public != note.is_public:
                # Add
                if is_public:
                    pnote = PUBLIC_NOTES(Id=note.note_id, slug=token_urlsafe(__PUBLIC_NOTE_KEY__))
                    db.session.add(pnote)
                    db.session.commit()
                else:
                    # remove
                    pnote = PUBLIC_NOTES.query.filter_by(Id=note_id).first()
                    db.session.delete(pnote)
                    db.session.commit()

            note.title = title
            note.body = body
            note.is_public = is_public
            update_date = datetime.datetime.now().strftime("%d %m %Y %X")

            db.session.commit()

            return note
        return False
    
    def Delete(note_id, user_id):
        PUBLIC_NOTES = Public_Notes.Public_Notes
        note = Notes.Get(note_id)
        if note.user_id == user_id:
            if note.is_public:
                pnote = PUBLIC_NOTES.query.filter_by(Id=note_id).first()
                db.session.delete(pnote)
                db.session.commit()
            db.session.delete(note)
            db.session.commit()
            return True
        return False
