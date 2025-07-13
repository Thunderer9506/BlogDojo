from flask import *
from sqlalchemy.exc import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from db import db
from models.user import User
from models.post import Post
from utils import pfp

import json
import uuid
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'secret'
db.init_app(app)

@app.route('/')
def initialRoute():
    return redirect(url_for('login'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            userId = str(uuid.uuid4())
            user = User(userId=userId,name=name, username=username, email=email, password=hashed_password,
                        profile_pic=pfp.generate_random_pfp(userId))
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.userId
            session['user_email'] = user.email
            session['user_password'] = user.password
            return redirect(url_for('home',userId=user.userId))  # PRG pattern
        except IntegrityError as e:
            print(e)
            db.session.rollback()
    return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.userId
            session['user_email'] = user.email
            return redirect(url_for('home', userId=user.userId))
        else:
            # 🔥 Redirecting with error message in URL
            return render_template('login.html', error='Credentials are invalid')

    # ✅ Extract the error if present from query parameters
    # error = request.args.get('error')
    return render_template('login.html')



@app.route('/<string:userId>')
def home(userId):
    post = Post.query.all()
    return render_template('index.html',post=post)

@app.route('/image/<string:post_id>')
def get_post_image(post_id):
    post = Post.query.get_or_404(post_id)
    if post.image_data:
        return Response(post.image_data, mimetype=post.image_mime)
    else:
        return "No image", 404

@app.route('/insert/<string:userId>',methods=['GET','POST'])
def insert(userId):
    if request.method == 'POST':
        image = request.files['image']
        image_data = image.read()            # Read image bytes
        image_mime = image.content_type      # Store content-type
        title = request.form.get('title')
        content = request.form.get('content')
        postId = str(uuid.uuid4())
        post = Post(blogId = postId,title=title,content=content,userId = userId,image_data=image_data,
                    image_mime=image_mime)
        db.session.add(post)    
        db.session.commit()
        return render_template('userPost.html',post=post)
    return render_template('newPost.html',userId=userId)

@app.route('/delete/<int:blogId>')
def deletePost(blogId):
    post = Post.query.filter_by(blogId=blogId).first()
    user = User.query.filter_by(userId=post.userId).first()
    userPosts = json.loads(user.blogId)
    userPosts.remove(blogId)
    user.blogId = json.dumps(userPosts)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('home',id=post.userId))

@app.route('/edit/<int:blogId>',methods=['GET','POST'])
def editPost(blogId):
    post = Post.query.filter_by(blogId=blogId).first()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post.title = title
        post.content = content
        db.session.commit()
        return redirect(url_for('home',id=post.userId))
    
    return render_template('edit.html',post=post)

@app.route('/view/<int:blogId>')
def viewPost(blogId):
    post = Post.query.filter_by(blogId=blogId).first()
    user = User.query.filter_by(userId=post.userId).first()
    return render_template('post.html',post = post,user = user.name)

# create the table
with app.app_context():
    db.create_all()
