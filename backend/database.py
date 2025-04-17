from tinydb import TinyDB, Query
from datetime import datetime, timezone
import numpy as np

# Connect to TinyDB
db = TinyDB('db.json')
User = Query()

# ---------- User Management ----------

def add_user(user_data):
    """Add a new user to the database"""
    if db.search(User.email == user_data["email"]):
        print(f"User {user_data['email']} already exists in the database.")
        return {"message": "User already exists"}

    # Force string serialization for created_at
    user_data["created_at"] = user_data["created_at"].isoformat()
    result_id = db.insert(user_data)
    print(f"User {user_data['email']} added successfully with ID: {result_id}")
    return {"message": f"User {user_data['email']} added successfully"}

def get_users():
    """Retrieve all registered users"""
    users = db.search(User.username.exists())
    user_list = [{"username": user["username"]} for user in users]
    print(f"Retrieved {len(user_list)} users from the database.")
    return user_list

# ---------- Access Logging ----------

def log_access(username, success):
    """Log user access attempts"""
    log_entry = {
        "log_type": "access_log",
        "username": username,
        "success": bool(success),
        "timestamp": datetime.now(timezone.utc).isoformat()  # Fix: serialize datetime
    }
    db.insert(log_entry)
    print(f"Access log added for {username}")

def get_access_logs():
    """Retrieve access logs"""
    logs = db.search((User.log_type == "access_log"))
    log_list = [{
        "username": log["username"],
        "success": log["success"],
        "timestamp": log["timestamp"]
    } for log in logs]
    print(f"Retrieved {len(log_list)} access logs from the database.")
    return sorted(log_list, key=lambda x: x['timestamp'], reverse=True)  # Newest first

# ---------- Face Encoding Management ----------

def add_face_encoding(username, encoding):
    """Store a user's face encoding in the database"""
    try:
        db.insert({
            "data_type": "face_encoding",
            "username": username,
            "encoding": encoding.tolist()
        })
        print(f"Face encoding for {username} stored successfully.")
    except Exception as e:
        print(f"Error storing face encoding for {username}: {e}")

def get_face_encodings():
    """Retrieve all face encodings"""
    try:
        users = db.search(User.data_type == "face_encoding")
        face_data = [(user["username"], np.array(user["encoding"])) for user in users]
        print(f"Retrieved {len(face_data)} face encodings from the database.")
        return face_data
    except Exception as e:
        print(f"Error retrieving face encodings: {e}")
        return []

# ---------- DeepFace Embeddings ----------

def add_face_embedding(username, embedding):
    """Store a DeepFace facial embedding in the database"""
    try:
        db.insert({
            "data_type": "deepface_embedding",
            "username": username,
            "embedding": embedding.tolist()
        })
        print(f"DeepFace embedding for {username} stored successfully.")
    except Exception as e:
        print(f"Error storing DeepFace embedding for {username}: {e}")

def get_face_embeddings():
    """Retrieve all DeepFace face embeddings"""
    try:
        entries = db.search(User.data_type == "deepface_embedding")
        embedding_data = [(entry["username"], np.array(entry["embedding"])) for entry in entries]
        print(f"Retrieved {len(embedding_data)} DeepFace embeddings from the database.")
        return embedding_data
    except Exception as e:
        print(f"Error retrieving DeepFace embeddings: {e}")
        return []
