import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[2]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from algoritma.searching import binary_search_by_title, search_by_genre
from algoritma.sorting import sort_by_rating


def _normalize_text(value):
    return str(value or "").strip().lower()


def _get_genres(film):
    genre_text = film.get("genre", "")
    return {_normalize_text(genre) for genre in genre_text.split(",") if genre.strip()}


def recommend_by_genre(films, genre, limit=10):
    matched_films = search_by_genre(films, genre)
    return sort_by_rating(matched_films)[:limit]


def recommend_top_films(films, limit=10, min_rating=0, year_from=None, year_to=None):
    recommendations = []

    for film in films:
        rating = float(film.get("rating", 0))
        year = int(film.get("tahun", 0))

        if rating < min_rating:
            continue
        if year_from is not None and year < int(year_from):
            continue
        if year_to is not None and year > int(year_to):
            continue

        recommendations.append(film)

    return sort_by_rating(recommendations)[:limit]


def recommend_similar_films(films, title, limit=5):
    selected_film = binary_search_by_title(films, title)
    if selected_film is None:
        return []

    selected_genres = _get_genres(selected_film)
    scored_films = []

    for film in films:
        if film.get("id") == selected_film.get("id"):
            continue

        shared_genres = selected_genres.intersection(_get_genres(film))
        if not shared_genres:
            continue

        score = (len(shared_genres) * 2) + float(film.get("rating", 0))
        scored_films.append((score, film))

    scored_films.sort(key=lambda item: item[0], reverse=True)
    return [film for _, film in scored_films[:limit]]


def recommend_by_preferences(films, genres=None, min_rating=0, limit=10):
    genres = genres or []
    selected_films = {}

    for genre in genres:
        for film in search_by_genre(films, genre):
            if float(film.get("rating", 0)) >= min_rating:
                selected_films[film.get("id")] = film

    if not genres:
        selected_films = {
            film.get("id"): film
            for film in films
            if float(film.get("rating", 0)) >= min_rating
        }

    return sort_by_rating(selected_films.values())[:limit]
