import json
import numpy as np
from database import add_face_encoding  # Import database function
import os

LOCAL_STORAGE_FILE = "face_encodings.json"  # Local file for encodings

def store_encodings():
    """Stores locally saved face encodings into MongoDB if available"""
    
    # Check if local encodings exist
    if not os.path.exists(LOCAL_STORAGE_FILE):
        print(f"No local encodings found in {LOCAL_STORAGE_FILE}. Run `add_face.py` first.")
        return
    
    # Load local face encodings
    with open(LOCAL_STORAGE_FILE, "r") as f:
        face_data = json.load(f)

    if not face_data:
        print("No valid face encodings found. Make sure images contain faces.")
        return

    # Try storing in MongoDB
    for username, encoding in face_data.items():
        try:
            add_face_encoding(username, np.array(encoding))  # Convert list back to NumPy array
            print(f"Stored {username}'s face encoding in MongoDB")
        except Exception as e:
            print(f"Failed to store {username}'s encoding in MongoDB: {e}")

if __name__ == "__main__":
    store_encodings()
