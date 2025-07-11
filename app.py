from flask import Flask
from db import db
from models.user import User
from models.post import Post
from utils import idGenerator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():
    return "Hello world"



# create the table
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)