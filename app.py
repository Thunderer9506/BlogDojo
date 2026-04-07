from flask import *
from sqlalchemy.exc import *
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models.user import User
from models.post import Post
from utils import pfp
from functools import wraps

import uuid
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

app.secret_key = os.getenv('SECRET_KEY')
db.init_app(app)

@app.route('/')
def home():
    post = Post.query.all()
    user = User.query.all()
    return render_template('index.html',posts=post,users=user,userId=session['user_id'])

@app.route('/image/<string:post_id>')
def get_post_image(post_id):
    post = Post.query.get_or_404(post_id)
    if post.image_data:
        return Response(post.image_data, mimetype=post.image_mime)
    else:
        return "No image", 404
    

@app.route('/post/<string:blogId>')
def viewPost(blogId):
    post = Post.query.filter_by(blogId=blogId).first()
    user = User.query.filter_by(userId=post.userId).first()
    return render_template('post.html',post = post,user = user,currentUser = session['user_id'])


@app.template_filter('sliceDate')
def slice_date(s):
    return s.strftime("%d-%m-%Y")

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # fallback to 5000 if PORT not set
    app.run(host="0.0.0.0", port=port, debug=True)
