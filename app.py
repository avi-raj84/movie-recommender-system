
import streamlit as st
import pickle
import requests
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

API_KEY = os.getenv("TMDB_API_KEY", "")

@st.cache_data
def load_movies():
    with open("movies.pkl", "rb") as file:
        return pickle.load(file)

movies = load_movies()

if "tags" not in movies.columns:
    st.error("movies.pkl mein 'tags' column nahi mila.")
    st.stop()

@st.cache_resource
def build_model(tags):
    vectorizer = CountVectorizer(
        max_features=5000,
        stop_words="english"
    )
    vectors = vectorizer.fit_transform(tags)

    model = NearestNeighbors(metric="cosine", algorithm="brute")
    model.fit(vectors)
    return model, vectors

tags = movies["tags"].fillna("").astype(str).tolist()
model, vectors = build_model(tags)

def fetch_poster(movie_id):
    if not API_KEY:
        return "https://placehold.co/500x750?text=Poster+Unavailable"

    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{int(movie_id)}",
            params={"api_key": API_KEY, "language": "en-US"},
            timeout=10
        )
        response.raise_for_status()
        path = response.json().get("poster_path")
        if path:
            return "https://image.tmdb.org/t/p/w500" + path
    except (requests.RequestException, ValueError) as e:
        print("Poster error:", e)

    return "https://placehold.co/500x750?text=Poster+Unavailable"

def recommend(movie):
    indices = movies.index[movies["title"] == movie].tolist()
    if not indices:
        return [], []

    movie_index = indices[0]
    count = min(6, len(movies))
    distances, neighbors = model.kneighbors(
        vectors[movie_index], n_neighbors=count
    )

    names, posters = [], []
    for index in neighbors[0]:
        if index == movie_index:
            continue
        row = movies.iloc[index]
        names.append(row["title"])
        posters.append(fetch_poster(row["movie_id"]))
        if len(names) == 5:
            break

    return names, posters

st.title("🎬 Movie Recommender System")
st.write("Select a movie to discover five similar movies!")

selected_movie = st.selectbox("Select a movie", movies["title"].values)

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
