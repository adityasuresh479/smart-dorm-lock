import face_recognition
import numpy as np
import cv2
import os
from database import get_face_encodings
# Directory where known user images are stored
KNOWN_FACES_DIR = "data"

# Load known face encodings from the database
face_data = get_face_encodings()
known_face_names, known_face_encodings = zip(*face_data) if face_data else ([], [])


# Load and encode faces from the "data/" folder
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])  # Use filename as name

def recognize_face(image_file):
    """Recognizes face from an uploaded image"""
    
    # Load image and find face encodings
    image = face_recognition.load_image_file(image_file)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        return None  # No face detected

    face_encoding = face_encodings[0]  # Use first face detected
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

    # Find the best match
    best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None

    if best_match_index is not None and matches[best_match_index]:
        return known_face_names[best_match_index]  # Return the recognized username
    
    return None  # No match found
