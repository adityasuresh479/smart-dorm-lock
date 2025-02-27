from flask import Flask
from flask_jwt_extended import JWTManager
from auth import auth_bp
from recognition import recognition_bp

app = Flask(__name__)

# Set JWT Secret Key (Change this in production!)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(recognition_bp, url_prefix="/recognition")

@app.route("/", methods=["GET"])
def home():
    return {"message": "Smart Dorm Lock API is running!"}

if __name__ == "__main__":
    app.run(debug=True)

