import os
import requests
from datetime import datetime
from dotenv import load_dotenv

from app import create_app, db
from app.models import Movie, Theater, Showtime

load_dotenv()

app = create_app()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def fetch_movies(language="te"):
    print("⏳ Fetching movies from TMDb...")
    url = f"https://api.themoviedb.org/3/movie/now_playing?language={language}&page=1&api_key={TMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("results", [])

with app.app_context():
    db.create_all()

    if Movie.query.count() == 0:
        movies = fetch_movies(language="te")  # Telugu movies

        for m in movies[:5]:
            title = m["title"]
            lang = "Telugu"
            release_date_str = m.get("release_date", "2024-01-01")
            release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
            poster_path = m.get("poster_path", "")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

            print(f"▶️ {title} | Poster URL: {poster_url}")

            movie = Movie(
                title=title,
                language=lang,
                poster=poster_url,
                release_date=release_date,
                status="Current"
            )
            db.session.add(movie)
            db.session.flush()

            # Add sample theaters
            t1 = Theater(name="PVR Hyderabad", location="Hyderabad")
            t2 = Theater(name="INOX GVK", location="Hyderabad")
            db.session.add_all([t1, t2])
            db.session.flush()

            # Add showtimes
            show1 = Showtime(movie_id=movie.id, theater_id=t1.id, show_time="10:00 AM", price=180.0)
            show2 = Showtime(movie_id=movie.id, theater_id=t2.id, show_time="1:00 PM", price=200.0)

            db.session.add_all([show1, show2])

        db.session.commit()
        print("✅ Database initialized with TMDb movies and showtimes.")
    else:
        print("ℹ️ Movies already exist in the database.")
