import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging.handlers import RotatingFileHandler

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set up logging
if not os.path.exists('logs'):
    os.mkdir('logs')

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] - %(message)s')

# Console logging
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# File logging
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=5)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

# Logger configuration
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(console_handler)
app.logger.addHandler(file_handler)

# Log application start
app.logger.info('Starting Flask application...')

# Example Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

# Routes
@app.route('/')
def index():
    app.logger.info('Index endpoint called.')
    return "Hello, world! The app is running."

@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f'New user added: {new_user.to_dict()}')
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        app.logger.error(f"Error adding user: {e}", exc_info=True)
        return jsonify({"error": "Unable to add user"}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        app.logger.info(f'User retrieved: {user.to_dict()}')
        return jsonify(user.to_dict())
    except Exception as e:
        app.logger.error(f"Error retrieving user with id {user_id}: {e}", exc_info=True)
        return jsonify({"error": "Unable to retrieve user"}), 500

# Entry point
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
