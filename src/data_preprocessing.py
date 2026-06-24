import ast
import pandas as pd


# Extract names from JSON-like columns
def convert(text):

    return [
        item["name"]
        for item in ast.literal_eval(text)
    ]


# Extract top 3 cast members
def get_top_cast(text):

    cast_members = []

    for index, item in enumerate(ast.literal_eval(text)):

        if index < 3:
            cast_members.append(item["name"])
        else:
            break

    return cast_members


# Extract director name
def fetch_director(text):

    for item in ast.literal_eval(text):

        if item["job"] == "Director":
            return [item["name"]]

    return []


# Remove spaces from names
def collapse(items):

    return [
        item.replace(" ", "")
        for item in items
    ]


def main():

    # Load TMDB datasets
    movies = pd.read_csv(
        "data/tmdb_5000_movies.csv"
    )

    credits = pd.read_csv(
        "data/tmdb_5000_credits.csv"
    )

    print("Movies Shape:", movies.shape)
    print("Credits Shape:", credits.shape)

    # Merge datasets
    movies = movies.merge(
        credits,
        on="title"
    )

    # Keep only required columns
    movies = movies[
        [
            "movie_id",
            "title",
            "overview",
            "genres",
            "keywords",
            "cast",
            "crew"
        ]
    ]

    # Remove rows with missing values
    movies.dropna(inplace=True)

    print(
        "\nShape After Cleaning:",
        movies.shape
    )

    # Extract useful metadata
    movies["genres"] = movies["genres"].apply(convert)

    movies["keywords"] = movies["keywords"].apply(convert)

    movies["cast"] = movies["cast"].apply(
        get_top_cast
    )

    movies["crew"] = movies["crew"].apply(
        fetch_director
    )

    movies["overview"] = movies["overview"].apply(
        lambda x: x.split()
    )

    # Remove spaces from names
    movies["genres"] = movies["genres"].apply(collapse)

    movies["keywords"] = movies["keywords"].apply(collapse)

    movies["cast"] = movies["cast"].apply(collapse)

    movies["crew"] = movies["crew"].apply(collapse)

    # Combine all features into a single tags column
    movies["tags"] = (
        movies["overview"]
        + movies["genres"]
        + movies["keywords"]
        + movies["cast"]
        + movies["crew"]
    )

    # Final dataset
    processed_movies = movies[
        [
            "movie_id",
            "title",
            "genres",
            "tags"
        ]
    ].copy()

    processed_movies["tags"] = (
        processed_movies["tags"]
        .apply(lambda x: " ".join(x))
        .str.lower()
    )

    # Save processed dataset
    processed_movies.to_csv(
        "outputs/processed_movies.csv",
        index=False
    )

    print("\nProcessed Dataset:")
    print(processed_movies.head())

    print(
        "\nProcessed dataset saved to:"
    )

    print(
        "outputs/processed_movies.csv"
    )


if __name__ == "__main__":
    main()