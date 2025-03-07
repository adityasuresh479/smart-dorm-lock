import face_recognition
import numpy as np
import json
import os
import sys

LOCAL_STORAGE_FILE = "face_encodings.json"  # Temporary storage for face encodings

# Load locally stored face encodings if the file exists
if os.path.exists(LOCAL_STORAGE_FILE):
    with open(LOCAL_STORAGE_FILE, "r") as f:
        face_data = json.load(f)
    known_face_names = list(face_data.keys())
    known_face_encodings = [np.array(encoding) for encoding in face_data.values()]
else:
    known_face_names = []
    known_face_encodings = []

def recognize_face(image_file):
    """Recognizes a face from an uploaded image and returns similarity score"""
    
    # Load the input image and extract face encodings
    image = face_recognition.load_image_file(image_file)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        return None, None  # No face detected

    face_encoding = face_encodings[0]  # Use the first detected face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

    if len(face_distances) == 0:
        return None, None  # No match found

    best_match_index = np.argmin(face_distances)  # Find best match
    similarity = (1 - face_distances[best_match_index]) * 100  # Convert distance to similarity

    if face_recognition.compare_faces([known_face_encodings[best_match_index]], face_encoding)[0]:
        return known_face_names[best_match_index], round(similarity, 2)

    return None, None  # No match found

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recognition.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    recognized_name, similarity = recognize_face(image_path)

    if recognized_name:
        print(f"Face recognized as: {recognized_name} with {similarity}% similarity")
    else:
        print("No match found")
