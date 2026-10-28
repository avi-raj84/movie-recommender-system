# Movie Recommendation System

A content-based movie recommendation web app built using Python and Streamlit. Select a movie and the application suggests five similar titles based on movie content.

## Live Demo

[Open Movie Recommender](https://movie-recommender-system-ysrhckqmry2deukptlpa2f.streamlit.app/)

## Overview

I built this project to understand how recommendation systems work and how a machine learning concept can be turned into a usable web application.

The system uses movie tags to find titles with similar content. Recommendations are displayed through a simple interface, with posters fetched from TMDB when available.

## Features

- Select a movie from the available dataset.
- Get five similar movie recommendations.
- View movie posters through the TMDB API.
- Use the application directly in a web browser.
- Find recommendations without needing a user account.

## Technologies Used

- **Python** — Application logic
- **Pandas** — Dataset handling
- **Scikit-learn** — Text vectorization and similarity search
- **Streamlit** — Web interface
- **TMDB API** — Movie poster retrieval
- **Pickle** — Loading the processed movie dataset

## How It Works

1. The application loads the processed movie dataset.
2. Movie tags are converted into numerical vectors using `CountVectorizer`.
3. `NearestNeighbors` with cosine distance identifies movies with similar content.
4. The application displays up to five recommendations.
5. Poster images are retrieved from TMDB when available.

This is a content-based recommendation approach. It compares movie information rather than relying on a user's watch history or ratings.

## Project Structure

```text
movie-recommender-system/
├── app.py
├── movies.pkl
├── requirements.txt
└── README.md
```

## Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/avi-raj84/movie-recommender-system.git
cd movie-recommender-system
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure the TMDB API key**

Set the `TMDB_API_KEY` environment variable before running the app. On Streamlit Community Cloud, add it through the app's Secrets settings.

Do not commit API keys or other credentials to the repository.

**4. Start the application**

```bash
streamlit run app.py
```

## What I Learned

- Building a content-based recommendation system
- Working with text features and cosine distance
- Using Scikit-learn for similarity search
- Connecting a Python application to an external API
- Deploying a Streamlit app

## Author

**Aayush Raj**

- GitHub: [avi-raj84](https://github.com/avi-raj84)
