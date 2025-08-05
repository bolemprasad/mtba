from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from app.models import Movie, Showtime, User
from app.services.movie_service import fetch_movies_by_language
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            error = 'Username or email already exists'
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('routes.login'))

    return render_template('register.html', error=error)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user'] = user.username
            return redirect(url_for('routes.movie_list'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

@routes.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('routes.login'))
    return render_template('dashboard.html', username=session['user'])

@routes.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('routes.home'))

@routes.route('/movies')
def movie_list():
    if 'user' not in session:
        return redirect(url_for('routes.login'))

    selected_language = request.args.get('lang')
    if selected_language:
        movies = Movie.query.filter_by(language=selected_language).all()
    else:
        movies = Movie.query.all()

    return render_template('movies.html', movies=movies, selected_language=selected_language)

@routes.route('/book/<int:movie_id>', methods=['GET', 'POST'])
def book_movie(movie_id):
    if 'user' not in session:
        return redirect(url_for('routes.login'))

    movie = Movie.query.get_or_404(movie_id)
    showtimes = Showtime.query.filter_by(movie_id=movie.id).all()

    if request.method == 'POST':
        show_id = request.form['show_id']
        seats = request.form['seats']
        # For now, we just print/return a confirmation. Later, store booking in DB.
        return f"Booked {seats} seat(s) for showtime ID {show_id}"

    return render_template('book.html', movie=movie, showtimes=showtimes)


