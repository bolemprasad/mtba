# populate_movies.py

from app import create_app, db
from app.models import Movie
from app.services.movie_service import fetch_movies_by_language
from datetime import datetime

app = create_app()  # ✅ You were missing this line

with app.app_context():
    movies = fetch_movies_by_language(lang="te", category="now_playing")
    print(f"🔍 Found {len(movies)} movies")

    for m in movies:
        title = m.get("title") or m.get("name")  # Support both keys
        if not title or not m.get("poster"):
            print(f"⚠️ Skipping invalid movie entry: {m}")
            continue

        exists = Movie.query.filter_by(title=title).first()
        if not exists:
            new_movie = Movie(
                title=title,
                language=m.get("language", "unknown"),
                poster=m["poster"],
                release_date=datetime.strptime(m["release_date"], "%Y-%m-%d") if m.get("release_date") else datetime.utcnow(),
                status=m.get("status", "unknown"),
                description=m.get("description", "No description available")
            )
            db.session.add(new_movie)

    db.session.commit()
    print("✅ Movies added to the database.")
