import streamlit as st
import pickle
import requests

# --------------------------------
# 1. TMDB API KEY
# --------------------------------
API_KEY = "b02e2ad749c79040d0abf4fc44d3ffc4"

# --------------------------------
# 2. FETCH MOVIE POSTER
# --------------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    try:
        response = requests.get(
            url,
            params={"api_key": API_KEY, "language": "en-US"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/original{poster_path}"

        # Try alternative image sizes if the poster path exists
        return "https://placehold.co/500x750?text=Poster+Unavailable"

    except (requests.RequestException, ValueError) as e:
        print(f"Poster fetch failed for movie ID {movie_id}: {e}")
        return "https://placehold.co/500x750?text=Poster+Unavailable"


# --------------------------------
# 3. LOAD DATA
# --------------------------------
@st.cache_resource
def load_data():
    with open("movies.pkl", "rb") as file:
        movies_data = pickle.load(file)

    with open("similarity.pkl", "rb") as file:
        similarity_data = pickle.load(file)

    return movies_data, similarity_data


movies, similarity = load_data()


# --------------------------------
# 4. RECOMMEND MOVIES
# --------------------------------
def recommend(movie):
    movie_indices = movies.index[movies["title"] == movie].tolist()

    if not movie_indices:
        return [], []

    movie_index = movie_indices[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        enumerate(distances),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for index, score in movie_list:
        movie_id = movies.iloc[index]["movie_id"]
        movie_title = movies.iloc[index]["title"]

        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# --------------------------------
# 5. STREAMLIT USER INTERFACE
# --------------------------------
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommender System")
st.write("Select a movie to discover five similar movies!")

selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend", type="primary"):

    with st.spinner("Finding movies for you..."):
        names, posters = recommend(selected_movie)

    if names:
        columns = st.columns(5)

        for col, name, poster in zip(columns, names, posters):
            with col:
                st.subheader(name)
                st.image(poster, use_container_width=True)
    else:
        st.warning("Could not find recommendations for this movie.")

