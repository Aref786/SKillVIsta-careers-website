from flask import Flask, render_template, request, redirect, url_for, flash, session
import pyodbc
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


username = None

# Database Connection
SERVER='AREF\SQLEXPRESS'
DATABASE="SKillVista"
connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'
# Create a connection
conn = pyodbc.connect(connectionString)

# Function to fetch data from the SQL Server table
def get_job_postings():
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM job_postings') 
    job_postings = cursor.fetchall()
    conn.close()
    return job_postings

# Function to insert user data into the database
def insert_user(username, email, password):
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
    conn.commit()
    cursor.close()
    session=session[username]

# Function to insert contact form data into the database
def insert_contact_data(name, email, message):
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contact_form (name, email, message) VALUES (?, ?, ?)', (name, email, message))
    conn.commit()
    conn.close()

# Function to insert job posting data into the database
def insert_job_creation(title, description, budget):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO job_posting (title, description, budget) VALUES (?, ?, ?)', (title, description, budget))
    conn.commit()
    cursor.close()


#############################################################################


@app.route('/')
def index():
    job_postings = get_job_postings()
    return render_template('index.html', job_postings=job_postings,username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global username
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM login WHERE username = ? AND password = ?", (username, password))
        row = cursor.fetchone()
        if row:
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    global username
    username = None
    return render_template('index.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username is already taken
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('signup'))
        
        # Insert new user into the database
        insert_user(username, email, password)
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')


@app.route('/create_job_posting', methods=['GET', 'POST'])
def create_job_posting():
    if 'username'  in session:
        flash('Please log in to create a job posting.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        budget = request.form['budget']

        # Insert job posting data into the database
        insert_job_creation(title, description, budget)
        
        flash('Job posting created successfully!', 'success')
        return redirect(url_for('profile'))
    else:
        return render_template('create_job_posting.html')


















@app.route('/job_details')
def job_details():
    # Job details logic
    return render_template('job_details.html')

@app.route('/about')
def about():
    # Logic for the about page
    return render_template('about.html')


@app.route('/profile')
def profile():
    # User profile logic
    return render_template('profile.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        insert_contact_data(name, email, message)
        return redirect(url_for(''))
    else:
        return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)