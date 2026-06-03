from .sorting import sort_by_title


def _normalize_text(value):
    return str(value or "").strip().lower()


def _get_genres(film):
    genre_text = film.get("genre", "")
    return [_normalize_text(genre) for genre in genre_text.split(",") if genre.strip()]


def search_by_title(films, keyword):
    keyword = _normalize_text(keyword)
    if not keyword:
        return []

    return [
        film for film in films
        if keyword in _normalize_text(film.get("judul"))
    ]


def search_by_genre(films, genre):
    genre = _normalize_text(genre)
    if not genre:
        return []

    return [
        film for film in films
        if genre in _get_genres(film)
    ]


def search_by_year(films, year):
    try:
        target_year = int(year)
    except (TypeError, ValueError):
        return []

    return [
        film for film in films
        if int(film.get("tahun", 0)) == target_year
    ]


def search_by_director(films, keyword):
    keyword = _normalize_text(keyword)
    if not keyword:
        return []

    return [
        film for film in films
        if keyword in _normalize_text(film.get("sutradara"))
    ]


def binary_search_by_title(films, title):
    sorted_films = sort_by_title(films)
    target_title = _normalize_text(title)
    low = 0
    high = len(sorted_films) - 1

    while low <= high:
        middle = (low + high) // 2
        current_title = _normalize_text(sorted_films[middle].get("judul"))

        if current_title == target_title:
            return sorted_films[middle]
        if current_title < target_title:
            low = middle + 1
        else:
            high = middle - 1

    return None
