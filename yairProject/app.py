from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

db = SQLAlchemy(app)
Session(app)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Increase length for security
    nickname = db.Column(db.String(120), unique=True, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)  # Store local time

# Initialize Database
with app.app_context():
    db.create_all()


# Landing Page → Redirect to Sign In
@app.route('/')
def home():
    return redirect(url_for('signin_page'))  # Go directly to Sign In


# Sign-Up Route
@app.route('/signupw', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    nickname = data.get('nickname')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    if User.query.filter_by(nickname=nickname).first():
        return jsonify({"message": "Nickname already taken"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    new_user = User(email=email, password=hashed_password, nickname=nickname)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id
    return jsonify({"redirect": "/messages"}), 200  # Redirect to messages


# Sign-In Route
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    print(str(data))
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({"redirect": "/messages"}), 200  # Redirect to messages
    return jsonify({"message": "Invalid email or password"}), 400


# Messages Page (Placeholder)
@app.route('/messages')
def messages():
    if 'user_id' not in session:
        return redirect(url_for('signin_page'))  # Redirect to sign-in if not logged in
    return render_template('messages.html')  # Load messages page


@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401  # User must be signed in

    data = request.get_json()
    sender_id = session['user_id']
    receiver_id = data.get('receiver_id')
    message_text = data.get('message')

    # Validate receiver exists
    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({"message": "Recipient does not exist"}), 400

    # Save message
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, message=message_text)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        "message": "Message sent successfully!",
        "message_id": new_message.id,
        "timestamp": new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }), 200

@app.route('/get_messages', methods=['GET'])
def get_messages():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = session['user_id']

    messages = Message.query.filter(
        (Message.sender_id == user_id) | (Message.receiver_id == user_id)
    ).order_by(Message.timestamp).all()

    messages_data = [
        {
            "id": msg.id,
            "sender_id": msg.sender_id,
            "receiver_id": msg.receiver_id,
            "message": msg.message,
            "timestamp": msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for msg in messages
    ]

    return jsonify(messages_data), 200


# Logout Route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove user session
    return jsonify({"message": "Logged out successfully!", "redirect": url_for('signin_page')}), 200


# Sign-In Page
@app.route('/signin')
def signin_page():
    return render_template('signin.html')  # Load sign-in page


# Sign-Up Page
@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')  # Load sign-up page


if __name__ == '__main__':
    app.run(debug=True)
