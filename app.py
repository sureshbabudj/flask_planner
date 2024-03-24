from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from flask_htmx import HTMX, responses
from models import User, Plan
from database import db_session, init_db
from faker import Faker
import random

app = Flask(__name__)
app.secret_key = 'cdskbcska74hdfjskbcdksy'

htmx = HTMX(app)

@app.route('/login', methods=['POST'])
def login():
    # Handle login
    email = request.form['email']
    password = request.form['password']
    user = db_session.query(User).filter_by(email=email).first()
    if user and user.verify_password(password):
        # Password is correct, create user session
        session['user_id'] = user.id
        return responses.make_response(location='/planner')
    else:
        # Invalid credentials
        return responses.make_response('Invalid credentials', retarget="#errors"), 422


@app.route('/', methods=['GET'])
def home():
    if 'user_id' in session:
        # User is logged in, redirect to planner route
        return redirect(url_for('planner'))
    
    # Show login/register page
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handle registration
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name=name, email=email)
        new_user.password = password  # Set password hash
        db_session.add(new_user)
        db_session.commit()

        return responses.make_response(location='/')
    
    # Show registration page
    return render_template('register.html')

@app.route('/logout')
def logout():
    # Remove the user_id from the session if it's there
    session.pop('user_id', None)
    return responses.make_response(location='/')
    
@app.route('/planner',  methods=['GET', 'POST'])
def planner():
    if 'user_id' not in session:
        # User is not logged in, redirect to home
        return redirect(url_for('home'))
    
    # Get the current date
    current_date = datetime.now()

    # Find the start of the week (Monday)
    start_of_week = current_date - timedelta(days=current_date.weekday())

    # Generate a list of dates for the current week
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    
    return render_template('planner.html', week_dates=week_dates)
    

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        # User is not logged in, redirect to home
        return redirect(url_for('home'))
    
    # Retrieve all users and plans
    users = db_session.query(User).all()
    plans = db_session.query(Plan).all()
    
    # Render a template that lists users and plans
    # Assuming 'templates/home.html' exists and is set up to display users and plans
    return render_template('admin.html', users=users, plans=plans)

# Instantiate a Faker object
fake = Faker()

@app.route('/seed_db')
def seed_db():
    # Create 10 users with faker data
    for _ in range(10):
        name = fake.name()
        email = fake.email()
        password = fake.password()
        new_user = User(name=name, email=email)
        new_user.password = password  # Set password hash
        db_session.add(new_user)
    db_session.commit()

    # Retrieve all users
    users = db_session.query(User).all()

    # Create 5 plans with random users as creators and participants
    for _ in range(5):
        creator = random.choice(users)
        start_time = fake.future_datetime(end_date="+30d")  # Random future date within 30 days
        end_time = start_time + timedelta(hours=random.randint(1, 5))  # Random duration between 1 to 5 hours
        new_plan = Plan(
            title=fake.sentence(nb_words=3),  # Random title
            summary=fake.text(max_nb_chars=200),  # Random summary
            link=fake.url(),  # Random URL
            duration=(end_time - start_time).seconds // 60,  # Duration in minutes
            start_time=start_time,
            end_time=end_time,
            creator=creator
        )
        db_session.add(new_plan)
        # Add random participants to the plan
        participants = random.sample(users, k=random.randint(1, len(users)-1))
        for participant in participants:
            if participant != creator:
                new_plan.participants.append(participant)
    db_session.commit()

    return 'Database seeded with users and plans!'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    
