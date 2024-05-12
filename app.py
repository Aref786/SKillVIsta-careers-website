from flask import Flask, render_template, request, redirect, url_for, flash,session
import pyodbc
import hashlib
import os
from werkzeug.utils import secure_filename

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

# Function to fetch static data 
def Home_get_postings():
    Home_job_postings = [
        {
            'id': 1,
            'title': 'Software Engineer',
            'company': 'ABC Tech Solutions',
            'description': 'We are seeking a software engineer to join our team...',
            'deadline': '2024-05-31',
            'how_to_apply': 'Submit your resume to careers@abctech.com...',
            'contact': 'For inquiries, contact HR at hr@abctech.com.',
            'benefits': 'Competitive salary and benefits.',
            'image_url': url_for('static', filename='images/asset-01.jpg')
        },
        {
            'id': 2,
            'title': 'Data Analyst',
            'company': 'Data Insights Inc.',
            'description': 'Data Insights Inc. seeks a detail-oriented data analyst...',
            'deadline': '2024-06-15',
            'how_to_apply': 'Send your resume to careers@datainsights.com...',
            'contact': 'For inquiries, email info@datainsights.com.',
            'benefits': 'Competitive salary with bonuses.',
            'image_url': url_for('static', filename='images/asset-02.png')
       },
        {
            'id': 3,
            'title': 'UX/UI Designer',
            'company': 'Design Innovations Co.',
            'description': 'Design Innovations Co. needs a creative UX/UI designer...',
            'deadline': '2024-06-30',
            'how_to_apply': 'Submit your resume to jobs@designinnovations.com...',
            'contact': 'For more info, contact careers@designinnovations.com.',
            'benefits': 'Competitive salary and remote work options.',
            'image_url': url_for('static', filename='images/asset-07.jpeg')
        },
        {
            'id': 4,
            'title': 'Marketing Specialist',
            'company': 'Brand Solutions Agency',
            'description': 'Brand Solutions Agency seeks a marketing specialist...',
            'deadline': '2024-07-15',
            'how_to_apply': 'Send your resume to careers@brandsolutions.com...',
            'contact': 'For inquiries, email info@brandsolutions.com.',
            'benefits': 'Competitive salary and performance incentives.',
            'image_url': url_for('static', filename='images/asset-08.png')
        },
        {
            'id': 5,
            'title': 'Web Developer',
            'company': 'Tech Solutions Ltd.',
            'description': 'Tech Solutions Ltd. is looking for a skilled web developer...',
            'deadline': '2024-07-30',
            'how_to_apply': 'To apply, send your CV to careers@techsolutions.com...',
            'contact': 'For inquiries, contact HR at hr@techsolutions.com.',
            'benefits': 'Competitive salary and opportunities for career growth.',
           'image_url': url_for('static', filename='images/asset-01.jpg')
        },
        {
            'id': 6,
            'title': 'Financial Analyst',
            'company': 'Finance Experts Inc.',
            'description': 'Finance Experts Inc. is hiring a financial analyst...',
            'deadline': '2024-08-15',
            'how_to_apply': 'Submit your application to jobs@financeexperts.com...',
            'contact': 'For more information, email info@financeexperts.com.',
            'benefits': 'Competitive salary and comprehensive benefits package.',
            'image_url': url_for('static', filename='images/asset-02.png')
        },
        {
            'id': 7,
            'title': 'Graphic Designer',
            'company': 'Creative Designs Agency',
            'description': 'Creative Designs Agency is seeking a talented graphic designer...',
            'deadline': '2024-08-30',
            'how_to_apply': 'Send your portfolio to careers@creativedesigns.com...',
            'contact': 'For inquiries, contact HR at hr@creativedesigns.com.',
            'benefits': 'Competitive salary and a creative work environment.',
            'image_url': url_for('static', filename='images/asset-01.jpg')
        },
        {
            'id': 8,
            'title': 'Customer Service Representative',
            'company': 'Service Excellence Ltd.',
            'description': 'Service Excellence Ltd. is hiring a customer service representative...',
            'deadline': '2024-09-15',
            'how_to_apply': 'To apply, send your resume to careers@serviceexcellence.com...',
            'contact': 'For inquiries, email info@serviceexcellence.com.',
            'benefits': 'Competitive salary and training opportunities.',
            'image_url': url_for('static', filename='images/asset-08.png')
        },
        {
            'id': 9,
            'title': 'Service Representative',
            'company': 'Service Excellence Ltd.',
            'description': 'Service Excellence Ltd. is hiring a customer service representative...',
            'deadline': '2024-09-15',
            'how_to_apply': 'To apply, send your resume to careers@serviceexcellence.com...',
            'contact': 'For inquiries, email info@serviceexcellence.com.',
            'benefits': 'Competitive salary and training opportunities.',
            'image_url': url_for('static', filename='images/asset-01.jpg')
        },
         {
            'id': 10,
            'title': 'Content Writer',
            'company': 'WordSmith Inc.',
            'description': 'WordSmith Inc. is looking for a creative content writer...',
            'deadline': '2024-09-30',
            'how_to_apply': 'Submit writing samples to careers@wordsmith.com...',
            'contact': 'For inquiries, email info@wordsmith.com.',
            'benefits': 'Competitive salary and flexible work schedule.',
            'image_url': url_for('static', filename='images/asset-08.png')
        },
        {
            'id': 11,
            'title': 'Human Resources Manager',
            'company': 'HR Solutions Group',
            'description': 'HR Solutions Group is seeking an experienced HR manager...',
            'deadline': '2024-10-15',
            'how_to_apply': 'Send your CV to careers@hrsolutionsgroup.com...',
            'contact': 'For more information, contact HR at hr@hrsolutionsgroup.com.',
            'benefits': 'Competitive salary and benefits package.',
            'image_url': url_for('static', filename='images/asset-02.png')
        }
    ]
    return Home_job_postings

def get_jobes():
    # Assuming connectionString is defined somewhere with the appropriate database connection details
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
def insert_job_creation(title, description, budget, deadline, instructions, contact, salary_benefits, username):
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO UserJobPostings (Title, Description, Budget, Deadline, Instructions, ContactInfo, SalaryBenefits, UserName)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, budget, deadline, instructions, contact, salary_benefits, username))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


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
    username = session.get('username')
    print(username)
    job_postings = Home_get_postings()  # Call the function to get job postings
    if not username:
        return render_template('index.html', job_postings=job_postings)
    else:
        return render_template('index.html', job_postings=job_postings, username=username)

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
            session['username'] = username
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
    resume_path = None  # Initialize resume_path variable
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
        
        # Handle file upload (resume)
        if 'resume' in request.files:
            resume = request.files['resume']
            resume_filename = secure_filename(resume.filename)
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
            resume.save(resume_path)
        
        # Insert new user into the database
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('INSERT INTO users (username, email, password, resume_path) VALUES (?, ?, ?, ?)', (username, email, hashed_password, resume_path))
        conn.commit()
        cursor.close()
        
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')
        

@app.route('/create_job_posting', methods=['GET', 'POST'])
def create_job_posting():
    # Get username from session
    username = session.get('username')
    if not username:
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
            insert_job_creation(title, description, budget, deadline, instructions, contact, salary_benefits, username)
            flash('Job posting created successfully!', 'success')
            print(title,description,budget,deadline,instructions,contact,salary_benefits,username)
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('create_job_posting'))
    else:
        return render_template('create_job_posting.html')


#@app.route('/view_postings')
#def view_postings():
#   job_postings = view_job_postings()
#   return render_template('view_postings.html', job_postings=job_postings)


@app.route('/job_details')
def job_details():
    job_postings = get_jobes()
    return render_template('job_details.html', job_postings=job_postings)


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