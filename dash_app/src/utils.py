import requests
import plotly.express as px
import pandas as pd

from dash import html


def ping_backend_alive():
    try:

        r = requests.get("http://localhost:8000/alive", timeout=2)
        return r.status_code == 200
    
    except Exception as e:
        return False
    

def create_music_taste_graph(session_id: str = None):
    
    data = requests.get("http://localhost:8000/session/clustering/plot", timeout=120).json()
    
    for d in data:
        d['tsne_coordinate'] = {'x': d['tsne_coordinate'][0], 'y': d['tsne_coordinate'][1]}
    
    df = pd.json_normalize(data)

    if df.empty:
        return [html.Span("Add tracks to the session to get statistics & recommendations")]

    fig = px.scatter(df, x="tsne_coordinate.x", y="tsne_coordinate.y",
                     color="cluster", hover_name="track_name",
                     title="Input tracks categorized based on multiple characteristics"
                    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=False
    )

    fig.update_layout(transition_duration=200)


def add_to_session(search_value: str):
    response = requests.get(f"http://localhost:8000/session/add/{search_value}", timeout=10)
    success = response.status_code == 200

    return success