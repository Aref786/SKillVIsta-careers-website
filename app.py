from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)

# Database Connection
SERVER='AREF\SQLEXPRESS'
DATABASE="SKillVista"

connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

# Create a connection
conn = pyodbc.connect(connectionString)

@app.route('/')
def baseS():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Entering Posat request!")
        # Get the user's input from the login form
        username = request.form.get('username')
        password = request.form.get('password')

        query = "SELECT * FROM users WHERE username=? AND password=?"
        cursor = conn.cursor()
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        # If the user's credentials are valid, redirect them to their profile page
        if result:
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            # If the user's credentials are invalid, display an error message
            flash('Login failed. Please check your username and password and try again.', 'danger')
            return redirect(url_for('login'))

    else:
        print("Entering Get Request!")
        return render_template('login.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Signup logic
    return render_template('signup.html')

@app.route('/job_details')
def job_details():
    # Logic for job details page
    return render_template('job_details.html')

@app.route('/about')
def about():
    # Logic for the about page
    return render_template('about.html')


@app.route('/profile')
def profile():
    # User profile logic
    return render_template('profile.html')


if __name__ == "__main__":
    app.run(debug=True)