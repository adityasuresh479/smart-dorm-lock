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
    
    # Ensure all encodings are NumPy arrays and have the correct shape
    known_face_encodings = []
    for name, encodings in face_data.items():
        if isinstance(encodings, list):  # Ensure it's a list
            np_encodings = [np.array(enc) for enc in encodings if isinstance(enc, list) and len(enc) == 128]
            if np_encodings:
                avg_encoding = np.mean(np_encodings, axis=0)  # Average encoding for stability
                avg_encoding = avg_encoding / np.linalg.norm(avg_encoding)  # Normalize encoding
                known_face_encodings.append(avg_encoding)
            else:
                known_face_names.remove(name)  # Remove names without valid encodings
else:
    known_face_names = []
    known_face_encodings = []

def recognize_face(image_file):
    """Recognizes a face from an uploaded image and returns similarity scores"""
    
    # Load the input image and extract face encodings
    image = face_recognition.load_image_file(image_file)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        print("No face detected in the input image.")
        return None, None  # No face detected

    face_encoding = face_encodings[0]  # Use the first detected face
    face_encoding = face_encoding / np.linalg.norm(face_encoding)  # Normalize encoding

    if len(known_face_encodings) == 0:
        print("No stored face encodings found to compare against.")
        return None, None  # No match found

    # Convert known face encodings to a NumPy array (ensure it's properly shaped)
    known_face_encodings_array = np.array(known_face_encodings)

    # Compute cosine similarity instead of Euclidean distance
    similarities = np.dot(known_face_encodings_array, face_encoding)  # Cosine similarity

    # Debugging: Print all similarity scores
    print("\nSimilarity Scores:")
    for i, similarity in enumerate(similarities):
        similarity_percentage = similarity * 100  # Convert to percentage
        print(f"{known_face_names[i]}: {similarity_percentage:.2f}%")

    best_match_index = np.argmax(similarities)  # Find best match
    best_similarity = similarities[best_match_index] * 100  # Convert to percentage

    if best_similarity > 95:  # Adjustable threshold
        return known_face_names[best_match_index], round(best_similarity, 2)

    return None, None  # No match found

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recognition.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        sys.exit(1)

    recognized_name, similarity = recognize_face(image_path)

    if recognized_name:
        print(f"\nFace recognized as: {recognized_name} with {similarity:.2f}% similarity")
    else:
        print("\nNo match found")
