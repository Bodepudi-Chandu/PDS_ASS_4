import dash
from dash import dcc, html
import requests
import pandas as pd

RAPIDAPI_KEY = '29c4f831cfmsh52dc9590010758dp119888jsn6df53e96b996'

def fetch_anime_data(query='one piece', limit=10, score=8):
    """Fetches anime data from MyAnimeList API based on the search query."""
    url = 'https://myanimelist.p.rapidapi.com/v2/anime/search'
    params = {'q': query, 'n': limit, 'score': score}
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': 'myanimelist.p.rapidapi.com'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return {}

def parse_data_to_df(anime_list):
    """Parses the API response into a Pandas DataFrame."""
    rows = []
    for anime in anime_list:
        
        title = anime.get('title')
        score = anime.get('score')  
        synopsis = anime.get('synopsis')
        rows.append({'Title': title, 'Score': score, 'Synopsis': synopsis})
    return pd.DataFrame(rows)



data = fetch_anime_data('one piece', 10, 8)
df = parse_data_to_df(data)


app = dash.Dash(__name__)


app.layout = html.Div(children=[
    html.H1(children='MyAnimeList Dashboard'),
    html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(len(df))
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)