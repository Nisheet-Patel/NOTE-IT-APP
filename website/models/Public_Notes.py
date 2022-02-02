from website import db
from . import Notes


class Public_Notes(db.Model):
    __tablename__ = "public_notes"
    Id =  db.Column(db.Integer, db.ForeignKey('notes.note_id'))
    slug = db.Column(db.String(16), primary_key=True)

    @staticmethod
    def Get_Slug(note_id):
        # return public slug of given note_id
        slug = Public_Notes.query.filter_by(Id=note_id).first().slug
        return slug

    @staticmethod
    def All(user_id):
        # return all public notes with public slug of given user_id
        NOTES = Notes.Notes
        notes = db.session.query(NOTES,Public_Notes).join(Public_Notes, Public_Notes.Id == NOTES.note_id).filter(NOTES.user_id == user_id)

        return notes