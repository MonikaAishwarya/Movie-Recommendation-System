from src.hybrid_recommender import (
    hybrid_recommend
)


def main():

    print("=" * 60)
    print("HYBRID MOVIE RECOMMENDATION SYSTEM")
    print("=" * 60)

    # Get favorite movies from user
    favorite_movies_input = input(
        "\nEnter your top favorite movies (comma separated): "
    )

    favorite_movies = [
        movie.strip()
        for movie in favorite_movies_input.split(",")
        if movie.strip()
    ]

    if not favorite_movies:

        print(
            "\nPlease enter at least one movie."
        )

        return

    # Get preferred genres
    preferred_genres_input = input(
        "Enter preferred genres (comma separated): "
    )

    preferred_genres = [
        genre.strip()
        for genre in preferred_genres_input.split(",")
        if genre.strip()
    ]

    # Generate recommendations
    recommendations = hybrid_recommend(
        favorite_movies=favorite_movies,
        preferred_genres=preferred_genres,
        user_id=1,
        top_n=10
    )

    if not recommendations:

        print(
            "\nNo recommendations found."
        )

        return

    print("\n" + "=" * 60)
    print("TOP PERSONALIZED RECOMMENDATIONS")
    print("=" * 60)

    for rank, (movie, score) in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"{rank}. {movie} "
            f"(Score: {score:.3f})"
        )


if __name__ == "__main__":
    main()