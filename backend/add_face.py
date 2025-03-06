import face_recognition
import numpy as np
import os
from database import add_face_encoding  # Your existing database function

KNOWN_FACES_DIR = "data"  # Folder containing known faces

def store_face_encodings():
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                username = os.path.splitext(filename)[0]  # Remove file extension
                add_face_encoding(username, encodings[0])  # Store encoding in DB
                print(f"Face encoding stored for {username}")
            else:
                print(f"No face detected in {filename}")

if __name__ == "__main__":
    store_face_encodings()
