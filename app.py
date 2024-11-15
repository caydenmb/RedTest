import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

@app.route('/')
def hello():
    logger.info("Accessed the root endpoint.")
    return jsonify({"message": "Hello, world!"}), 200

if __name__ == "__main__":
    logger.info("Starting the app with debug mode.")
    app.run(host="0.0.0.0", port=8000, debug=True)
