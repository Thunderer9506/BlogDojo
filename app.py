from flask import Flask,render_template,redirect,url_for,request
from flask_ckeditor import CKEditor, CKEditorField
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

@app.route('/1')
def home():
    user = User.query.filter_by(userId = 1).first()
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
        content = bleach.clean(request.form.get('content'))
        # You can now store this in a database or print
        print(f"Title: {title}, Content: {content}")
        
    
    return render_template('newPost.html',id=userId,form=form)

# create the table
with app.app_context():
    db.create_all()
