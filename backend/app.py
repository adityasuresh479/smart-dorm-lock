from flask import Flask, request, jsonify
from recognition import recognize_face
from auth import verify_user
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# GPIO setup for door lock (modify pin based on your setup)
LOCK_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LOCK_PIN, GPIO.OUT)
GPIO.output(LOCK_PIN, GPIO.LOW)  # Start with the door locked

def unlock_door():
    """Unlock the door for 5 seconds and then lock it"""
    GPIO.output(LOCK_PIN, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(LOCK_PIN, GPIO.LOW)  # Automatically locks after 5 seconds


@app.route('/scan', methods=['POST'])
def scan():
    if 'image' not in request.files:
        return jsonify({"message": "No image provided"}), 400

    file = request.files['image']
    
    # Process the image for facial recognition
    recognized_user = recognize_face(file)
    
    if recognized_user:
        if verify_user(recognized_user):
            unlock_door()
            return jsonify({"message": "Access granted", "user": recognized_user}), 200
        else:
            return jsonify({"message": "Unauthorized user"}), 403
    else:
        return jsonify({"message": "Face not recognized"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
