import os
import requests
from flask import Flask, render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Flask application initialization
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')  # Use a secure value for production

# Configure logging for debugging and operations
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log all messages to 'app.log'
        logging.StreamHandler()  # Output messages to the console as well
    ]
)

# API Keys and URLs
SHUFFLE_API_KEY = "f45f746d-b021-494d-b9b6-b47628ee5cc9"
CHICKEN_API_KEY = "316a2f45bff17a887b8a37748e61ac06"
CHICKEN_BASE_URL = "https://affiliates.chicken.gg/v1/referrals?key={api_key}&minTime={min_time}&maxTime={max_time}"

# In-memory storage for users and application configuration (Note: Replace with a database for production)
users = {
    'admin': generate_password_hash('password')  # Default admin credentials
}
config = {
    'SHUFFLE_WAGER_ENABLED': True,
    'SHUFFLE_RAFFLE_ENABLED': True,
    'CHICKEN_ENABLED': True,
    'SHUFFLE_API_KEY': SHUFFLE_API_KEY,
    'CHICKEN_API_KEY': CHICKEN_API_KEY,
    'START_TIME': 1620000000  # Example start time in epoch format
}

# Log worker startup
logging.info("Flask application instance initialized and ready to serve requests.")

@app.before_first_request
def before_first_request():
    # This runs before handling the first request and can be used for initialization tasks
    logging.info("First request received - initializing components if necessary.")

# Utility function for API requests
def fetch_data_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            logging.info(f"Data fetched successfully from API: {url}")
            return data
        else:
            logging.warning(f"No data found for the provided URL: {url}")
            return {"error": "No data found."}
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return {"error": str(e)}

@app.route('/')
def index():
    logging.info("Serving the index page.")
    return render_template('index.html', title='Redhunllef Event Platform')

@app.route('/shuffle_wager')
def shuffle_wager():
    if not config['SHUFFLE_WAGER_ENABLED']:
        logging.warning("Shuffle Wager Event is disabled - serving no_event page.")
        return render_template('no_event.html', title='No Race Available')
    
    # Fetch data from Shuffle API (dummy example)
    url = f"https://api.shuffle.com/data?key={config['SHUFFLE_API_KEY']}"
    data = fetch_data_from_api(url)
    
    logging.info("Serving Shuffle Wager Event page.")
    return render_template('shuffle_wager.html', title='Shuffle Wager Event', config=config, data=data)

@app.route('/shuffle_raffle')
def shuffle_raffle():
    if not config['SHUFFLE_RAFFLE_ENABLED']:
        logging.warning("Shuffle Raffle Event is disabled - serving no_event page.")
        return render_template('no_event.html', title='No Race Available')
    
    # Fetch data from Shuffle API for Raffle (dummy example)
    url = f"https://api.shuffle.com/raffle?key={config['SHUFFLE_API_KEY']}"
    data = fetch_data_from_api(url)
    
    logging.info("Serving Shuffle Raffle Event page.")
    return render_template('shuffle_raffle.html', title='Shuffle Raffle Event', config=config, data=data)

@app.route('/chicken')
def chicken():
    if not config['CHICKEN_ENABLED']:
        logging.warning("Chicken.gg Wager Event is disabled - serving no_event page.")
        return render_template('no_event.html', title='No Race Available')
    
    # Fetch data from Chicken API (dummy example)
    url = CHICKEN_BASE_URL.format(api_key=config['CHICKEN_API_KEY'], min_time=config['START_TIME'], max_time=int(os.getenv('MAX_TIME', 9999999999)))
    data = fetch_data_from_api(url)
    
    logging.info("Serving Chicken.gg Wager Event page.")
    return render_template('chicken.html', title='Chicken.gg Wager Event', config=config, data=data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        flash('You need to log in first.')
        logging.warning("Unauthorized access attempt to admin page.")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Update configuration based on form data
        config['SHUFFLE_WAGER_ENABLED'] = 'shuffle_wager_enabled' in request.form
        config['SHUFFLE_RAFFLE_ENABLED'] = 'shuffle_raffle_enabled' in request.form
        config['CHICKEN_ENABLED'] = 'chicken_enabled' in request.form
        logging.info(f"Admin updated event settings: {config}")

    logging.info("Serving the admin settings page.")
    return render_template('admin.html', title='Admin Settings', config=config)

@app.route('/superuser', methods=['GET', 'POST'])
def superuser():
    if not session.get('logged_in') or session.get('username') != 'admin':
        flash('You do not have access to this page.')
        logging.warning("Unauthorized access attempt to superuser page.")
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'add_user' in request.form:
            new_username = request.form.get('username')
            new_password = request.form.get('password')
            if new_username in users:
                flash('User already exists.')
                logging.warning(f"Attempted to add existing user: {new_username}")
            else:
                users[new_username] = generate_password_hash(new_password)
                flash(f'User {new_username} added successfully.')
                logging.info(f"Superuser added new user: {new_username}")

        if 'delete_user' in request.form:
            user_to_delete = request.form.get('delete_user')
            if user_to_delete in users and user_to_delete != 'admin':
                del users[user_to_delete]
                flash(f'User {user_to_delete} deleted successfully.')
                logging.info(f"Superuser deleted user: {user_to_delete}")
            else:
                flash('Cannot delete admin or non-existent user.')
                logging.warning(f"Attempted to delete user: {user_to_delete}")

        if 'update_api_keys' in request.form:
            config['SHUFFLE_API_KEY'] = request.form.get('shuffle_api_key')
            config['CHICKEN_API_KEY'] = request.form.get('chicken_api_key')
            config['START_TIME'] = request.form.get('start_time')
            logging.info(f"Superuser updated API keys: {config}")

    logging.info("Serving the superuser settings page.")
    return render_template('superuser.html', title='Superuser Settings', config=config, users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['logged_in'] = True
            session['username'] = username
            logging.info(f"User {username} logged in.")
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password.')
            logging.warning(f"Failed login attempt for username: {username}")

    logging.info("Serving the login page.")
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    logging.info(f"User {session.get('username')} logged out.")
    session.clear()
    return redirect(url_for('index'))

# Custom 404 error handler to redirect to 404.html
@app.errorhandler(404)
def page_not_found(e):
    logging.warning(f"404 error - page not found: {request.path}")
    return render_template('404.html', title='404 - Page Not Found'), 404

# Note: No app.run() here; Gunicorn will manage the application in production
