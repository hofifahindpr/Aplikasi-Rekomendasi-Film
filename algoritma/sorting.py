def _normalize_text(value):
    return str(value or "").strip().lower()


def _get_genres(film):
    genre_text = film.get("genre", "")
    return [_normalize_text(genre) for genre in genre_text.split(",") if genre.strip()]


def _merge(left, right, key, reverse):
    result = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        left_value = key(left[left_index])
        right_value = key(right[right_index])
        should_take_left = left_value >= right_value if reverse else left_value <= right_value

        if should_take_left:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def merge_sort(films, key, reverse=False):
    copied_films = list(films)
    if len(copied_films) <= 1:
        return copied_films

    middle = len(copied_films) // 2
    left = merge_sort(copied_films[:middle], key, reverse)
    right = merge_sort(copied_films[middle:], key, reverse)
    return _merge(left, right, key, reverse)


def sort_by_rating(films, descending=True):
    return merge_sort(films, key=lambda film: float(film.get("rating", 0)), reverse=descending)


def sort_by_year(films, descending=True):
    return merge_sort(films, key=lambda film: int(film.get("tahun", 0)), reverse=descending)


def sort_by_title(films, descending=False):
    return merge_sort(films, key=lambda film: _normalize_text(film.get("judul")), reverse=descending)


def sort_by_genre(films, genre=None, descending=True):
    if not genre:
        return merge_sort(
            films,
            key=lambda film: (_get_genres(film)[0] if _get_genres(film) else "", -float(film.get("rating", 0))),
        )

    target_genre = _normalize_text(genre)
    filtered_films = [
        film for film in films if target_genre in _get_genres(film)
    ]
    return sort_by_rating(filtered_films, descending=descending)
