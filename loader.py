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
csv_file_path = "C:\\Users\\ryany\\OneDrive\\Desktop\\CMPSC431W\\NittanyBusiness\\NittanyBusinessDataset_v3" #USE YOUR PATH TO THE Users.csv FILE

# Function to hash password with SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def insert_user(cursor):
    with open(csv_file_path + "\\Users.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO user (email, password) VALUES (%s, %s)"
        data = [(row[0], hash_password(row[1])) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_helpdesk(cursor):
    with open(csv_file_path + "\\Helpdesk.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO helpdesk (email, position) VALUES (%s, %s)"
        data = [(row[0], row[1]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_zipcode(cursor):
    with open(csv_file_path + "\\Zipcode_Info.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO zipcode (zip_code, city, state) VALUES (%s, %s, %s)"
        data = [(row[0], row[1], row[2]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_address(cursor):
    with open(csv_file_path + "\\Address.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO address (business_address_id, zip_code, building_number, street_name) VALUES (%s, %s, %s, %s)"
        data = [(row[0], row[1], row[2], row[3]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_buyer(cursor):
    with open(csv_file_path + "\\Buyers.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO buyer (email, business_name, business_address_id) VALUES (%s, %s, %s)"
        data = [(row[0], row[1], row[2]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_seller(cursor):
    with open(csv_file_path + "\\Sellers.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO seller (email, business_name, business_address_id, bank_routing_number, bank_account_number, balance) VALUES (%s, %s, %s, %s, %s, %s)"
        data = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_credit_card(cursor):
    with open(csv_file_path + "\\Credit_Cards.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO credit_card (credit_card_num, card_type, expire_month, expire_year, security_code, owner_email) VALUES (%s, %s, %s, %s, %s, %s)"
        data = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_request(cursor):
    with open(csv_file_path + "\\Requests.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO request (request_id, sender_email, helpdesk_staff_email, request_type, request_desc, request_status) VALUES (%s, %s, %s, %s, %s, %s)"
        data = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_category(cursor):
    with open(csv_file_path + "\\Categories.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO category (parent_category, category_name) VALUES (%s, %s)"
        data = [(row[0], row[1]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_product(cursor):
    with open(csv_file_path + "\\Product_Listings.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO product_listing (seller_email, product_id, category, title, name, detail, stock, price, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7].replace("$", "").replace(",", ""), row[8]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_order(cursor):
    with open(csv_file_path + "\\Orders.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO orders (order_id, seller_email, product_id, buyer_email, date, amount, payment) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

def insert_review(cursor):
    with open(csv_file_path + "\\Reviews.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        insert_query = "INSERT INTO review (order_id, rating, text) VALUES (%s, %s, %s)"
        data = [(row[0], row[1], row[2]) for row in csv_reader]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")

# Connect to MySQL
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    # Create users table if not exists
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            email VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HelpDesk (
            email VARCHAR(255) PRIMARY KEY,
            position VARCHAR(255),
            FOREIGN KEY (email) REFERENCES User(email)
            ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ZipCode (
            zip_code VARCHAR(9) PRIMARY KEY,
            state VARCHAR(14),
            city VARCHAR(255)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Address (
            business_address_id VARCHAR(255) PRIMARY KEY,
            building_number VARCHAR(20),
            street_name VARCHAR(255),
            zip_code VARCHAR(10),
            FOREIGN KEY (zip_code) REFERENCES ZipCode(zip_code)
            ON DELETE NO ACTION
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Buyer (
            email VARCHAR(255) PRIMARY KEY,
            business_name VARCHAR(255),
            business_address_id VARCHAR(255),
            FOREIGN KEY (email) REFERENCES User(email),
            FOREIGN KEY (business_address_id) REFERENCES Address(business_address_id)
            ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Seller (
            email VARCHAR(255) PRIMARY KEY,
            business_name VARCHAR(255),
            business_address_id VARCHAR(255),
            bank_routing_number VARCHAR(255),
            bank_account_number VARCHAR(255),
            balance VARCHAR(255),
            FOREIGN KEY (email) REFERENCES User(email),
            FOREIGN KEY (business_address_id) REFERENCES Address(business_address_id)
            ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Credit_Card (
            credit_card_num VARCHAR(255) PRIMARY KEY,
            card_type VARCHAR(255),
            expire_month VARCHAR(2),
            expire_year VARCHAR(4),
            security_code VARCHAR(10),
            owner_email VARCHAR(255),
            FOREIGN KEY (owner_email) REFERENCES Buyer(email)
            ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Request (
            request_id INT,
            sender_email VARCHAR(255),
            helpdesk_staff_email VARCHAR(255),
            request_type VARCHAR(255),
            request_desc VARCHAR(255),
            request_status INT,
            FOREIGN KEY (sender_email) REFERENCES User(email),
            FOREIGN KEY (helpdesk_staff_email) REFERENCES HelpDesk(email)
            ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Category (
            category_name VARCHAR(255) PRIMARY KEY,
            parent_category VARCHAR(255)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Product_Listing (
            product_id INT,
            seller_email VARCHAR(255),
            category VARCHAR(255),
            title VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            detail TEXT,
            stock INT CHECK (stock >= 0),
            price INT,
            status INT,
            PRIMARY KEY (product_id, seller_email),
            FOREIGN KEY (category) REFERENCES Category(category_name),
            FOREIGN KEY (seller_email) REFERENCES Seller(email)
            ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INT PRIMARY KEY,
            seller_email VARCHAR(255),
            product_id INT,
            buyer_email VARCHAR(255),
            date VARCHAR(10),
            amount INT,
            payment INT,
            FOREIGN KEY (buyer_email) REFERENCES Buyer(email),
            FOREIGN KEY (seller_email) REFERENCES Seller(email),
            FOREIGN KEY (product_id) REFERENCES Product_Listing(product_id)
            ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Review (
            order_id INT PRIMARY KEY,
            rating DECIMAL(2,1),
            text VARCHAR(255),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
            ON DELETE CASCADE
        )
    """)
    print("Table created successfully (if not existed).")

    # Read and insert data from CSV
    insert_user(cursor)
    print("inserted user")
    insert_helpdesk(cursor)
    print("inserted helpdesk")
    insert_zipcode(cursor)
    print("inserted zipcode")
    insert_address(cursor)
    print("inserted address")
    insert_buyer(cursor)
    print("inserted buyer")
    insert_seller(cursor)
    print("inserted seller")
    insert_credit_card(cursor)
    print("inserted credit card")
    insert_request(cursor)
    print("inserted request")
    insert_category(cursor)
    print("inserted category")
    insert_product(cursor)
    print("inserted product")
    insert_order(cursor)
    print("inserted order")
    insert_review(cursor)
    print("inserted review")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
