from src.content_based import (
    recommend_multiple_movies,
    boost_by_genres
)

from src.collaborative_filtering import (
    recommend_movies_for_user
)


def hybrid_recommend(
    favorite_movies,
    preferred_genres,
    user_id=None,
    top_n=10
):
    """
    Combine:
    1. Content-Based Filtering
    2. Genre Preference Boosting
    3. Collaborative Filtering

    Returns ranked movie recommendations.
    """

    # Generate content-based recommendations
    content_recommendations = (
        recommend_multiple_movies(
            favorite_movies,
            top_n=20
        )
    )

    # Boost scores for preferred genres
    content_recommendations = (
        boost_by_genres(
            content_recommendations,
            preferred_genres
        )
    )

    hybrid_scores = {}

    # Initialize scores using content-based results
    for movie, score in content_recommendations:

        hybrid_scores[movie] = score

    # Add collaborative filtering contribution
    if user_id is not None:

        collaborative_recommendations = (
            recommend_movies_for_user(
                user_id,
                n_recommendations=20
            )
        )

        for movie in collaborative_recommendations:

            # If movie already exists,
            # increase its score
            if movie in hybrid_scores:

                hybrid_scores[movie] += 0.20

            # Otherwise add movie with
            # collaborative score
            else:

                hybrid_scores[movie] = 0.20

    # Sort by final score
    final_recommendations = sorted(
        hybrid_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return final_recommendations[:top_n]


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

    recommendations = hybrid_recommend(
        favorite_movies=favorite_movies,
        preferred_genres=preferred_genres,
        user_id=1,
        top_n=10
    )

    print("\nHYBRID RECOMMENDATIONS\n")

    for movie, score in recommendations:

        print(
            f"{movie} ({score:.3f})"
        )