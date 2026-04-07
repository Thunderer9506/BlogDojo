# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BlogDojo is a Flask-based blog application with Firestore database and ImageKit for image storage. It supports user authentication (single admin account), rich-text blog creation with QuillJS, image uploads, and CRUD operations.

## Commands

```bash
# Run locally
flask run

# Production (Render.com)
gunicorn app:app

# Install dependencies
pip install -r requirements.txt
# or with uv
uv sync
```

## Architecture

```
blogdojo/
├── app.py              # Flask app, routes, admin auth decorator
├── db/storage.py       # Firestore Database class + ImageKit ImageStorage class
├── templates/          # Jinja2 templates (base.html, index.html, post.html, etc.)
├── static/             # CSS, JS, assets
└── .env                # Environment variables (SECRET_KEY, Firebase credentials, ImageKit keys)
```

**Key components:**
- `app.py`: Main Flask application with routes for login/logout, home, create/edit/delete/view posts. Uses `@admin_required` decorator for protected routes.
- `db/storage.py`: 
  - `Database` class: CRUD operations for blog posts in Firestore (collection: "Blog")
  - `ImageStorage` class: Handles image uploads to ImageKit under `/blog_images` folder
- Authentication: Single admin account stored in Firestore document "credentials" with email/password (password hashed with werkzeug)

## Environment Variables

Required in `.env`:
- `SECRET_KEY` - Session encryption
- `SERVICE_ACCOUNT_KEY_PATH` - Firebase service account JSON
- `IMAGEKIT_PRIVATE_KEY` - ImageKit upload key
- `PORT` - Optional, for deployment

## Deployment

Deployed on Render.com as a web service (see `render.yaml`). Uses Gunicorn for production.
