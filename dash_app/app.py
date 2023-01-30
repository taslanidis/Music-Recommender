import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "MusicOS - The music recommender"