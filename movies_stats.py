import os
import json
import requests
from datetime import date
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
            movies_stats.append({
                "id": movie.get('id'),
                "title": movie.get('title'),
                "popularity": movie.get('popularity'),
                "vote_average": movie.get('vote_average'),
                "release_date": movie.get('release_date')
            })

        return movies_stats

    except requests.exceptions.RequestException as e:
        raise e
    

def save_to_json(exatracted_data):
    file_path = f"./data/movies_stats_{date.today()}.json"

    with open(file_path, 'w', encoding='utf-8') as json_outfile:
        json.dump(exatracted_data, json_outfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    movies_stats = get_movies_stats()
    save_to_json(movies_stats)

