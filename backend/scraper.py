import requests
from bs4 import BeautifulSoup

def get_trending_movies():
    url = "https://www.imdb.com/chart/moviemeter/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    movies = []
    for item in soup.select(".titleColumn a"):
        movies.append(item.get_text())
    
    return movies[:10]  # Return top 10 trending

@app.get("/trending")
def trending_movies():
    return get_trending_movies()
