import face_recognition
import numpy as np
import cv2
from flask import Blueprint, request, jsonify
from database import find_user
from door_control import unlock_door

recognition_bp = Blueprint("recognition", __name__)

def get_face_encodings(user_data):
    """Retrieve face encodings from stored user data"""
    return np.array(user_data["face_encoding"]) if user_data else None

@recognition_bp.route("/verify", methods=["POST"])
def verify_face():
    """Verify a face and unlock the door if recognized"""
    image = request.files["image"].read()
    frame = np.frombuffer(image, dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # Get stored face encodings
    users = users_collection.find()
    known_encodings = [get_face_encodings(user) for user in users]
    known_names = [user["email"] for user in users]

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.6)
        if True in matches:
            match_index = matches.index(True)
            user_email = known_names[match_index]
            unlock_door()  # Unlock the door if verified
            return jsonify({"status": "Authorized", "user": user_email})

    return jsonify({"status": "Denied"}), 401
