# NittanyBusiness Login 

## Project Overview

NittanyBusiness is a Flask-based web application providing secure user authentication using MySQL and Bootstrap.

## Features

- User authentication with email and password
- Secure password hashing (SHA-256)
- Session-based login management
- Responsive Bootstrap interface
- Protected dashboard route
- User logout functionality

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
- Create a MySQL database named `NittanyBusiness`
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
├── app.py          # Main Flask application
├── loader.py       # Database population script
└── templates/
    ├── login.html      # Login page template
    └── dashboard.html  # Dashboard template
```

## User Authentication Workflow

1. User enters email and password
2. Credentials are hashed and verified against database
3. Successful login creates a session
4. User redirected to dashboard
5. Logout destroys the session

## Security Measures

- Passwords hashed with SHA-256
- Parameterized SQL queries
- Session-based authentication
- Flash messages for login feedback

## Technologies

- Python
- Flask
- MySQL
- MySQL Connector
- Bootstrap 5
- SHA-256 Hashing


## Troubleshooting

- Ensure MySQL service is running
- Verify database credentials
- Check CSV file path in `loader.py`
- Confirm all required packages are installed



