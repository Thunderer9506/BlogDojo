
# 🧘‍♂️ BlogDojo

BlogDojo is a simple yet elegant blog web application built with **Flask**, **Firestore**, and **ImageKit**. Designed as a personal learning project, BlogDojo lets the admin create, edit, and view rich-text blog posts using a Quill-powered editor. Visitors can browse and read all published posts. This project is open-source and will continue evolving as more features are added.

---

## 🚀 Live Demo

🔗 Live Website: [https://blogdojo.onrender.com](https://blogdojo.onrender.com)

---

## 🧠 Overview

BlogDojo focuses on enhancing practical full-stack development skills using:

- 🧱 Flask for backend & routing
- 🗄️ Firestore for cloud database
- ✍️ QuillJS for rich blog editing
- 📷 Image uploading via ImageKit
- 🔐 Session-based admin login
- 🌗 Theme toggling (light/dark)

---

## ✨ Features

### Current Features
- 📝 **Rich Blog Creation** using Quill (Admin only)
- 🖼️ **Image Upload** support via ImageKit (Admin only)
- 🔒 **Admin Authentication** - Single admin account with session-based login
- 🗃️ **View All Blogs** on Home Page (Public)
- 🛠️ **Edit/Delete Posts** (Admin only)
- 🎨 **Light/Dark Mode** (stored in `localStorage`)
- ✅ Password hashing with Werkzeug

### Previous Features (Removed)
- ❌ Public sign-up (now single admin account only)
- ❌ Profile page for users (removed as only admin can post)
- ❌ SQLite database (migrated to Firestore)

---

## 🛠️ Tech Stack

| Layer        | Tech                           |
|--------------|--------------------------------|
| Backend      | Python, Flask                  |
| Database     | Firestore (Firebase)           |
| Image Storage| ImageKit                       |
| Frontend     | HTML, CSS, JS, QuillJS         |
| Auth         | werkzeug + Sessions            |
| Deployment   | Render.com                     |

---

## 📦 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/Thunderer9506/blogdojo.git
cd blogdojo
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## ⚙️ Running Locally

```bash
flask run
```

Visit [http://localhost:5000](http://localhost:5000)

---

## 🔐 Environment Variables

Create a `.env` or set them in your OS/Render:

| Variable                         | Purpose                      |
|----------------------------------|------------------------------|
| `SECRET_KEY`                     | Session encryption           |
| `SERVICE_ACCOUNT_KEY_PATH`       | Firebase service account JSON|
| `IMAGEKIT_PRIVATE_KEY`           | ImageKit upload authentication|
| `PORT`                           | Port for deployment (optional)|

---

## 📁 Folder Structure

```
blogdojo/
│
├── app.py                    # Main Flask app, routes, admin auth
├── db/
│   └── storage.py            # Firestore Database + ImageKit ImageStorage
├── templates/                # Jinja2 HTML templates
│   ├── macros/               # Reusable template components
│   ├── base.html             # Base template
│   ├── index.html            # Home page (all posts)
│   ├── post.html             # Single post view
│   ├── login.html            # Admin login
│   ├── newPost.html          # Create post (admin)
│   └── edit.html             # Edit post (admin)
├── static/                   # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── assets/
├── requirements.txt          # Python dependencies
└── README.md                 # You're here
```

---


## 🛡️ Security Practices

- 🔐 Passwords are **hashed** using `werkzeug.security`
- 📁 File uploads are validated and stored in ImageKit cloud storage
- 🛡️ Jinja2 templates use the `|safe` filter **only** after HTML sanitization
- 🔒 Admin-only routes protected with `@admin_required` decorator

---

## 🤝 Contributing

Want to improve BlogDojo? Fork the repo and submit a PR!

```bash
git clone https://github.com/your-username/blogdojo.git
git checkout -b new-feature
```

Open a pull request with clear changes.

---

## 📜 License

MIT License © 2025 [Shaurya Srivastava]

---
