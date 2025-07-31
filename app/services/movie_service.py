import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Ensure .env variables are loaded

def fetch_movies_by_language(lang="te", query="", category="now_playing"):
    # ✅ Load API key inside the function
    API_KEY = os.getenv("TMDB_API_KEY")

    if not API_KEY:
        print("❌ TMDB_API_KEY not found.")
        return []

    language_codes = {
        "english": "en",
        "telugu": "te",
        "tamil": "ta",
        "hindi": "hi",
        "malayalam": "ml",
        "kannada": "kn"
    }

    lang_code = language_codes.get(lang.lower(), "")

    # 🧠 Determine URL
    if query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=en-US&query={query}&region=IN"
    elif lang_code:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=en-US&region=IN&with_original_language={lang_code}&sort_by=release_date.desc&page=1"
    else:
        url = f"https://api.themoviedb.org/3/movie/{category}?api_key={API_KEY}&language=en-US&region=IN&page=1"

    print("🔍 Final API URL:", url)  # Debug

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        print("✅ Fetched", len(results), "movies")

        movies = []
        for movie in results:
            if movie.get("poster_path"):
                movies.append({
                    "id": movie["id"],
                    "name": movie["title"],
                    "description": movie["overview"],
                    "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                })

        print("✅ Parsed movies:", len(movies))
        return movies

    except requests.exceptions.RequestException as e:
        print("❌ Error fetching movies:", e)
        return []

def fetch_movie_by_id(movie_id):
    API_KEY = os.getenv("TMDB_API_KEY")
    if not API_KEY:
        print("❌ TMDB_API_KEY not found.")
        return None

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie = response.json()
        return {
            'id': movie['id'],
            'name': movie['title'],
            'description': movie['overview'],
            'poster': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else ""
        }
    except Exception as e:
        print("❌ Error fetching movie by ID:", e)
        return None
