from flask import Flask, request, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from deepface import DeepFace
import os
import numpy as np
import traceback
import time  # <-- ADD THIS for sleep()
from datetime import datetime
from database import add_user, get_face_embeddings, add_face_embedding,get_access_logs,log_access, db
from door_control import unlock_door, lock_door, cleanup  

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

# Path setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
FRONTEND_FOLDER = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ========== ROUTES ==========

@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/<path:filename>")
def serve_frontend(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    image = request.files.get("image")

    if not email or not password or not image:
        return jsonify({"error": "Missing required fields"}), 400

    if not allowed_file(image.filename):
        return jsonify({"error": "Invalid image format"}), 400

    # Save the image
    filename = secure_filename(image.filename)
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], email)
    os.makedirs(user_folder, exist_ok=True)
    image_path = os.path.join(user_folder, filename)
    image.save(image_path)

    try:
        representations = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            detector_backend="retinaface",
            enforce_detection=True
        )
        embedding = representations[0]["embedding"]
        add_face_embedding(email, np.array(embedding))

        user_data = {
            "email": email,
            "password": generate_password_hash(password),
            "created_at": datetime.now()
        }
        result = add_user(user_data)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user = db.users.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": f"Welcome back, {email}!"})


@app.route("/unlock", methods=["POST"])
def unlock():
    image = request.files.get("image")
    if not image:
        return jsonify({"error": "Image is required"}), 400

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    try:
        representation = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            detector_backend="retinaface",
            enforce_detection=True
        )[0]["embedding"]
        input_embedding = np.array(representation)

        known_embeddings = get_face_embeddings()
        if not known_embeddings:
            return jsonify({"error": "No embeddings in database"}), 500

        similarities = []
        usernames = []

        for username, stored_embedding in known_embeddings:
            sim = np.dot(input_embedding, stored_embedding) / (
                np.linalg.norm(input_embedding) * np.linalg.norm(stored_embedding)
            )
            similarities.append(sim)
            usernames.append(username)

        best_index = np.argmax(similarities)
        best_similarity = similarities[best_index] * 100
        best_username = usernames[best_index]

        access_granted = bool(best_similarity > 70)
        log_access(best_username, access_granted)

        if access_granted:
            unlock_door()  # <<< Unlock the door!
            time.sleep(5)  # <<< Keep it unlocked for 5 seconds
            lock_door()    # <<< Then lock it again

        return jsonify({
            "message": f"Access granted for {best_username}" if access_granted else "Access denied",
            "similarity": round(best_similarity, 2)
        })

    except Exception as e:
        print("=== UNLOCK ERROR TRACE ===")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/access-logs", methods=["GET"])
def get_logs():
    try:
        logs = get_access_logs()
        print("Access logs fetched:", logs)  # <=== ADD THIS
        return jsonify(logs)
    except Exception as e:
        print("Error fetching logs:", e)
        return jsonify({"error": str(e)}), 500


# ========== MAIN ==========

if __name__ == "__main__":
    try:
        app.run(debug=True,use_reloader=False)
    finally:
        cleanup()  # <<< Important: release GPIO when server stops!


