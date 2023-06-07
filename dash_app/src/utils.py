import requests
import plotly.express as px
import pandas as pd
import json

from typing import List
from dash import html, dcc


class BackendCommunicator:

    @staticmethod
    def get_session_stats():
        try:

            r = requests.get("http://localhost:8000/session/statistics", timeout=10)
            return r.json()
        
        except Exception as e:
            return {}


    @staticmethod
    def add_user_to_session(user_id: str) -> List[str]:
        try:

            r = requests.get(f"http://localhost:8000/session/users/add/{user_id}", timeout=10)
            return r.json()
        
        except Exception as e:
            return False

    @staticmethod
    def get_active_users() -> List[str]:
        try:

            r = requests.get("http://localhost:8000/session/users/get", timeout=10)
            return r.json()
        
        except Exception as e:
            return []


    @staticmethod
    def ping_backend_alive():
        try:

            r = requests.get("http://localhost:8000/alive", timeout=2)
            return r.status_code == 200
        
        except Exception as e:
            return False
        
    
    @staticmethod
    def generate_recommendations(
        danceability: int,
        valence: int,
        energy: int,
        include_genres: List[str],
        exclude_genres: List[str]
    ):
        
        data = {
            'danceability': danceability if danceability is not None else 4,
            'valence': valence if valence is not None else 4,
            'energy': energy if energy is not None else 4,
            'include_genres': include_genres if include_genres is not None else [],
            'exclude_genres': exclude_genres if exclude_genres is not None else []
        }
        
        try:

            r = requests.post("http://localhost:8000/session/recommendations", data=json.dumps(data), timeout=120)
            return r.status_code == 200
        
        except Exception as e:
            return False
    

    @staticmethod
    def create_music_taste_graph(session_id: str = None):
        
        data = requests.get("http://localhost:8000/session/clustering/plot", timeout=120).json()
        
        for d in data:
            d['tsne_coordinate'] = {'x': d['tsne_coordinate'][0], 'y': d['tsne_coordinate'][1]}
        
        df = pd.json_normalize(data)

        if df.empty:
            return []

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

        return dcc.Graph(figure=fig)


    @staticmethod
    def add_to_session(search_value: str, user_id: str):
        data = {
            "playlist_or_track_id": search_value,
            "provided_by_user_id": user_id
        }
        response = requests.post(url=f"http://localhost:8000/session/add", data=json.dumps(data), timeout=10)
        success = response.status_code == 200

        return success