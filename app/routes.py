from app import app
from flask import render_template, request, redirect, url_for, session
from app.models import users

app.secret_key = 'your_secret_key_here'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Credentials'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            error = 'User already exists'
        else:
            users[username] = password
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"Welcome, {session['user']}! You are logged in."

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))
