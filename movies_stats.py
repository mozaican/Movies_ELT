import os
import requests
from dotenv import load_dotenv


load_dotenv()

def get_movies_stats():

    try:
        url = "https://api.themoviedb.org/3/movie/popular"

        token = os.getenv("API_TOKEN")
        if not token:
            raise ValueError("API_TOKEN is not set in the environment")

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url, headers=headers)

        data = response.json()

        movies_stats = []
        for movie in data.get('results', []):
            movie_data = {
                "id": movie.get('id'),
                "title": movie.get('title'),
                "popularity": movie.get('popularity'),
                "vote_average": movie.get('vote_average'),
                "release_date": movie.get('release_date')
            }
            movies_stats.append(movie_data)
            
        return movies_stats

    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    get_movies_stats()

