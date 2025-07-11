from db import db
from datetime import datetime,timezone

class Post(db.Model):
    blogId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300),nullable=False)
    content = db.Column(db.Text, nullable=False,unique=True)
    userId = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime,default=datetime.now(timezone.utc))
