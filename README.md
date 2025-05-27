# Flask To-Do App

A simple To-Do web application built using Python Flask and MySQL. Users can register, log in, add tasks, mark them as complete/incomplete, and delete them.

## Features

- User registration and login with password hashing
- Session management using Flask sessions
- Add, view, complete, and delete personal tasks
- MySQL database integration

## Requirements

- Python 3.x
- Flask
- MySQL Server
- mysql-connector-python
- Werkzeug

## Installation

1. **Clone the repository:**
git clone https://github.com/MAHIMA-0/flask-todo-app.git
 flask-todo-app
Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
Install dependencies:
pip install flask mysql-connector-python werkzeug
Set up the MySQL database:

Open MySQL and run the following SQL commands:

CREATE DATABASE todo_db;

USE todo_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    task TEXT,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

Run the Flask app:
python app.py
Access the app:

Open your browser and visit: http://127.0.0.1:5000

File Structure

.
├── app.py
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── tasks.html
│   └── add_task.html
├── static/
│   └── (optional CSS files)
└── README.md

