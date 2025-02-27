from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB (Replace 'localhost' with your MongoDB server address if needed)
client = MongoClient("mongodb://localhost:27017/")
db = client.smart_lock

def add_user(user_data):
    """Add a new user to the database"""
    if db.users.find_one({"email": user_data["email"]}):
        return {"message": "User already exists"}

    db.users.insert_one(user_data)
    return {"message": f"User {user_data['email']} added successfully"}


def get_users():
    """Retrieve all registered users"""
    return list(db.users.find({}, {"_id": 0, "username": 1}))

def log_access(username, success):
    """Log user access attempts"""
    log_entry = {
        "username": username,
        "success": success,
        "timestamp": datetime.now()
    }
    db.access_logs.insert_one(log_entry)

def get_access_logs():
    """Retrieve access logs"""
    return list(db.access_logs.find({}, {"_id": 0, "username": 1, "success": 1, "timestamp": 1}))

def add_face_encoding(username, encoding):
    """Store a user's face encoding in the database"""
    db.faces.insert_one({"username": username, "encoding": encoding.tolist()})

def get_face_encodings():
    """Retrieve all face encodings"""
    users = db.faces.find({})
    return [(user["username"], np.array(user["encoding"])) for user in users]

