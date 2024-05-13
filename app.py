from flask import Flask, render_template, request, redirect, url_for, flash,session
import pyodbc
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database Connection
SERVER = r'AREF\SQLEXPRESS'
DATABASE = "SkillVista"
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


#######################################################################################################################

@app.route('/')
def index():
    username = session.get('username')
    #print(username)
    job_postings = Home_get_postings()  # Call the function to get job postings
    if not username:
        return render_template('index.html', job_postings=job_postings)
    else:
        return render_template('index.html', job_postings=job_postings, username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        global role
        role = request.form['role']
        
        # Establish a database connection
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
        
        if role == 'employer':
            cursor.execute("SELECT username, password FROM Employers WHERE username=?", (username,))
            user = cursor.fetchone()
            
            if user:
                # Check if the hashed password matches
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if hashed_password == user.password:
                    session['username'] = user.username
                    session['role'] = 'employer'
                    return redirect(url_for('create_job_posting'))
                else:
                    flash('Invalid username or password', 'danger')
                    return redirect(url_for('login'))
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))

        elif role == 'jobseeker':
            cursor.execute("SELECT username, password FROM JobSeekers WHERE username=?", (username,))
            user = cursor.fetchone()
            
            if user:
                # Check if the hashed password matches
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if hashed_password == user.password:
                    session['username'] = user.username
                    session['role'] = 'jobseeker'
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password', 'danger')
                    return redirect(url_for('login'))
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
        
        # Close the cursor and database connection
        cursor.close()
        conn.close()
    return render_template('login.html')


@app.route('/logout')
def logout():
    global username
    username = None
    global role
    role=None
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
        role = request.form['role']
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if role == 'employer':
            # Retrieve employer-specific fields
            company_name = request.form['company_name']
            industry = request.form['industry']
            company_size = request.form['company_size']
            website = request.form['website']
            contact_person = request.form['contact_person']
            contact_email = request.form['contact_email']
            contact_phone = request.form['contact_phone']
            company_address = request.form['company_address']
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Employers (username, email, password, company_name, industry, company_size, website, contact_person, contact_email, contact_phone, company_address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (username, email, hashed_password, company_name, industry, company_size, website, contact_person, contact_email, contact_phone, company_address))
        elif role == 'jobseeker':
            # Retrieve jobseeker-specific fields
            full_name = request.form['full_name']
            phone = request.form['phone']
            location = request.form['location']
            occupation = request.form['occupation']
            industry_expertise = request.form['industry_expertise']
            experience_years = request.form['experience_years']
            education = request.form['education']
            skills = request.form['skills']
            certifications = request.form['certifications']
            work_type = request.form['work_type']
            job_categories = request.form['job_categories']
            salary = request.form['salary']
            cursor = conn.cursor()
            cursor.execute("INSERT INTO JobSeekers (username, email, password, full_name, phone, location, occupation, industry_expertise, experience_years, education, skills, certifications, work_type, job_categories, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (username, email, hashed_password, full_name, phone, location, occupation, industry_expertise, experience_years, education, skills, certifications, work_type, job_categories, salary))
        # Printing full_name here will cause UnboundLocalError
        # print(username, email, hashed_password, full_name, phone, location, occupation, industry_expertise, experience_years, education, skills, certifications, work_type, job_categories, salary)
        conn.commit()  # Commit changes to the database
        flash('You have successfully signed up!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/create_job_posting', methods=['GET', 'POST'])
def create_job_posting():
    # Get username and role from session
    username = session.get('username')
    role = session.get('role')  # Retrieve role from session
    if not username or role != 'employer':
        flash('Please log in as an employer to create a job posting.', 'error')
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
            return redirect(url_for('view_postings'))
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT [Title], [Description], [Budget], [Deadline], [Instructions], [ContactInfo], [SalaryBenefits], [UserName] FROM [SKillVista].[dbo].[UserJobPostings]")
            data = cursor.fetchall()
            cursor.close()
            return render_template('create_job_posting.html', job_postings=data)
        except pyodbc.Error as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('view_postings'))


@app.route('/view_postings')
def view_postings():
    username = session.get('username')
    role = session.get('role')
    if not username or role != 'employer':
        cursor = conn.cursor()
        cursor.execute("SELECT JobID, Title, Description, Budget, Deadline, Instructions, ContactInfo, SalaryBenefits FROM [SKillVista].[dbo].[UserJobPostings]")
        all_job_postings = cursor.fetchall()
        cursor.close()
        employer_info = [(job[0], job[1], job[2], job[3]) for job in all_job_postings]
        job_info = [(job[0], job[1], job[2], job[3], job[4], job[5], job[6]) for job in all_job_postings]
        return render_template('view_all_jobes.html', employer_info=employer_info, job_info=job_info)
    else:
        try:
            cursor = conn.cursor()
            # Use parameterized query to prevent SQL injection
            cursor.execute("SELECT * FROM [SKillVista].[dbo].[UserJobPostings] WHERE UserName=?", (username,))
            job_postings = cursor.fetchall()
            cursor.close()
            return render_template('view_postings.html', job_postings=job_postings)
        except pyodbc.Error as e:
            error = str(e)
            # Log the error for debugging purposes
            app.logger.error(f"Error executing SQL query: {error}")
            return render_template('error.html', message=error)



    try:
        #Execute the stored procedure to retrieve all job postings
        cursor = conn.cursor()
        cursor.execute("EXEC RetrieveAllJobPostings")
        all_job_postings = cursor.fetchall()
         # Separate the data into different subsets for different tables
        employer_info = [(job.EmployerUsername, job.EmployerEmail, job.CompanyName, job.Industry) for job in all_job_postings]
        job_info = [(job.JobTitle, job.JobDescription, job.JobBudget, job.JobDeadline, job.JobInstructions, job.JobContactInfo, job.JobSalaryBenefits) for job in all_job_postings]
        # Close the cursor and the database connection
        cursor.close()
        conn.close()
        return render_template('job_details.html', employer_info=employer_info, job_info=job_info)
    except pyodbc.Error as e:
        # Log the error for debugging purposes
        app.logger.error(f"Error executing SQL query: {str(e)}")
        return render_template('error.html', message="An error occurred while retrieving job postings.")


@app.route('/error')
def error():
    """
    Render the error.html template with a default error message.
    """
    return render_template('error.html', message="An unknown error occurred.")


@app.route('/job_details')
def job_details():
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


@app.route('/apply/<int:job_id>')
def apply_job(job_id):
    # Your logic for applying to a job
    return render_template('apply_job.html', job_id=job_id)


@app.route('/submit_application', methods=['POST'])
def submit_application():
    # Logic for submitting the application
    return 'Application submitted successfully'



if __name__ == "__main__":
    app.run(debug=True)