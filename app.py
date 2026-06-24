import streamlit as st

from src.hybrid_recommender import hybrid_recommend


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Hybrid Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------
# Sidebar
# --------------------------------

st.sidebar.title("🎬 About")

st.sidebar.info(
    """
    Hybrid Movie Recommendation System

    Technologies Used:
    - Python
    - Pandas
    - Scikit-Learn
    - TF-IDF Vectorization
    - Cosine Similarity
    - K-Nearest Neighbors (KNN)
    - Streamlit

    Recommendation Techniques:
    - Content-Based Filtering
    - Collaborative Filtering
    - Hybrid Recommendation System
    """
)

# --------------------------------
# Main Title
# --------------------------------

st.title("🎬 Hybrid Movie Recommendation System")

st.write(
    """
    Discover movies based on your favorite films and genre preferences.

    This recommendation engine combines Content-Based Filtering and
    Collaborative Filtering to generate personalized suggestions.
    """
)

# --------------------------------
# User Inputs
# --------------------------------

favorite_movies = st.text_input(
    "Enter Favorite Movies (comma separated)",
    placeholder="Avatar, Interstellar, The Dark Knight"
)

preferred_genres = st.text_input(
    "Enter Preferred Genres (comma separated)",
    placeholder="Action, Science Fiction"
)

# --------------------------------
# Recommendation Button
# --------------------------------

if st.button("🚀 Recommend Movies"):

    if not favorite_movies.strip():

        st.warning(
            "Please enter at least one favorite movie."
        )

    else:

        favorite_movies = [
            movie.strip()
            for movie in favorite_movies.split(",")
            if movie.strip()
        ]

        preferred_genres = [
            genre.strip()
            for genre in preferred_genres.split(",")
            if genre.strip()
        ]

        with st.spinner(
            "Generating recommendations..."
        ):

            recommendations = hybrid_recommend(
                favorite_movies=favorite_movies,
                preferred_genres=preferred_genres,
                user_id=1,
                top_n=10
            )

        if not recommendations:

            st.error(
                "No recommendations found."
            )

        else:

            st.success(
                f"Found {len(recommendations)} recommendations."
            )

            st.subheader(
                "🎥 Recommended Movies"
            )

            for rank, (movie, score) in enumerate(
                recommendations,
                start=1
            ):

                st.markdown(
                    f"""
                    ### {rank}. {movie}

                    Recommendation Score: **{score:.3f}**
                    """
                )

                st.divider()

# --------------------------------
# Footer
# --------------------------------

st.markdown("---")

st.caption(
    "Developed by VEGESNA MONIKA AISHWARYA | "
    "Hybrid Movie Recommendation System"
)