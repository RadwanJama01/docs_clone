from app import db
from datetime import datetime

note_collaborators = db.Table(
    'note_collaborators',                   
    db.Column('note_id',db.Integer,db.ForeignKey('note.id')),
    db.Column('user_id',db.Integer,db.ForeignKey('user.id'))
)

class Note(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(128))
    #created_at = db.Column(db.DateTime,default = datetime.utcnow,nullable = False)
    #updated_at = db.Column(db.DateTime,default = datetime.utcnow, onupdate = datetime.utcnow,  nullable = False)
    content = db.Column(db.Text)
    
    created_at = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        nullable = False
    )
    updated_at = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        onupdate = datetime.utcnow,
        nullable = False
    )
    
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id')) #ForeignKey points to another table in our db
    owner = db.relationship('User',backref ='owned_notes')
    
    collaborators = db.relationship('User',secondary = note_collaborators, backref = 'collaborations')
    
    
    
    
        
    