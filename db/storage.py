import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from typing import Dict, Optional, Any
import os

from dotenv import load_dotenv
from imagekitio import ImageKit


class ImageStorage:
    """Class for uploading images to ImageKit."""

    def __init__(self) -> None:
        """Initialize ImageKit client from environment variables."""
        load_dotenv()
        self.private_key = os.getenv("IMAGEKIT_PRIVATE_KEY")
        self.client: Optional[ImageKit] = None

        if self.private_key:
            self.client = ImageKit(
                private_key=self.private_key,
            )
            print("[IMAGEKIT] ✓ ImageKit initialized successfully")
        else:
            print("[IMAGEKIT] ImageKit keys are missing. Image upload is disabled.")

    def upload_blog_image(self, image_data: Any, blog_id: str) -> str:
        """Upload a blog image to ImageKit and return its URL."""
        if not self.client:
            raise ValueError("ImageKit client is not initialized")

        print(f"[IMAGEKIT] Uploading image for blog '{blog_id}'")
        response = self.client.files.upload(
                file=image_data,
                file_name=f"blog_{blog_id}",
                folder="/blog_images",
            )

        image_url = response.url
        print(f"[IMAGEKIT] ✓ Image uploaded successfully: {image_url}")
        return image_url


class Database:
    """Database class for managing blog posts in Firestore."""
    
    def __init__(self) -> None:
        """ Initialize Firebase connection and Firestore client. """
        try:
            print("[DATABASE] Initializing Firebase connection...")
            self.image_storage = ImageStorage()

            # Get the path to the service account key relative to this script
            service_account_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
            cred = credentials.Certificate(service_account_path)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()

            print("[DATABASE] ✓ Connected to Firestore successfully!")
        except FileNotFoundError as e:
            print(f"[ERROR] Service account key not found: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Failed to initialize Firebase: {e}")
            raise
    
    def readAll(self) -> Dict[str, Dict[str, Any]]:
        """ Retrieve all blog posts from the database. """
        try:
            print("[READ_ALL] Fetching all blog posts...")

            blogs_ref = self.db.collection("Blog")
            docs = blogs_ref.stream()

            data: Dict[str, Dict[str, Any]] = dict()
            for doc in docs:
                data[doc.id] = doc.to_dict() #type: ignore
            
            print(f"[READ_ALL] ✓ Successfully retrieved {len(data)} blog(s)")

            return data
        except Exception as e:
            print(f"[ERROR] Failed to read all blogs: {e}")
            raise
    
    def readOne(self, blogId: str) -> Dict[str, Any]:
        """ Retrieve a single blog post by its ID. """
        try:
            print(f"[READ_ONE] Fetching blog with ID: {blogId}")

            doc_ref = self.db.collection("Blog").document(blogId)
            doc = doc_ref.get()
            
            if not doc.exists: #type: ignore
                raise ValueError(f"Blog with ID '{blogId}' not found")
            
            print(f"[READ_ONE] ✓ Successfully retrieved blog '{blogId}'")
            return doc.to_dict()  # type: ignore
        except ValueError as e:
            print(f"[ERROR] Value error: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Failed to read blog '{blogId}': {e}")
            raise
    
    def create(self, data: Dict[str, Any], image_data: Any) -> str:
        """ Create a new blog post in the database. """
        try:
            print(f"[CREATE] Creating new blog post: '{data['title']}'")
            update_time, doc_ref = self.db.collection("Blog").add(data)
            print(f"[CREATE] ✓ Blog post created successfully with ID: {doc_ref.id}")

            if image_data:
                try:
                    image_url = self.image_storage.upload_blog_image(image_data=image_data, blog_id=doc_ref.id)
                    self.edit(doc_ref.id, {"image_url": image_url})
                    print(f"[CREATE] ✓ Image URL saved to blog '{doc_ref.id}'")
                except Exception as image_error:
                    print(f"[CREATE] Image upload failed. Rolling back blog '{doc_ref.id}'")
                    self.delete(doc_ref.id)
                    raise RuntimeError(f"Failed to upload image: {image_error}") from image_error

            return doc_ref.id
        except ValueError as e:
            print(f"[ERROR] Validation error: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Failed to create blog post: {e}")
            raise
    
    def delete(self, blogId: str) -> None:
        """ Delete a blog post from the database. """
        try:
            print(f"[DELETE] Deleting blog post with ID: {blogId}")
            self.db.collection("Blog").document(blogId).delete()
            print(f"[DELETE] ✓ Blog post '{blogId}' deleted successfully")
        except Exception as e:
            print(f"[ERROR] Failed to delete blog '{blogId}': {e}")
            raise
    
    def edit(self, blogId: str, data: Dict[str, Any]) -> None:
        """ Update/edit an existing blog post in the database. """
        try:
            print(f"[EDIT] Updating blog post with ID: {blogId}")
            
            # Verify blog exists before updating
            doc_ref = self.db.collection("Blog").document(blogId)
            if not doc_ref.get().exists:
                raise ValueError(f"Blog with ID '{blogId}' not found")
            
            doc_ref.update(data)
            print(f"[EDIT] ✓ Blog post '{blogId}' updated successfully")
        except ValueError as e:
            print(f"[ERROR] Value error: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Failed to edit blog '{blogId}': {e}")
            raise


# Fake data for testing
FAKE_BLOGS = [
    {
        "title": "Getting Started with Python",
        "content": "Python is a powerful programming language that is easy to learn. In this post, we'll explore the basics of Python programming and how to set up your development environment.",
        "date_created": "05-04-2026",
    },
    {
        "title": "Building Web Applications with Flask",
        "content": "Flask is a lightweight web framework for Python. Learn how to create scalable web applications using Flask, including routing, templating, and database integration.",
        "date_created": "03-04-2026",
    },
    {
        "title": "Understanding Databases and Firestore",
        "content": "Firestore is a cloud-hosted NoSQL database. Discover how to structure your data, query collections, and optimize performance for real-time applications.",
        "date_created": "01-04-2026",
    },
    {
        "title": "Web Design Best Practices",
        "content": "Creating beautiful and functional web designs requires understanding user experience, accessibility, and responsive design principles. Let's dive into modern web design techniques.",
        "date_created": "28-03-2026",
    },
    {
        "title": "Mastering JavaScript for Frontend Development",
        "content": "JavaScript is the backbone of modern web development. Learn about ES6 features, async programming, and how to build interactive user interfaces with JavaScript.",
        "date_created": "25-03-2026",
    }
]


# if __name__ == "__main__":
#     print("\n" + "="*70)
#     print("BLOG DATABASE OPERATIONS DEMO")
#     print("="*70 + "\n")
    
#     db = Database()
#     created_ids: list[str] = []
    
#     try:
#         # ==================== CREATE OPERATIONS ====================
#         print("\n" + "-"*70)
#         print("1. CREATE OPERATIONS - Adding fake blog posts")
#         print("-"*70 + "\n")
        
#         for blog_data in FAKE_BLOGS:
#             try:
#                 blog_id = db.create(blog_data)
#                 created_ids.append(blog_id)
#             except Exception as e:
#                 print(f"[DEMO] Skipping blog creation due to: {e}\n")
        
#         # ==================== READ ALL OPERATIONS ====================
#         print("\n" + "-"*70)
#         print("2. READ ALL OPERATIONS - Fetching all blog posts")
#         print("-"*70 + "\n")
        
#         try:
#             all_blogs = db.readAll()
#             print(f"\n[DEMO] Total blogs in database: {len(all_blogs)}")
#             for blog_id, blog_data in list(all_blogs.items())[:3]:  # Show first 3
#                 print(f"  • {blog_data.get('title')} (ID: {blog_id})")
#         except Exception as e:
#             print(f"[DEMO] Error reading all blogs: {e}")
        
#         # ==================== READ ONE OPERATIONS ====================
#         print("\n" + "-"*70)
#         print("3. READ ONE OPERATIONS - Fetching specific blog post")
#         print("-"*70 + "\n")
        
#         if created_ids:
#             try:
#                 blog_data = db.readOne(created_ids[0])
#                 print(f"\n[DEMO] Blog Details:")
#                 print(f"  Title: {blog_data.get('title')}")
#                 print(f"  Content: {blog_data.get('content')[:100]}...")
#                 print(f"  Date Created: {blog_data.get('date_created')}")
#                 print(f"  Author: {blog_data.get('author')}")
#             except Exception as e:
#                 print(f"[DEMO] Error reading blog: {e}")
        
#         # ==================== EDIT OPERATIONS ====================
#         print("\n" + "-"*70)
#         print("4. EDIT OPERATIONS - Updating a blog post")
#         print("-"*70 + "\n")
        
#         if created_ids:
#             try:
#                 update_data = {
#                     "title": "Updated: Getting Started with Python (Advanced)",
#                     "content": "Updated content with more advanced topics...",
#                     "date_created": "06-04-2026"
#                 }
#                 db.edit(created_ids[0], update_data)
                
#                 # Verify the edit
#                 updated_blog = db.readOne(created_ids[0])
#                 print(f"\n[DEMO] Updated Blog:")
#                 print(f"  New Title: {updated_blog.get('title')}")
#                 print(f"  New Date: {updated_blog.get('date_created')}")
#             except Exception as e:
#                 print(f"[DEMO] Error editing blog: {e}")
        
#         # ==================== DELETE OPERATIONS ====================
#         print("\n" + "-"*70)
#         print("5. DELETE OPERATIONS - Removing a blog post")
#         print("-"*70 + "\n")
        
#         if len(created_ids) > 1:
#             try:
#                 db.delete(created_ids[-1])
#                 print(f"\n[DEMO] Blog post deleted from database")
#             except Exception as e:
#                 print(f"[DEMO] Error deleting blog: {e}")
        
#         # ==================== FINAL STATUS ====================
#         print("\n" + "-"*70)
#         print("6. FINAL STATUS - Verification")
#         print("-"*70 + "\n")
        
#         try:
#             final_blogs = db.readAll()
#             print(f"\n[DEMO] ✓ Final blog count in database: {len(final_blogs)}")
#         except Exception as e:
#             print(f"[DEMO] Error verifying final state: {e}")
        
#     except Exception as e:
#         print(f"\n[FATAL ERROR] Unexpected error in demo: {e}")
    
#     print("\n" + "="*70)
#     print("DEMO COMPLETED")
#     print("="*70 + "\n")
    