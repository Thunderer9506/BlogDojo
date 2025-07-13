from flask import Flask
from db import db
from models.user import User
from models.post import Post
from utils.idGenerator import Password
from sqlalchemy.exc import SQLAlchemyError
import json
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'  # use same or different DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    users = [
        {
            "name": "Aarav Mehta",
            "username": "aaravm",
            "email": "aarav.mehta@example.com",
            "password": "test1234",
            "blog_ids": [1, 3]
        },
        {
            "name": "Sara Verma",
            "username": "sverma",
            "email": "sara.verma@example.com",
            "password": "securepass",
            "blog_ids": [2]
        },
        {
            "name": "Dev Joshi",
            "username": "devj",
            "email": "dev.joshi@example.com",
            "password": "myblogpass",
            "blog_ids": [4, 6, 7]
        },
        {
            "name": "Nisha Kapoor",
            "username": "nkapoor",
            "email": "nisha.kapoor@example.com",
            "password": "hello123",
            "blog_ids": []
        },
        {
            "name": "Rohit Sen",
            "username": "rohits",
            "email": "rohit.sen@example.com",
            "password": "admin321",
            "blog_ids": [5]
        }
    ]

    try:
        # post = Post(blogId=4,title="Learning Flask From Scratch",
        #                             content = "I documented my Flask journey here so others can learn from my mistakes.",
        #                             userId = 3)
        # db.session.add(post)
        # db.session.commit()
        print(str(uuid.uuid4()))
        # for user in users:
        #     print(user['name'],
        #         user['username'],
        #         user['email'],
        #         user['password'],
        #         user['blog_ids'])
        #     temp = User(name = user['name'],
        #                 username = user['username'],
        #                 email = user['email'],
        #                 password = user['password'],
        #                 blogId = json.dumps(user['blog_ids']))
        #     db.session.add(temp)
        #     db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e._message())
    