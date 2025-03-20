import mysql.connector
import hashlib

# Database connection configuration
config = {
    'host': 'localhost',    
    'user': 'root',         
    'password': 'password', 
    'database': 'NittanyBusiness'
}

# Function to hash password with SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check email-password combination
def verify_user(email, password):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Hash the input password
        hashed_password = hash_password(password)

        # Search for user with given email and hashed password
        query = "SELECT * FROM users WHERE email = %s AND password_hash = %s"
        cursor.execute(query, (email, hashed_password))
        result = cursor.fetchone()

        if result:
            print("✅ Login successful!")
        else:
            print("❌ Invalid email or password.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()

# Example usage
email_input = input("Enter your email: ")
password_input = input("Enter your password: ")
verify_user(email_input, password_input)
