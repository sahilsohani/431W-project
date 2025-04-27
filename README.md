# NittanyBusiness Login 

## Project Overview

NittanyBusiness is a Flask-based web application that enables secure user authentication, session management, and user role assignment, backed by a MySQL database and styled with Bootstrap.

## Features

- Email and password-based user registration and login

- Secure password storage using SHA-256 hashing

- Session-based user authentication

- Protected route access (dashboard, profile management, etc.)

- Responsive and mobile-friendly UI with Bootstrap

- Flash messaging for user feedback

- Role-based user redirection (Buyer, Seller, Helpdesk)

## Prerequisites

- Python 3.7+
- MySQL
- MySQL Connector
- Flask

## Installation

1. Ensure MySQL is installed and running

2. Install required Python packages:
```bash
pip install flask mysql-connector-python
```

3. Database Setup:
- Create a MySQL database named `NittanyBusiness`: CREATE DATABASE NittanyBusiness;
- Update database credentials in `app.py` and `loader.py`:
```python
config = {
    'host': 'localhost',    
    'user': 'root',         
    'password': 'password', 
    'database': 'NittanyBusiness'
}
```

4. Populate Users:
- Ensure the CSV file path in `loader.py` is correct
- Run the loader script to populate the database:
```bash
python loader.py
```

## Running the Application

```bash
python app.py
```

Access the application at `http://localhost:5000`

## Project Files

```
.
├── app.py                   # Main Flask application 
├── loader.py                # Database setup and CSV data population script
├── role_required.py         # Role-based access control decorators
├── Address.csv              # CSV datasets 
├── Buyers.csv
├── Categories.csv
├── Credit_Cards.csv
├── Helpdesk.csv
├── Orders.csv
├── Product_Listings.csv
├── Requests.csv
├── Reviews.csv
├── Sellers.csv
├── Users.csv
├── Zipcode_Info.csv
├── templates/               # HTML templates
│   ├── buyer_base.html
│   ├── buyer_dashboard.html
│   ├── buyer_products.html
│   ├── buyer_profile.html
│   ├── buyer_search_results.html
│   ├── buyer_view_cart.html
│   ├── buyer_view_categories.html
│   ├── buyer_view_orders.html
│   ├── category.html
│   ├── checkout.html
│   ├── choose_role.html
│   ├── dashboard.html
│   ├── helpdesk_base.html
│   ├── helpdesk_dashboard.html
│   ├── helpdesk_resolve_requests.html
│   ├── helpdesk_view_requests.html
│   ├── list_product.html
│   ├── login.html
│   ├── register.html
│   ├── seller_base.html
│   ├── seller_dashboard.html
│   ├── seller_edit_product.html
│   ├── seller_list_product.html
│   ├── seller_manage_products.html
│   ├── seller_profile.html
│   ├── seller_view_feedback.html
│   ├── view_cart.html
├── README.md               

``` 

## User Authentication Workflow

1. User submits email and password via login form.

2. Password is hashed (SHA-256) and compared with the database.

3. On success, a session cookie is created.

4. User is redirected to their role-specific dashboard.

5. Logout operation clears the session.

## Security Measures

- Passwords hashed with SHA-256
- Parameterized SQL queries
- Session-based authentication
- Flash messages for login feedback

## Technologies Used

- Python
- Flask
- MySQL
- MySQL Connector
- Bootstrap 5
- SHA-256 Hashing


## Troubleshooting

- Ensure MySQL service is running: 
```bash
brew services start mysql
```
- Verify database credentials
- Check CSV file path in `loader.py`
- Confirm all required packages are installed:
```bash
pip install flask mysql-connector-python



