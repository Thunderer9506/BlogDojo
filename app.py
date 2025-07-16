from flask import *
from sqlalchemy.exc import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

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
migrate = Migrate(app, db)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def initialRoute():
    return redirect(url_for('login',userId = session['user_id']))

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
            return redirect(url_for('home',userId=user.userId))  
        except IntegrityError as e:
            print(e)
            db.session.rollback()
    return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home',userId = session['user_id']))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.userId
            session['user_email'] = user.email
            return redirect(url_for('home', userId=user.userId))
        else:
            
            return render_template('login.html', error='Credentials are invalid')
    
    return render_template('login.html')



@app.route('/<string:userId>/')
@login_required
def home(userId):
    post = Post.query.all()
    user = User.query.all()
    return render_template('index.html',posts=post,users=user,userId=userId)

@app.route('/image/<string:post_id>')
@login_required
def get_post_image(post_id):
    post = Post.query.get_or_404(post_id)
    if post.image_data:
        return Response(post.image_data, mimetype=post.image_mime)
    else:
        return "No image", 404
    

@app.route('/insert/<string:userId>',methods=['GET','POST'])
@login_required
def insert(userId):
    if request.method == 'POST':
        image = request.files['image']
        image_data = image.read()            
        image_mime = image.content_type      
        title = request.form.get('title')
        content = request.form.get('content')
        postId = str(uuid.uuid4())
        post = Post(blogId = postId,title=title,content=content,userId = userId,image_data=image_data,
                    image_mime=image_mime)
        db.session.add(post)    
        db.session.commit()
        return redirect(url_for('home',userId=userId))
    return render_template('newPost.html',userId=userId)

@app.route('/user/<string:userId>')
@login_required
def profile(userId):
    user = User.query.filter_by(userId = userId).all()
    post = Post.query.filter_by(userId = userId).all()

    return render_template('profile.html',user=user,posts=post,userId=userId)

@app.route('/post/<string:blogId>')
@login_required
def viewPost(blogId):
    post = Post.query.filter_by(blogId=blogId).first()
    user = User.query.filter_by(userId=post.userId).first()
    return render_template('post.html',post = post,user = user,currentUser = session['user_id'])

@app.route('/delete/<string:blogId>')
@login_required
def deletePost(blogId):
    post = Post.query.filter_by(blogId=blogId).first()
    user = User.query.filter_by(userId=post.userId).first()
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('profile',userId=user.userId))

@app.route('/edit/<string:blogId>',methods=['GET','POST'])
@login_required
def editPost(blogId):
    post = Post.query.filter_by(blogId=blogId).first()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post.title = title
        post.content = content
        db.session.commit()
        return redirect(url_for('profile',userId=post.userId))
        
    return render_template('edit.html',post=post)


@app.template_filter('sliceDate')
def slice_date(s):
    return s.strftime("%d-%m-%Y")


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # fallback to 5000 if PORT not set
    app.run(host="0.0.0.0", port=port)
