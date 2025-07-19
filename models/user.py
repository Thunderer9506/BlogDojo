from db import db
from datetime import datetime,timezone

class User(db.Model):
    userId = db.Column(db.String(100), primary_key=True)
    profile_pic = db.Column(db.String(150),default="",unique=True)
    name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime,default=datetime.now(timezone.utc))