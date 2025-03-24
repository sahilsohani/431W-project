from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

# Database configuration (Update this with your MySQL credentials)
config = {
    'host': 'localhost',    
    'user': 'root',         
    'password': 'password', 
    'database': 'NittanyBusiness'
}

# Function to hash passwords using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to verify user credentials
def verify_user(email, password):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        hashed_password = hash_password(password)
        query = "SELECT * FROM users WHERE email = %s AND password_hash = %s"
        cursor.execute(query, (email, hashed_password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None  # Return True if credentials are correct

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if verify_user(username, password):
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
