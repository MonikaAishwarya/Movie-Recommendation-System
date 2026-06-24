import pandas as pd
from sklearn.neighbors import NearestNeighbors


# Load MovieLens datasets
movies = pd.read_csv(
    "data/movies.csv"
)

ratings = pd.read_csv(
    "data/ratings.csv"
)


# Create user-movie rating matrix
user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
).fillna(0)


# Train KNN model using cosine similarity
model = NearestNeighbors(
    metric="cosine",
    algorithm="brute"
)

model.fit(user_movie_matrix)


def get_similar_users(
    user_id,
    n_neighbors=6
):
    """
    Find users with similar rating patterns.
    """

    if user_id not in user_movie_matrix.index:
        return []

    distances, indices = model.kneighbors(
        user_movie_matrix.loc[[user_id]],
        n_neighbors=n_neighbors
    )

    similar_users = user_movie_matrix.index[
        indices.flatten()
    ]

    return similar_users.tolist()


def recommend_movies_for_user(
    user_id,
    n_recommendations=10
):
    """
    Recommend movies liked by users
    with similar preferences.
    """

    if user_id not in user_movie_matrix.index:
        return []

    # Find nearest users
    similar_users = get_similar_users(
        user_id
    )

    # Remove target user
    similar_users = [
        user
        for user in similar_users
        if user != user_id
    ]

    # Movies already watched by target user
    watched_movies = set(
        ratings[
            ratings["userId"] == user_id
        ]["movieId"]
    )

    # Movies highly rated by similar users
    candidate_movies = ratings[
        (ratings["userId"].isin(similar_users))
        &
        (ratings["rating"] >= 4)
    ]

    # Average rating for each movie
    movie_scores = (
        candidate_movies
        .groupby("movieId")["rating"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    recommendations = []

    for movie_id in movie_scores.index:

        if movie_id in watched_movies:
            continue

        movie_title = movies[
            movies["movieId"] == movie_id
        ]["title"]

        if not movie_title.empty:

            recommendations.append(
                movie_title.values[0]
            )

        if len(recommendations) >= n_recommendations:
            break

    return recommendations


if __name__ == "__main__":

    user_id = 1

    print(
        f"\nSimilar Users to User {user_id}:"
    )

    print(
        get_similar_users(user_id)
    )

    print(
        f"\nRecommendations for User {user_id}:\n"
    )

    for movie in recommend_movies_for_user(
        user_id
    ):
        print(movie)