from flask import Blueprint, request, jsonify, g
from flask_bcrypt import Bcrypt
from flask_login import logout_user, login_required, LoginManager, login_user
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017")

# database instance
db = g.db
users = db['users']

login_manager = LoginManager()
bcrypt = Bcrypt()

user_management = Blueprint('user_management', __name__)


@login_manager.user_loader
def load_user(user_id):
    return users.find_one({'_id': ObjectId(user_id)})


@user_management.route('/register', methods=['POST'])
def register():
    # Get data from request
    email = request.json.get('email')
    password = request.json.get('password')

    # Check if email already exists
    if users.find_one({'email': email}):
        return jsonify({'error': 'Email already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new user
    user = {
        'email': email,
        'password': hashed_password,
    }

    # Insert the user in the database
    users.insert_one(user)

    return jsonify({'message': 'Registered successfully'}), 201


@user_management.route('/login', methods=['POST'])
def login():
    # Get data from request
    email = request.json.get('email')
    password = request.json.get('password')

    # Find the user by email
    user = users.find_one({'email': email})

    # If user doesn't exist or password is wrong
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 400

    # Log in the user and establish the session
    user_obj = {
        "_id": str(user["_id"]),
        "email": email
    }
    login_user(user_obj)

    return jsonify({"message": "Logged in successfully"}), 200


@user_management.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200
