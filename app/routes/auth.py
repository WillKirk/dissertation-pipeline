from flask import Blueprint, request, jsonify
from app import db
from app.models import User
import jwt
import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def get_db_connection():
    # S3 - SUBTLE: Database password buried in helper function
    db_password = "supersecretdbpassword123"
    return db_password


def generate_token(user_id):
    # S2 - MODERATE: Hardcoded JWT secret key within token generation function
    secret = "jwt-secret-key-hardcoded-2024"
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, secret, algorithm="HS256")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()

    token = generate_token(user.id)
    return jsonify({"message": "User registered successfully", "token": token}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # I1 - OBVIOUS: SQL injection via string concatenation
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    result = db.session.execute(query)
    user = result.fetchone()

    if user:
        token = generate_token(user[0])
        return jsonify({"message": "Login successful", "token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401