import ast
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# LOAD DATA
# =========================
movies = pd.read_csv("outputs/processed_movies.csv")

# Clean titles (VERY IMPORTANT for deployment)
movies["title"] = movies["title"].astype(str).str.strip()
movies["clean_title"] = movies["title"].str.lower().str.strip()


# =========================
# TF-IDF MATRIX
# =========================
tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

tfidf_matrix = tfidf.fit_transform(movies["tags"])

# Cosine similarity matrix
similarity = cosine_similarity(tfidf_matrix)


# =========================
# MOVIE INDEX MAP
# =========================
movie_indices = pd.Series(
    movies.index,
    index=movies["clean_title"]
)

# Remove duplicates safely
movie_indices = movie_indices[~movie_indices.index.duplicated(keep="first")]


# =========================
# CONTENT BASED CORE
# =========================
def recommend_with_scores(movie_name, top_n=10):
    """
    Returns recommended movies with similarity scores.
    """

    movie_name = movie_name.strip().lower()

    if movie_name not in movie_indices:
        return []

    movie_idx = movie_indices[movie_name]

    # safety check (important for cloud runtime)
    if movie_idx is None or movie_idx >= len(similarity):
        return []

    similarity_vector = similarity[movie_idx]

    # Convert to safe Python floats
    similarity_scores = []

    for idx, score in enumerate(similarity_vector):
        similarity_scores.append((idx, float(score)))

    # Sort safely
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )[1:top_n + 1]

    recommendations = []

    for index, score in similarity_scores:
        recommendations.append(
            (movies.iloc[index]["title"], score)
        )

    return recommendations


# =========================
# SIMPLE RECOMMEND
# =========================
def recommend(movie_name, top_n=10):
    """
    Return only movie titles.
    """

    results = recommend_with_scores(movie_name, top_n)

    return [movie for movie, _ in results]


# =========================
# MULTI-MOVIE RECOMMEND
# =========================
def recommend_multiple_movies(favorite_movies, top_n=20):
    """
    Combine recommendations from multiple movies.
    """

    movie_scores = {}
    movie_frequency = {}

    for movie in favorite_movies:

        recommendations = recommend_with_scores(movie, top_n)

        for rec_movie, score in recommendations:

            movie_scores[rec_movie] = movie_scores.get(rec_movie, 0) + score
            movie_frequency[rec_movie] = movie_frequency.get(rec_movie, 0) + 1

    final_scores = {}

    for movie in movie_scores:

        avg_score = movie_scores[movie] / movie_frequency[movie]

        frequency_bonus = (movie_frequency[movie] - 1) * 0.15

        final_scores[movie] = avg_score + frequency_bonus

    ranked_movies = sorted(
        final_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_movies[:top_n]


# =========================
# GENRE BOOSTING
# =========================
def boost_by_genres(recommendations, preferred_genres):
    """
    Boost scores if genres match user preference.
    """

    preferred_genres = [
        g.strip().lower()
        for g in preferred_genres
    ]

    boosted = []

    for movie, score in recommendations:

        movie_row = movies[movies["title"] == movie]

        if movie_row.empty:
            continue

        genres = ast.literal_eval(movie_row.iloc[0]["genres"])
        genres = [g.lower() for g in genres]

        bonus = 0

        for genre in preferred_genres:
            if genre in genres:
                bonus += 0.05

        boosted.append((movie, score + bonus))

    return sorted(boosted, key=lambda x: x[1], reverse=True)


# =========================
# VALID MOVIE CHECK
# =========================
def get_valid_movies(movie_list):
    """
    Filter only movies that exist in dataset.
    """

    valid_movies = []

    for movie in movie_list:
        clean = movie.strip().lower()

        if clean in movie_indices:
            valid_movies.append(movie.strip())

    return valid_movies


# =========================
# TEST RUN
# =========================
if __name__ == "__main__":

    favorites = ["Avatar", "Interstellar", "The Dark Knight"]

    genres = ["Action", "Science Fiction"]

    recs = recommend_multiple_movies(favorites)
    recs = boost_by_genres(recs, genres)

    print("\nPersonalized Recommendations:\n")

    for movie, score in recs:
        print(movie, round(score, 3))