import face_recognition
import numpy as np
import os
import json

KNOWN_FACES_DIR = "data"  # Folder containing known faces
LOCAL_STORAGE_FILE = "face_encodings.json"  # Temporary local file

def store_face_encodings():
    face_data = {}

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):

            image_path = os.path.join(KNOWN_FACES_DIR, filename)
            print(f"Processing {filename}...")  # Debugging print
            image = face_recognition.load_image_file(image_path)

            # Get face encodings
            encodings = face_recognition.face_encodings(image)

            if encodings:
                username = os.path.splitext(filename)[0]  # Remove file extension
                face_data[username] = encodings[0].tolist()  # Convert to list for JSON
                
                print(f"Face encoding stored for {username}")  # Debugging print
                print(f"Encoding length: {len(encodings[0])}")  # Check the vector size
            else:
                print(f"No face detected in {filename}")

    # Save locally only if faces were found
    if face_data:
        with open(LOCAL_STORAGE_FILE, "w") as f:
            json.dump(face_data, f)
        print(f"Encodings saved locally in {LOCAL_STORAGE_FILE}")
    else:
        print("No valid face encodings found. Check your images.")

if __name__ == "__main__":
    store_face_encodings()
