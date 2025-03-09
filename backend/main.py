from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import random
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

# Sample Movie Data (Ideally use a large-scale dataset) - For Testing Purposes Only 
movies_df = pd.DataFrame([
    {"imdb_id": "tt0816692", "title": "Interstellar", "genre": "Sci-Fi, Adventure", "year": 2014, "rating": 8.6},
    {"imdb_id": "tt1375666", "title": "Inception", "genre": "Sci-Fi, Thriller", "year": 2010, "rating": 8.8},
    {"imdb_id": "tt0468569", "title": "The Dark Knight", "genre": "Action, Drama", "year": 2008, "rating": 9.0},
    {"imdb_id": "tt0120753", "title": "The Million Dollar Hotel", "genre": "Drama, Mystery, Thriller", "year": 2000, "rating": 5.7},
    {"imdb_id": "tt0110912", "title": "Pulp Fiction", "genre": "Crime, Drama", "year": 1994, "rating": 8.9}
])

# Simulated User Ratings (Ideally use a large-scale dataset)
user_movie_ratings = pd.DataFrame([
    {"user_id": 1, "imdb_id": "tt0816692", "rating": 4.5},  # Interstellar
    {"user_id": 1, "imdb_id": "tt1375666", "rating": 4.7},  # Inception
    {"user_id": 2, "imdb_id": "tt0468569", "rating": 5.0},  # The Dark Knight
    {"user_id": 2, "imdb_id": "tt0816692", "rating": 4.8},  # Interstellar
    {"user_id": 3, "imdb_id": "tt0120753", "rating": 3.9},  # The Million Dollar Hotel
])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connect to MongoDB and Fetch Movies Data 
client = MongoClient("mongodb://localhost:27017/")
db = client["imdb_database"]
movies_collection = db["movies"]

# fetch movies from MongoDB database 
def get_movies_from_db(limit=20):
    return list(movies_collection.find({}, {"_id": 0}).limit(limit))

# Load movie data into a DataFrame
movies_df = pd.DataFrame(get_movies_from_db(limit=100))

# Convert genres into a format that can be vectorized
movies_df["genre_str"] = movies_df["genre"].fillna("")

# TF-IDF Vectorization for genres
tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df["genre_str"])

# Fetch IMDb Poster Dynamically
def fetch_imdb_poster(imdb_id):
    """
    Fetches the official movie poster from IMDb movie page dynamically.
    """
    imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        response = requests.get(imdb_url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract poster URL from Open Graph (og:image)
        og_image_tag = soup.find("meta", property="og:image")
        if og_image_tag and og_image_tag["content"]:
            return og_image_tag["content"]

    except requests.RequestException:
        pass  # Ignore errors and use fallback

    return "https://via.placeholder.com/300x450"  # Fallback poster

# Fetch Trending Movies from IMDb
def fetch_trending_movies():
    """
    Scrapes IMDb's Trending Movie List and fetches stable poster URLs.
    """
    url = "https://www.imdb.com/chart/moviemeter/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch trending movies: {e}"}

    soup = BeautifulSoup(response.text, "html.parser")

    trending_movies = []
    movie_items = soup.select("li.ipc-metadata-list-summary-item")[:5]  # Get top 5 movies

    for item in movie_items:
        title_tag = item.select_one("h3.ipc-title__text")
        link_tag = item.select_one("a.ipc-title-link-wrapper")
        rating_tag = item.select_one("span.ipc-rating-star--rating")

        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            imdb_id = link_tag["href"].split("/")[2]  # Extract IMDb ID
            imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
            poster_url = fetch_imdb_poster(imdb_id)  # Fetch dynamic poster
            rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"  # Get rating or show N/A

            trending_movies.append({
                "title": title,
                "poster": poster_url,
                "rating": rating,
                "imdb_url": imdb_url
            })

    return trending_movies if trending_movies else {"error": "Failed to parse trending movies."}

@app.get("/")
def home():
    return {"message": "FastAPI backend is running!"}

@app.get("/movies")
def get_movies():
    """
    Fetches movie list from processed IMDb data with poster URLs.
    """
    movie_list = get_movies_from_db(limit=50)  # Fetch top 50 movies

    # Fetch IMDb Posters for all movies
    for movie in movie_list:
        movie["poster"] = fetch_imdb_poster(movie["imdb_id"])

    return movie_list

# Step 1: Get Genre Matrix for Content-Based Filtering (CBF) 
def get_genre_matrix():
    genres = movies_df["genre"].str.get_dummies(sep=", ")
    return genres

# Step 2: Get Cosine Similarity for Genre-Based Recommendations
def get_cosine_similar_movies(movie_id, top_n=3):
    genre_matrix = get_genre_matrix()
    cosine_sim = cosine_similarity(genre_matrix, genre_matrix)

    # Check if movie_id exists in the DataFrame (for safety)
    if movie_id not in movies_df["imdb_id"].values:
        print(f"⚠ Warning: Movie ID '{movie_id}' not found in movies_df!")
        return []

    movie_idx = movies_df[movies_df["imdb_id"] == movie_id].index

    if len(movie_idx) == 0:
        print(f"⚠ Warning: No index found for Movie ID '{movie_id}'")
        return []

    movie_idx = movie_idx[0]  # Extract index safely
    similar_scores = list(enumerate(cosine_sim[movie_idx]))

    # Sort by similarity score and exclude the movie itself
    similar_movies = sorted(similar_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended_movies = [movies_df.iloc[i[0]].to_dict() for i in similar_movies]

    for movie in recommended_movies:
        movie["reason"] = "🎭 Similar to the movie you liked"

    return recommended_movies


# Step 3: Get User-Movie Matrix for Collaborative Filtering (CF)
def get_user_movie_matrix():
    return user_movie_ratings.pivot(index="user_id", columns="imdb_id", values="rating").fillna(0)

# Step 4: Get Similar Users using Cosine Similarity (Collaborative Filtering)
def get_similar_users(user_id):
    user_movie_matrix = get_user_movie_matrix()
    if user_id not in user_movie_matrix.index:
        return []

    user_similarity = cosine_similarity(user_movie_matrix)
    user_sim_df = pd.DataFrame(user_similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)

    similar_users = user_sim_df[user_id].sort_values(ascending=False).index[1:3].tolist()
    return similar_users

# Step 5: Recommend Movies based on Similar Users (Collaborative Filtering)
def recommend_collaborative(user_id):
    similar_users = get_similar_users(user_id)
    if not similar_users:
        return []

    user_movie_matrix = get_user_movie_matrix()
    similar_users_ratings = user_movie_matrix.loc[similar_users].mean().sort_values(ascending=False)

    watched_movies = user_movie_ratings[user_movie_ratings["user_id"] == user_id]["imdb_id"].tolist()
    recommended_movies = similar_users_ratings.drop(watched_movies).head(3)

    movie_details = [movie for movie in movies_df.to_dict(orient="records") if movie["imdb_id"] in recommended_movies.index]

    for movie in movie_details:
        movie["reason"] = "🧑‍🤝‍🧑 Recommended based on similar users"
    
    return movie_details

# Step 6: Hybrid Recommendation System (Combining CBF & CF)
@app.get("/recommendations/{user_id}")
@app.get("/recommendations/{user_id}")
def recommend_movies(user_id: int):
    """
    Hybrid recommendation combining:
    1. Content-Based Filtering (CBF) - Genre Similarity
    2. Collaborative Filtering (CF) - User Similarity
    3. Cosine Similarity - Movie Feature Similarity
    """

    # Get Watched Movies for the User
    watched_movies = user_movie_ratings[user_movie_ratings["user_id"] == user_id]["imdb_id"].tolist()
    
    if not watched_movies:
        print(f"⚠ Warning: No watched movies found for user {user_id}")
        return {"error": "No watched movies found for this user."}

    print(f"User {user_id} watched: {watched_movies}")

    # Content-Based Filtering: Recommend movies similar to watched ones
    cbf_recommendations = []
    for movie_id in watched_movies:
        recommendations = get_cosine_similar_movies(movie_id, top_n=3)  # Fetch multiple recommendations
        print(f"🎬 Content-Based Recommendations for {movie_id}: {recommendations}")
        cbf_recommendations.extend(recommendations)

    # Collaborative Filtering: Get recommendations from similar users
    cf_recommendations = recommend_collaborative(user_id)
    print(f"🤝 Collaborative Recommendations: {cf_recommendations}")

    # Merge Recommendations & Ensure Uniqueness
    all_recommendations = {movie["imdb_id"]: movie for movie in cbf_recommendations + cf_recommendations}.values()
    print(f"Merged Recommendations (Before Ensuring 5 movies): {all_recommendations}")

    # Ensure at least 5 unique recommendations
    final_recommendations = list(all_recommendations)
    if len(final_recommendations) < 5:
        print(f"⚠ Less than 5 recommendations. Adding more movies.")
        extra_movies = get_movies_from_db(limit=10)  # Fetch more movies if needed
        random.shuffle(extra_movies)
        final_recommendations.extend(extra_movies[:5 - len(final_recommendations)])

    print(f"Final Recommendations (Before Adding Posters): {final_recommendations}")

    # Fetch IMDb Posters for all movies
    for movie in final_recommendations:
        movie["poster"] = fetch_imdb_poster(movie["imdb_id"])  # Fetch IMDb poster
        movie["imdb_url"] = f"https://www.imdb.com/title/{movie['imdb_id']}/"  # Add IMDb Link

    print(f"🎉 Final Recommendations (After Adding Posters): {final_recommendations}")

    return final_recommendations


@app.get("/trending")
def trending_movies():
    """
    Fetches the top trending movies from IMDb Scraping.
    """
    return fetch_trending_movies()
