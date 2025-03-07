import face_recognition
import cv2

# Load the image
image_path = "data/IMG_9469.jpeg"  # Replace with your actual image file path
image = face_recognition.load_image_file(image_path)

# Detect faces
face_locations = face_recognition.face_locations(image)

# Print results
if face_locations:
    print(f"Detected {len(face_locations)} face(s) in the image.")
    for i, (top, right, bottom, left) in enumerate(face_locations):
        print(f"Face {i + 1}: Top={top}, Right={right}, Bottom={bottom}, Left={left}")
else:
    print("No faces detected.")
