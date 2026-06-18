import pandas as pd


def clean_movie_data(data):
    df = pd.DataFrame(data)
    df = df.dropna(subset=['id'])
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['popularity'] = df['popularity'].fillna(0)
    df = df.drop_duplicates(subset=['id'])
    return df


def add_features(df):
    current_year = 2026
    df['movie_age'] = current_year - df['release_date'].dt.year
    
    df['popularity_tier'] = pd.cut(
        df['popularity'], 
        bins=[0, 10, 50, float('inf')], 
        labels=['Niche', 'Popular', 'Blockbuster']
    )
    return df