from app import app, db
from app.models import Movie, Theater, Showtime
from datetime import date

with app.app_context():
    # ✅ Optional: Clear existing data
    db.session.query(Showtime).delete()
    db.session.query(Movie).delete()
    db.session.query(Theater).delete()

    # ✅ Add Movies
    movies = [
        Movie(title="RRR", language="Telugu", poster="rrr.jpg", release_date=date(2022, 3, 25), status="Current"),
        Movie(title="KGF 2", language="Kannada", poster="kgf2.jpg", release_date=date(2022, 4, 14), status="Current"),
        Movie(title="Leo", language="Tamil", poster="leo.jpg", release_date=date(2023, 10, 19), status="Upcoming"),
        Movie(title="Jawan", language="Hindi", poster="jawan.jpg", release_date=date(2023, 9, 7), status="Upcoming"),
        Movie(title="Salaar", language="Telugu", poster="salaar.jpg", release_date=date(2023, 12, 22), status="Upcoming"),
    ]

    # ✅ Add Theaters
    theaters = [
        Theater(name="PVR Cinemas", location="Hyderabad"),
        Theater(name="INOX", location="Bangalore"),
        Theater(name="Cinepolis", location="Chennai"),
    ]

    db.session.add_all(movies + theaters)
    db.session.commit()

    # ✅ Add Showtimes
    showtimes = [
        Showtime(movie_id=1, theater_id=1, show_time="6:00 PM", price=150.0),
        Showtime(movie_id=1, theater_id=3, show_time="7:00 PM", price=180.0),
        Showtime(movie_id=2, theater_id=2, show_time="9:00 PM", price=200.0),
    ]

    db.session.add_all(showtimes)
    db.session.commit()

    print("✅ Seed data inserted successfully.")
