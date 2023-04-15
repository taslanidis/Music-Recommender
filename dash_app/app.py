import dash_bootstrap_components as dbc

from dash import Dash


# Initialize the Dash app with Bootstrap stylesheet
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/style.css"],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    #suppress_callback_exceptions=True
)
server = app.server