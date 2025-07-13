from flask import *
from flask_ckeditor import CKEditor, CKEditorField
from sqlalchemy.exc import *
import bleach
from flask_wtf import FlaskForm
from wtforms import SubmitField
from db import db
from models.user import User
from models.post import Post
from utils import idGenerator
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.secret_key = 'secret'
db.init_app(app)
ckeditor = CKEditor(app)

class PostForm(FlaskForm):
    content = CKEditorField('Content')
    submit = SubmitField('Post')

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
            user = User(name=name, username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.userId
            session['user_email'] = user.email
            session['user_password'] = user.password
            return redirect(url_for('home',id=user.userId))  # PRG pattern
        except IntegrityError as e:
            print(e)
            db.session.rollback()
    return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home',id=session['user_id']))
    else:
        if request.method == 'POST':
            try:
                email = request.form.get('email')
                password = request.form.get('password')
                user = User.query.filter_by(email=email, password=password).first()
                session['user_id'] = user.userId
                session['user_email'] = user.email
                session['user_password'] = user.password
                if user:
                    return redirect(url_for('home', id=user.userId))
                else:
                    return render_template('login.html', error="Invalid login")
            except:
                return redirect(url_for('login', error="Something went bad"))
    return render_template('login.html')


@app.route('/<int:userId>')
def home(userId):
    user = User.query.filter_by(userId = userId).first()
    blogs = []
    for i in json.loads(user.blogId):
        temp = Post.query.filter_by(blogId=i).first()
        blogs.append(temp)
    
    return render_template('index.html',blogs = blogs,id=user.userId)


@app.route('/<int:userId>/insert',methods=['GET','POST'])
def insert(userId):
    form = PostForm()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        # You can now store this in a database or print
        print(f"Title: {title}, Content: {content}")

    
    return render_template('newPost.html',id=userId,form=form)

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
