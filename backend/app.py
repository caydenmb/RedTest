from flask import Flask, jsonify, render_template, send_from_directory
import os
import logging
from flask_cors import CORS
from utils import fetch_leaderboard_data
from waitress import serve

# Set up Flask app
app = Flask(__name__, static_folder='../frontend/build', template_folder='../frontend/build')
CORS(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialization to check if index.html exists
def initialize_app():
    index_path = os.path.join(app.template_folder, 'index.html')
    if not os.path.exists(index_path):
        logger.error(f"Initialization Error: index.html not found at {index_path}")
        raise FileNotFoundError(f"index.html not found at {index_path}")
    else:
        logger.info(f"Initialization Successful: index.html found at {index_path}")

@app.route("/api/leaderboard/<sponsor>", methods=["GET"])
def get_leaderboard(sponsor):
    try:
        leaderboard_data, status_code = fetch_leaderboard_data(sponsor)
        if status_code == 200:
            logger.info(f"Successfully fetched leaderboard data for sponsor: {sponsor}")
            return jsonify(leaderboard_data)
        else:
            logger.error(f"Failed to fetch leaderboard data for sponsor: {sponsor}, status code: {status_code}")
            return jsonify({"error": f"Failed to fetch leaderboard data. Status code: {status_code}"}), status_code
    except Exception as e:
        logger.exception(f"Unexpected error occurred while fetching leaderboard data for sponsor: {sponsor}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        logger.info(f"Serving static file: {path}")
        return send_from_directory(app.static_folder, path)
    else:
        logger.info(f"Serving index.html for path: {path}")
        return render_template('index.html')

@app.before_request
def before_request():
    logger.debug("Handling incoming request.")

@app.after_request
def after_request(response):
    logger.debug(f"Request completed with response status: {response.status}")
    return response

if __name__ == "__main__":
    try:
        initialize_app()
        logger.info("Starting Flask server on port 8080")
        serve(app, host='0.0.0.0', port=8080)
    except Exception as e:
        logger.exception(f"An error occurred during application initialization or startup: {e}")
