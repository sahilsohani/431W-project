# NittanyBusiness 

## Overview
A secure web application for user authentication using Flask, MySQL, and Bootstrap.

## Features
- Secure user login
- Password hashing
- Session management
- Responsive design

## Requirements
- Python 3.8+
- MySQL
- Flask
- mysql-connector-python

## Setup
1. Clone the repository
2. Install dependencies: `pip install flask mysql-connector-python`
3. Configure database settings in `app.py`
4. Run database loader: `python loader.py`
5. Start the application: `python app.py`

## Key Files
- `app.py`: Main Flask application
- `loader.py`: Database population script
- `templates/login.html`: Login page
- `templates/dashboard.html`: User dashboard

## Security
- Passwords hashed with SHA-256
- Secure session management

## Running the App
Access the application at `http://localhost:5000`

## License
MIT License
