from db import db
from datetime import datetime,timezone

class Post(db.Model):
    blogId = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String(),nullable=False)
    content = db.Column(db.Text, nullable=False,unique=True)
    userId = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime,default=datetime.now(timezone.utc))
    image_data = db.Column(db.LargeBinary)  # Store image binary data
    image_mime = db.Column(db.String(50))   # Optional: store content-type like "image/jpeg"
