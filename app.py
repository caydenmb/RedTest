import os
import logging
from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Set up Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecret')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///mydb.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up SQLAlchemy and Migrate
try:
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    logging.info("SQLAlchemy and Flask-Migrate initialized successfully.")
except AttributeError as e:
    logging.error(f"Error initializing SQLAlchemy: {e}")
    raise e

# Set up logging level to debug for detailed output
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Example User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Example Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=False)

# Route handlers
@app.route('/')
def index():
    logging.info("Accessed the index route.")
    active_event = Event.query.filter_by(is_active=True).first()
    if active_event:
        logging.debug(f"Active event found: {active_event.name}")
        return render_template('index.html', event=active_event, title="Home")
    else:
        logging.warning("No active event found. Redirecting to 'no_event' page.")
        return render_template('no_event.html', title="No Event")

@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        logging.warning("Unauthorized access attempt to admin page.")
        return redirect(url_for('login'))
    events = Event.query.all()
    logging.info("Accessed the admin route. Listing all events.")
    return render_template('admin.html', events=events, title="Admin")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logging.debug(f"Attempt to login with username: {username}")

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['logged_in'] = True
            session['username'] = username
            logging.info(f"User {username} successfully logged in.")
            return redirect(url_for('index'))
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            flash('Invalid credentials')
    
    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    logging.info(f"User {session.get('username', 'Unknown')} logged out.")
    session.clear()
    return redirect(url_for('index'))

@app.route('/event/create', methods=['GET', 'POST'])
def create_event():
    if 'logged_in' not in session:
        logging.warning("Unauthorized access attempt to create an event.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%d %H:%M:%S')
        is_active = request.form.get('is_active') == 'on'

        new_event = Event(name=name, start_time=start_time, end_time=end_time, is_active=is_active)
        db.session.add(new_event)
        db.session.commit()
        logging.info(f"New event '{name}' created successfully.")
        return redirect(url_for('admin'))

    return render_template('create_event.html', title="Create Event")

@app.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    if 'logged_in' not in session:
        logging.warning("Unauthorized access attempt to edit an event.")
        return redirect(url_for('login'))

    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        event.name = request.form['name']
        event.start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%d %H:%M:%S')
        event.end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%d %H:%M:%S')
        event.is_active = request.form.get('is_active') == 'on'

        db.session.commit()
        logging.info(f"Event '{event.name}' updated successfully.")
        return redirect(url_for('admin'))

    return render_template('edit_event.html', event=event, title="Edit Event")

@app.route('/event/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    if 'logged_in' not in session:
        logging.warning("Unauthorized access attempt to delete an event.")
        return redirect(url_for('login'))

    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    logging.info(f"Event '{event.name}' deleted successfully.")
    return redirect(url_for('admin'))

@app.route('/api/events')
def api_events():
    events = Event.query.all()
    event_list = [{
        'id': event.id,
        'name': event.name,
        'start_time': event.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': event.end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'is_active': event.is_active
    } for event in events]
    logging.info("API request for events received.")
    return jsonify(event_list)

# Error handling for 404
@app.errorhandler(404)
def page_not_found(e):
    logging.error(f"Page not found: {request.url}")
    return render_template('404.html'), 404

# Running the app
if __name__ == '__main__':
    logging.info("Starting Flask application.")
    app.run(debug=False, host='0.0.0.0', port=8000)
