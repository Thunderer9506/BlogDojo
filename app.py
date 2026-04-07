from flask import *
from werkzeug.security import check_password_hash
from db.storage import Database
from functools import wraps
from dotenv import load_dotenv
from datetime import datetime
from typing import Any, Dict, List
import os
import tempfile

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

db = Database()


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_admin_credentials() -> Dict[str, Any]:
    """Fetch admin credentials from Firestore doc id 'credentials'."""
    try:
        return db.readOne('credentials')
    except Exception as e:
        print(f"[AUTH] Could not read admin credentials: {e}")
        return {}


def normalize_posts(posts_map: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert Firestore map response into template-ready post list."""
    posts: List[Dict[str, Any]] = []
    for blog_id, data in posts_map.items():
        if blog_id == 'credentials':
            continue

        post_data = dict(data)
        post_data['blogId'] = blog_id
        if 'date' not in post_data and 'date_created' in post_data:
            post_data['date'] = post_data['date_created']
        posts.append(post_data)

    posts.sort(key=lambda x: x.get('date_created', ''), reverse=True)
    return posts


@app.context_processor
def inject_auth_state() -> Dict[str, bool]:
    return {'is_admin': bool(session.get('is_admin', False))}


@app.route('/')
def initialRoute():
    return redirect(url_for('home'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('is_admin'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_admin_credentials()
        stored_email = user.get('email')
        stored_password = user.get('password')
        if user and email == stored_email and check_password_hash(stored_password, password):
            session['is_admin'] = True
            return redirect(url_for('home'))
        return render_template('login.html', error='Credentials are invalid')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('home'))


@app.route('/signup')
def signup():
    # Only one admin account is supported in this application.
    return render_template('login.html', error='Sign up is disabled. Please contact admin.')


@app.route('/home')
def home():
    posts_map = db.readAll()
    posts = normalize_posts(posts_map)
    return render_template(
        'index.html',
        posts=posts,
    )
    
@app.route('/insert',methods=['GET','POST'])
@admin_required
def insert():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            return render_template('newPost.html', error='Title and content are required')

        post_data = {
            'title': title,
            'content': content,
            'date_created': datetime.now().strftime('%d-%m-%Y'),
        }

        image = request.files.get('image')

        try:

            db.create(post_data, image_data=image.read())
            return redirect(url_for('home'))
        except Exception as e:
            print(f"[ERROR] Failed to create blog post: {e}")

    return render_template('newPost.html')

@app.route('/post/<string:blogId>')
def viewPost(blogId):
    try:
        post = db.readOne(blogId)
    except ValueError:
        abort(404)

    post['blogId'] = blogId
    if 'date' not in post and 'date_created' in post:
        post['date'] = post['date_created']

    return render_template('post.html', post=post)


@app.route('/post-image/<string:post_id>')
def get_post_image(post_id):
    try:
        post = db.readOne(post_id)
    except Exception:
        abort(404)

    image_url = post.get('image_url')
    if image_url:
        return redirect(image_url)

    return redirect(url_for('static', filename='assets/demo.png'))

@app.route('/delete/<string:blogId>')
@admin_required
def deletePost(blogId):
    db.delete(blogId)
    return redirect(url_for('home'))

@app.route('/edit/<string:blogId>',methods=['GET','POST'])
@admin_required
def editPost(blogId):
    try:
        post = db.readOne(blogId)
    except ValueError:
        abort(404)

    post['blogId'] = blogId

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        update_data: Dict[str, Any] = {}

        if title:
            update_data['title'] = title
        if content:
            update_data['content'] = content

        image = request.files.get('image')
        temp_file_path = None

        try:
            if image and image.filename:
                suffix = os.path.splitext(image.filename)[1] or '.jpg'
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    image.save(tmp)
                    temp_file_path = tmp.name

                image_url = db.image_storage.upload_blog_image(temp_file_path, blogId)
                update_data['image_url'] = image_url

            if update_data:
                db.edit(blogId, update_data)
            return redirect(url_for('viewPost', blogId=blogId))
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        
    return render_template('edit.html', post=post)


@app.template_filter('sliceDate')
def slice_date(s):
    if hasattr(s, 'strftime'):
        return s.strftime("%d-%m-%Y")
    return str(s)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # fallback to 5000 if PORT not set
    app.run(host="0.0.0.0", port=port, debug=True)
