from pymongo import MongoClient
import numpy as np
from datetime import datetime, timezone


# Connect to MongoDB (Replace 'localhost' with your MongoDB server address if needed)
client = MongoClient("mongodb://localhost:27017/")
db = client.smart_lock

def add_user(user_data):
    """Add a new user to the database"""
    if db.users.find_one({"email": user_data["email"]}):
        print(f"User {user_data['email']} already exists in the database.")
        return {"message": "User already exists"}

    result = db.users.insert_one(user_data)
    print(f"User {user_data['email']} added successfully with ID: {result.inserted_id}")
    return {"message": f"User {user_data['email']} added successfully"}

def get_users():
    """Retrieve all registered users"""
    users = list(db.users.find({}, {"_id": 0, "username": 1}))
    print(f"Retrieved {len(users)} users from the database.")
    return users

def log_access(username, success):
    """Log user access attempts"""
    log_entry = {
        "username": username,
        "success": bool(success),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    result = db.access_logs.insert_one(log_entry)  # ✅ FIX: assign result
    print(f"Access log added for {username} with ID: {result.inserted_id}")


def get_access_logs():
    """Retrieve access logs"""
    logs = list(db.access_logs.find({}, {"_id": 0, "username": 1, "success": 1, "timestamp": 1}))
    print(f"Retrieved {len(logs)} access logs from the database.")
    return logs

def add_face_encoding(username, encoding):
    """Store a user's face encoding in the database"""
    try:
        result = db.faces.insert_one({"username": username, "encoding": encoding.tolist()})
        print(f"Face encoding for {username} stored successfully with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error storing face encoding for {username}: {e}")

def get_face_encodings():
    """Retrieve all face encodings"""
    try:
        users = db.faces.find({})
        face_data = [(user["username"], np.array(user["encoding"])) for user in users]
        print(f"Retrieved {len(face_data)} face encodings from the database.")
        return face_data
    except Exception as e:
        print(f"Error retrieving face encodings: {e}")
        return []
def add_face_embedding(username, embedding):
    """Store a DeepFace facial embedding in the database"""
    try:
        result = db.deepface_faces.insert_one({
            "username": username,
            "embedding": embedding.tolist()
        })
        print(f"DeepFace embedding for {username} stored with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error storing DeepFace embedding for {username}: {e}")

def get_face_embeddings():
    """Retrieve all DeepFace face embeddings"""
    try:
        entries = db.deepface_faces.find({})
        return [(entry["username"], np.array(entry["embedding"])) for entry in entries]
    except Exception as e:
        print(f"Error retrieving DeepFace embeddings: {e}")
        return []
