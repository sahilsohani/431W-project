import mysql.connector
import csv
import hashlib

# Database connection configuration
config = {
    'host': 'localhost',    # Change if MySQL is on a remote server
    'user': 'root',         # Your MySQL username
    'password': 'password', # Your MySQL password
    'database': 'NittanyBusiness'  # Your target database
}

# Path to CSV file
csv_file_path = "C:\\Users\\ryany\\OneDrive\\Desktop\\CMPSC431W\\NittanyBusiness\\NittanyBusinessDataset_v3\\Users.csv" #USE YOUR PATH TO THE Users.csv FILE

# Function to hash password with SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connect to MySQL
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    # Create users table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash CHAR(64) NOT NULL
        )
    """)
    print("Table created successfully (if not existed).")

    # Read and insert data from CSV
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
        data = [(row[0], hash_password(row[1])) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
