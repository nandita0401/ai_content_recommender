from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ IMDb Movie Data with Permanent IMDb URLs
movies = [
    {"id": 1, "title": "Inception", "genre": "Sci-Fi", "rating": 8.8, "imdb_id": "tt1375666"},
    {"id": 2, "title": "The Dark Knight", "genre": "Action", "rating": 9.0, "imdb_id": "tt0468569"},
    {"id": 3, "title": "Interstellar", "genre": "Sci-Fi", "rating": 8.6, "imdb_id": "tt0816692"},
]


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

        # ✅ Extract permanent poster URL from Open Graph meta tag
        og_image_tag = soup.find("meta", property="og:image")
        if og_image_tag and og_image_tag["content"]:
            return og_image_tag["content"]

    except requests.RequestException:
        pass  # Ignore errors and use fallback

    return "https://via.placeholder.com/300x450"  # Fallback poster



@app.get("/")
def home():
    return {"message": "FastAPI backend is running!"}


@app.get("/movies")
def get_movies():
    """
    Fetches movie list with fresh IMDb poster URLs.
    """
    movie_list = []
    for movie in movies:
        movie_list.append({
            "id": movie["id"],
            "title": movie["title"],
            "genre": movie["genre"],
            "rating": movie["rating"],
            "poster": fetch_imdb_poster(movie["imdb_id"]),
            "imdb_url": f"https://www.imdb.com/title/{movie['imdb_id']}/"
        })
    return movie_list




@app.get("/recommendations/{user_id}")
def recommend_movies(user_id: int):
    """
    Returns 2 random movies with personalized recommendations.
    """
    explanations = {
        1: "You like Sci-Fi thrillers",
        2: "You enjoy action-packed movies",
        3: "You prefer mind-bending narratives"
    }

    recommended = random.sample(movies, 2)

    recommended_movies = []
    for movie in recommended:
        recommended_movies.append({
            "id": movie["id"],
            "title": movie["title"],
            "genre": movie["genre"],
            "rating": movie["rating"],
            "poster": fetch_imdb_poster(movie["imdb_id"]),
            "imdb_url": f"https://www.imdb.com/title/{movie['imdb_id']}/",
            "reason": explanations.get(movie["id"], "Recommended for you")
        })

    return recommended_movies


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


@app.get("/trending")
def trending_movies():
    return fetch_trending_movies()
