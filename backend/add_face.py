import face_recognition
import numpy as np
import os
import json

KNOWN_FACES_DIR = "data"  # Folder containing known faces
LOCAL_STORAGE_FILE = "face_encodings.json"  # Temporary local file

def store_face_encodings():
    # Load existing encodings if the file exists
    if os.path.exists(LOCAL_STORAGE_FILE):
        with open(LOCAL_STORAGE_FILE, "r") as f:
            try:
                face_data = json.load(f)
                if not isinstance(face_data, dict):
                    face_data = {}  # Ensure it's a dictionary
            except (json.JSONDecodeError, TypeError):
                face_data = {}
    else:
        face_data = {}

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(KNOWN_FACES_DIR, filename)
            print(f"Processing {filename}...")  # Debugging print

            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                username = os.path.splitext(filename)[0]  # Remove file extension
                
                # Ensure storage format is consistent
                if username not in face_data:
                    face_data[username] = []

                # Convert to NumPy and ensure shape consistency
                new_encodings = [enc.tolist() for enc in encodings]
                existing_encodings = face_data[username]

                # Only add unique encodings
                for enc in new_encodings:
                    if not any(np.allclose(np.array(enc), np.array(existing), atol=1e-6) for existing in existing_encodings):
                        face_data[username].append(enc)

                print(f"Stored {len(new_encodings)} new face encodings for {username}")

            else:
                print(f"No face detected in {filename}")

    # Save locally only if faces were found
    if face_data:
        with open(LOCAL_STORAGE_FILE, "w") as f:
            json.dump(face_data, f, indent=4)  # Pretty-print JSON for readability
        print(f"Encodings saved locally in {LOCAL_STORAGE_FILE}")
    else:
        print("No valid face encodings found. Check your images.")

if __name__ == "__main__":
    store_face_encodings()
