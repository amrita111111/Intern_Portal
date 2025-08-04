from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# JSON file path
DATA_FILE = 'data/users.json'

def load_data():
    """Load data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            # Return default data if file doesn't exist
            return {
                "users": [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "referral_code": "johndoe2025",
                        "total_donations": 1250,
                        "rewards": [
                            {"id": 1, "name": "Coffee Voucher", "description": "Free coffee at campus cafe", "unlocked": True},
                            {"id": 2, "name": "Lunch Pass", "description": "Free lunch at cafeteria", "unlocked": True},
                            {"id": 3, "name": "Gift Card", "description": "$25 Amazon gift card", "unlocked": False},
                            {"id": 4, "name": "Mentorship Session", "description": "1-hour session with senior developer", "unlocked": False}
                        ]
                    },
                    {
                        "id": 2,
                        "name": "Jane Smith",
                        "email": "jane.smith@example.com",
                        "referral_code": "janesmith2025",
                        "total_donations": 2100,
                        "rewards": [
                            {"id": 1, "name": "Coffee Voucher", "description": "Free coffee at campus cafe", "unlocked": True},
                            {"id": 2, "name": "Lunch Pass", "description": "Free lunch at cafeteria", "unlocked": True},
                            {"id": 3, "name": "Gift Card", "description": "$25 Amazon gift card", "unlocked": True},
                            {"id": 4, "name": "Mentorship Session", "description": "1-hour session with senior developer", "unlocked": False}
                        ]
                    },
                    {
                        "id": 3,
                        "name": "Mike Johnson",
                        "email": "mike.johnson@example.com",
                        "referral_code": "mikejohnson2025",
                        "total_donations": 800,
                        "rewards": [
                            {"id": 1, "name": "Coffee Voucher", "description": "Free coffee at campus cafe", "unlocked": True},
                            {"id": 2, "name": "Lunch Pass", "description": "Free lunch at cafeteria", "unlocked": False},
                            {"id": 3, "name": "Gift Card", "description": "$25 Amazon gift card", "unlocked": False},
                            {"id": 4, "name": "Mentorship Session", "description": "1-hour session with senior developer", "unlocked": False}
                        ]
                    }
                ]
            }
    except Exception as e:
        print(f"Error loading data: {e}")
        return {"users": []}

def save_data(data):
    """Save data to JSON file"""
    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# API Endpoints
@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    intern_data = load_data()
    user = next((user for user in intern_data["users"] if user["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/api/users')
def get_all_users():
    intern_data = load_data()
    return jsonify(intern_data["users"])

@app.route('/api/leaderboard')
def get_leaderboard():
    intern_data = load_data()
    # Sort users by total donations in descending order
    leaderboard = sorted(intern_data["users"], key=lambda x: x["total_donations"], reverse=True)
    return jsonify(leaderboard)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user_id = data.get('user_id', 1)  # Default to user 1 if not specified
    
    # Dummy authentication - in real app, you'd check against database
    if email and password:
        intern_data = load_data()
        # Find user by ID (1, 2, or 3)
        user = next((user for user in intern_data["users"] if user["id"] == user_id), None)
        if user:
            return jsonify({
                "success": True,
                "user": user,
                "message": "Login successful"
            })
        else:
            return jsonify({"success": False, "message": "User not found"}), 404
    
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    # Dummy signup - in real app, you'd save to database
    if name and email and password:
        intern_data = load_data()
        new_user = {
            "id": len(intern_data["users"]) + 1,
            "name": name,
            "email": email,
            "referral_code": f"{name.lower().replace(' ', '')}2025",
            "total_donations": 0,
            "rewards": [
                {"id": 1, "name": "Coffee Voucher", "description": "Free coffee at campus cafe", "unlocked": False},
                {"id": 2, "name": "Lunch Pass", "description": "Free lunch at cafeteria", "unlocked": False},
                {"id": 3, "name": "Gift Card", "description": "$25 Amazon gift card", "unlocked": False},
                {"id": 4, "name": "Mentorship Session", "description": "1-hour session with senior developer", "unlocked": False}
            ]
        }
        intern_data["users"].append(new_user)
        
        # Save updated data to JSON file
        if save_data(intern_data):
            return jsonify({
                "success": True,
                "user": new_user,
                "message": "Signup successful"
            })
        else:
            return jsonify({"success": False, "message": "Error saving user data"}), 500
    
    return jsonify({"success": False, "message": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 