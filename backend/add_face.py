from deepface import DeepFace
from database import add_face_embedding, add_user
import os
import numpy as np
from datetime import datetime

KNOWN_FACES_DIR = "data"  # Each subfolder = one user

def extract_and_store_embeddings():
    if not os.path.exists(KNOWN_FACES_DIR):
        print(f"Directory '{KNOWN_FACES_DIR}' does not exist.")
        return

    for username in os.listdir(KNOWN_FACES_DIR):
        user_folder = os.path.join(KNOWN_FACES_DIR, username)
        if not os.path.isdir(user_folder):
            continue  # Skip files, only use directories as users

        print(f"\nProcessing user: {username}")
        embeddings_stored = 0

        for filename in os.listdir(user_folder):
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            image_path = os.path.join(user_folder, filename)
            print(f"  → {filename}")

            try:
                representations = DeepFace.represent(
                    img_path=image_path,
                    model_name="Facenet",
                    detector_backend="retinaface",
                    enforce_detection=True
                )

                for obj in representations:
                    embedding = obj["embedding"]
                    add_face_embedding(username, np.array(embedding))
                    embeddings_stored += 1

            except Exception as e:
                print(f"    ⚠️  Failed to process {filename}: {e}")

        if embeddings_stored > 0:
            user_data = {
                "username": username,
                "email": f"{username}@example.com",  # Placeholder email
                "created_at": datetime.now()
            }
            add_user(user_data)
            print(f"Stored {embeddings_stored} embeddings for {username} and registered user in DB.")
        else:
            print(f"No valid faces found for {username}.")

if __name__ == "__main__":
    extract_and_store_embeddings()
