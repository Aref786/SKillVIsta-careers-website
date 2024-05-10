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


#########################################################################################################################


# Function to authenticate user
def authenticate_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    cursor.close()
    return user

# Function to fetch data from the SQL Server table
def get_postings():
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
def insert_job_creation(title, description, budget, deadline, instructions, contact, salary_benefits):
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO JobPostings (Title, Description, Budget, Deadline, Instructions, ContactInfo, SalaryBenefits)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, budget, deadline, instructions, contact, salary_benefits))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

# Function to insert  view job posting data into the database
def viwe_job_postinges():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM JobPostings")
    view_job_postings = cursor.fetchall()
    conn.commit()
    conn.close()
    return view_job_postings


def view_job_postings():
    try:
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM JobPostings")
        job_postings = cursor.fetchall()
        cursor.close()
        conn.close()
        return job_postings
    except Exception as e:
        print("An error occurred while fetching job postings:", e)
        return []

#######################################################################################################################


@app.route('/')
def index():
     
     if 'username' in session:
        job_postings = get_postings()
        return redirect(url_for('view_postings'))
     else:
         job_postings = get_postings()
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
    session.pop('username', None)
    session.clear()  # Clear the session data
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

    
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
    if 'username' not in session:
        flash('Please log in to create a job posting.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        budget = request.form['budget']
        deadline = request.form['deadline']
        instructions = request.form['instructions']
        contact = request.form['contact']
        salary_benefits = request.form['salary_benefits']

        # Insert job posting data into the database
        try:
            insert_job_creation(title, description, budget, deadline, instructions, contact, salary_benefits)
            flash('Job posting created successfully!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('create_job_posting'))

    else:
        return render_template('create_job_posting.html')


@app.route('/view_postings')
def view_postings():
    job_postings = view_job_postings()
    return render_template('view_postings.html', job_postings=job_postings)




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