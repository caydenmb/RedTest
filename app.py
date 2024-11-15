from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import sys

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configure Logging
logging.basicConfig(level=logging.DEBUG, handlers=[
    logging.StreamHandler(sys.stdout)
])

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
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    app.logger.info('New user added: %s', new_user)
    return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    app.logger.info('User retrieved: %s', user)
    return jsonify(user.to_dict())

# Entry point
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
