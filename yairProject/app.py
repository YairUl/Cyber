from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

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


# Initialize Database
with app.app_context():
    db.create_all()


# Landing Page → Redirect to Sign In
@app.route('/')
def home():
    return redirect(url_for('signin_page'))  # Go directly to Sign In


# Sign-Up Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    nickname = data.get('nickname')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists."}), 400

    if User.query.filter_by(nickname=nickname).first():
        return jsonify({"message": "Nickname already taken."}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(email=email, password=hashed_password, nickname=nickname)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id  # Store user ID in session
    return jsonify({"message": "Signup successful!", "redirect": url_for('messages')}), 200


# Sign-In Route
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id  # Store user ID in session
        return jsonify({"message": "Sign-in successful!", "redirect": url_for('messages')}), 200

    return jsonify({"message": "Invalid email or password."}), 400


# Messages Page (Placeholder)
@app.route('/messages')
def messages():
    if 'user_id' not in session:
        return redirect(url_for('signin_page'))  # Redirect to sign-in if not logged in
    return render_template('messages.html')  # Load messages page


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
