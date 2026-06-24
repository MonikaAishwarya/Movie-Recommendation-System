import ast
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load processed movie dataset
movies = pd.read_csv(
    "outputs/processed_movies.csv"
)

# Convert movie descriptions into TF-IDF vectors
tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

tfidf_matrix = tfidf.fit_transform(
    movies["tags"]
)

# Compute cosine similarity between all movies
similarity = cosine_similarity(
    tfidf_matrix
)

# Map movie titles to dataframe indices
movie_indices = pd.Series(
    movies.index.values,
    index=movies["title"].str.lower()
)

movie_indices = movie_indices[
    ~movie_indices.index.duplicated(
        keep="first"
    )
]


def recommend_with_scores(
    movie_name,
    top_n=10
):
    """
    Returns recommended movies along with similarity scores.
    """

    movie_name = movie_name.strip().lower()

    if movie_name not in movie_indices.index:
        return []

    movie_idx = movie_indices[movie_name]

    # Handle duplicate movie titles
    if isinstance(movie_idx, pd.Series):
        movie_idx = movie_idx.iloc[0]

    similarity_scores = list(
        enumerate(
            similarity[movie_idx]
        )
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )[1:top_n + 1]

    recommendations = []

    for index, score in similarity_scores:

        recommendations.append(
            (
                movies.iloc[index]["title"],
                float(score)
            )
        )

    return recommendations


def recommend(
    movie_name,
    top_n=10
):
    """
    Returns only movie titles.
    """

    recommendations = recommend_with_scores(
        movie_name,
        top_n
    )

    return [
        movie
        for movie, _
        in recommendations
    ]


def recommend_multiple_movies(
    favorite_movies,
    top_n=20
):
    """
    Generate recommendations based on multiple favorite movies.
    """

    movie_scores = {}
    movie_frequency = {}

    for movie in favorite_movies:

        recommendations = recommend_with_scores(
            movie,
            top_n
        )

        for recommended_movie, score in recommendations:

            movie_scores[
                recommended_movie
            ] = movie_scores.get(
                recommended_movie,
                0
            ) + score

            movie_frequency[
                recommended_movie
            ] = movie_frequency.get(
                recommended_movie,
                0
            ) + 1

    final_scores = {}

    for movie in movie_scores:

        average_score = (
            movie_scores[movie]
            / movie_frequency[movie]
        )

        # Boost movies appearing in recommendations
        # of multiple favorite movies
        frequency_bonus = (
            movie_frequency[movie] - 1
        ) * 0.15

        final_scores[movie] = (
            average_score +
            frequency_bonus
        )

    ranked_movies = sorted(
        final_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_movies[:top_n]


def boost_by_genres(
    recommendations,
    preferred_genres
):
    """
    Increase recommendation scores
    if genres match user preferences.
    """

    preferred_genres = [
        genre.strip().lower()
        for genre in preferred_genres
    ]

    boosted_recommendations = []

    for movie, score in recommendations:

        movie_row = movies[
            movies["title"] == movie
        ]

        if movie_row.empty:
            continue

        genres = ast.literal_eval(
            movie_row.iloc[0]["genres"]
        )

        genres = [
            genre.lower()
            for genre in genres
        ]

        bonus = 0

        for preferred_genre in preferred_genres:

            if preferred_genre in genres:
                bonus += 0.05

        boosted_recommendations.append(
            (
                movie,
                score + bonus
            )
        )

    boosted_recommendations.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return boosted_recommendations


def get_valid_movies(
    movie_list
):
    """
    Return only movies that exist in dataset.
    """

    return [
        movie
        for movie in movie_list
        if movie.strip().lower()
        in movie_indices.index
    ]


if __name__ == "__main__":

    favorite_movies = [
        "Avatar",
        "Interstellar",
        "The Dark Knight"
    ]

    preferred_genres = [
        "Action",
        "Science Fiction"
    ]

    recommendations = (
        recommend_multiple_movies(
            favorite_movies
        )
    )

    recommendations = (
        boost_by_genres(
            recommendations,
            preferred_genres
        )
    )

    print(
        "\nPersonalized Recommendations:\n"
    )

    for movie, score in recommendations:

        print(
            f"{movie} ({score:.3f})"
        )