from deepface import DeepFace
from database import get_face_embeddings
import numpy as np
import os
import sys

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recognize_face(image_file):
    """Recognizes a face from an uploaded image using FaceNet embeddings"""
    
    try:
        # Generate embedding for input image
        representation = DeepFace.represent(
            img_path=image_file,
            model_name="Facenet",
            detector_backend="retinaface",
            enforce_detection=True
        )[0]["embedding"]
        input_embedding = np.array(representation)
    except Exception as e:
        print(f"Face detection failed: {e}")
        return None, None

    known_embeddings = get_face_embeddings()
    if not known_embeddings:
        print("No stored face embeddings in database.")
        return None, None

    similarities = []
    names = []

    for username, stored_embedding in known_embeddings:
        similarity = cosine_similarity(input_embedding, stored_embedding)
        similarities.append(similarity)
        names.append(username)

    # Compute best match
    best_index = np.argmax(similarities)
    best_similarity = similarities[best_index] * 100
    best_name = names[best_index]

    # Debug output
    print("\nSimilarity Scores:")
    for name, score in zip(names, similarities):
        print(f"{name}: {score * 100:.2f}%")

    if best_similarity > 90:
        return best_name, round(best_similarity, 2)

    return None, None

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
        print("\nNo match found.")
