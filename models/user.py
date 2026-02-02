from db import db
from datetime import datetime,timezone

class User(db.Model):
    userId = db.Column(db.String(), primary_key=True)
    profile_pic = db.Column(db.String(),default="")
    name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime,default=datetime.now(timezone.utc))