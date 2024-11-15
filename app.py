import os
from flask import Flask, render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Application initialization
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')  # Use a secure key

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# In-memory database simulation for users and configuration
users = {
    'admin': generate_password_hash('password')
}
config = {
    'SHUFFLE_WAGER_ENABLED': True,
    'SHUFFLE_RAFFLE_ENABLED': True,
    'CHICKEN_ENABLED': True,
    'SHUFFLE_API_KEY': 'default_shuffle_key',
    'CHICKEN_API_KEY': 'default_chicken_key',
    'START_TIME': 1620000000  # Example epoch start time
}

@app.route('/')
def index():
    logging.debug("Serving the index page.")
    return render_template('index.html', title='Redhunllef Event Platform')

@app.route('/shuffle_wager')
def shuffle_wager():
    logging.debug(f"Shuffle Wager Event requested, enabled status: {config['SHUFFLE_WAGER_ENABLED']}")
    return render_template('shuffle_wager.html', title='Shuffle Wager Event', config=config)

@app.route('/shuffle_raffle')
def shuffle_raffle():
    logging.debug(f"Shuffle Raffle Event requested, enabled status: {config['SHUFFLE_RAFFLE_ENABLED']}")
    return render_template('shuffle_raffle.html', title='Shuffle Raffle Event', config=config)

@app.route('/chicken')
def chicken():
    logging.debug(f"Chicken.gg Wager Event requested, enabled status: {config['CHICKEN_ENABLED']}")
    return render_template('chicken.html', title='Chicken.gg Wager Event', config=config)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        flash('You need to log in first.')
        logging.warning("Unauthorized access attempt to admin page.")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        config['SHUFFLE_WAGER_ENABLED'] = 'shuffle_wager_enabled' in request.form
        config['SHUFFLE_RAFFLE_ENABLED'] = 'shuffle_raffle_enabled' in request.form
        config['CHICKEN_ENABLED'] = 'chicken_enabled' in request.form
        logging.info(f"Admin updated event settings: {config}")

    logging.debug("Serving the admin settings page.")
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

    logging.debug("Serving the superuser settings page.")
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

    logging.debug("Serving the login page.")
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

# Running the app for production (debug mode turned off)
if __name__ == "__main__":
    logging.info("Starting the Flask application.")
    app.run(debug=False, host='0.0.0.0', port=8000)
