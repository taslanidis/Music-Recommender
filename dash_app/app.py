import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "MusicOS - The music recommender"