from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '12'

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='todo_db'
    )

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            flash("Username already exists")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            flash("Registered successfully! Please login.")
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        cursor.close()
        conn.close()
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('tasks', user_id=user['id']))
            else:
                flash("Incorrect password")
        else:
            flash("Username not found. Please register.")
            return redirect(url_for('register'))

    return render_template('login.html')

# View Tasks
@app.route('/tasks/<int:user_id>')
def tasks(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash("Unauthorized access.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('tasks.html', tasks=tasks, user_id=user_id)

# Add Task
@app.route('/add_task/<int:user_id>', methods=['GET', 'POST'])
def add_task(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash("Unauthorized access.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        task = request.form['task']
        if task.strip():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (user_id, task) VALUES (%s, %s)", (user_id, task))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('tasks', user_id=user_id))
    return render_template('add_task.html', user_id=user_id)

# Delete Task
@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('tasks', user_id=session['user_id']))

# Complete/Uncomplete Task
@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT completed FROM tasks WHERE id = %s AND user_id = %s", (task_id, session['user_id']))
    result = cursor.fetchone()

    if result is not None:
        new_status = not result['completed']
        cursor.execute("UPDATE tasks SET completed = %s WHERE id = %s", (new_status, task_id))
        conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for('tasks', user_id=session['user_id']))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
