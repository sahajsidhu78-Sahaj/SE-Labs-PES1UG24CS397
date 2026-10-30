"""Movie review and rating board."""

import hashlib
import os
import secrets

STREAM_HOST = "127.0.0.1"
STREAM_PORT = 8000
MODERATOR_PASSWORD = os.environ.get("MODERATOR_PASSWORD", "")

MOVIES = {}


def add_movie(title, genre, year):
    """Add a movie with empty ratings and reviews."""
    MOVIES[title] = {"genre": genre, "year": year,
                     "ratings": [], "reviews": []}


def rate_movie(title, stars, review_text=""):
    """Add a 1-5 star rating (and optional review) to a movie."""
    if title not in MOVIES:
        print("Unknown movie:", title)
        return False
    if not 1 <= stars <= 5:
        print("Rating must be between 1 and 5, got", stars)
        return False
    MOVIES[title]["ratings"].append(stars)
    if review_text:
        MOVIES[title]["reviews"].append(review_text)
    return True


def average_rating(title):
    """Return the average rating of a movie, or 0.0 if unrated."""
    ratings = MOVIES[title]["ratings"]
    if not ratings:
        return 0.0
    return round(sum(ratings) / len(ratings), 1)


def top_movies(count=2):
    """Return the titles of the highest-rated movies."""
    ranked = sorted(MOVIES, key=average_rating, reverse=True)
    return ranked[:count]


def pick_featured():
    """Pick a random movie to feature."""
    return secrets.choice(sorted(MOVIES))


def review_id(title, review_text):
    """Generate a short id for a review."""
    digest = hashlib.sha256((title + review_text).encode()).hexdigest()
    return digest[:10]


def print_all_reviews():
    """Print every movie with its average rating."""
    for i, title in enumerate(MOVIES, start=1):
        print(i, title, average_rating(title))


def stream_address():
    """Return the host:port streaming address."""
    return f"{STREAM_HOST}:{STREAM_PORT}"


def main():
    """Run a short demonstration."""
    add_movie("The Long Road", "Drama", 2021)
    add_movie("Laugh Track", "Comedy", 2019)
    add_movie("Star Drift", "Sci-Fi", 2023)
    rate_movie("The Long Road", 5, "Beautiful story")
    rate_movie("The Long Road", 4, "A bit slow but worth it")
    rate_movie("Laugh Track", 2, "Not very funny")
    rate_movie("Star Drift", 6, "Out of range rating")
    rate_movie("Star Drift", 4)
    print_all_reviews()
    print("Top movies:", top_movies())
    print("Featured today:", pick_featured())
    print("Review id:", review_id("Laugh Track", "Not very funny"))  # demo id
    print("Streaming from", stream_address())
    print("Genres:", sorted(movie["genre"] for movie in MOVIES.values()))


if __name__ == "__main__":
    main()
