from flask import Flask,render_template
from db import db
from models.user import User
from models.post import Post
from utils import idGenerator
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():
    user = User.query.filter_by(name="Aarav Mehta",password="test1234").first()
    blogs = []
    for i in json.loads(user.blogId):
        temp = Post.query.filter_by(blogId=i).first()
        blogs.append(temp)
    
    return render_template('index.html',blogs = blogs)



# create the table
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)