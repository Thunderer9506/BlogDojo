from flask import Flask
from db import db
from models.user import User
from models.post import Post
from utils.idGenerator import Password
from sqlalchemy.exc import SQLAlchemyError
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'  # use same or different DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    blog_posts = [
        {
            "blogid": 1,
            "title": "Why I Started Blogging as a Developer",
            "content": "Sharing my journey as a dev has helped me learn faster and connect with others.",
            "userId": 1  # Aarav Mehta
        },
        {
            "blogid": 2,
            "title": "5 Python Tricks That Will Save You Hours",
            "content": "These Python tips helped me write cleaner, faster code—especially during crunch time.",
            "userId": 2  # Sara Verma
        },
        {
            "blogid": 3,
            "title": "Debugging is a Superpower",
            "content": "Here’s how I approach bugs: treat them like puzzles, not problems.",
            "userId": 1  # Aarav Mehta
        },
        {
            "blogid": 4,
            "title": "Learning Flask From Scratch",
            "content": "I documented my Flask journey here so others can learn from my mistakes.",
            "userId": 3  # Dev Joshi
        },
        {
            "blogid": 5,
            "title": "How I Stay Productive as a Remote Dev",
            "content": "Simple routines, good music, and lots of tea keep me on track.",
            "userId": 5  # Rohit Sen
        },
        {
            "blogid": 6,
            "title": "What I Learned From My First Open Source PR",
            "content": "It was terrifying, exciting, and incredibly rewarding. Here’s what I learned.",
            "userId": 3  # Dev Joshi
        },
        {
            "blogid": 7,
            "title": "SQLAlchemy for Beginners",
            "content": "Understanding the ORM layer made databases feel much less scary.",
            "userId": 3  # Dev Joshi
        }
    ]


    try:
        for blog in blog_posts:

            temp = Post(
                title = blog["title"],
                content = blog["content"],
                userId = blog["userId"],
            )
            db.session.add(temp)
            db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e._message())
    