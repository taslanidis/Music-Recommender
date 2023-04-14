import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, dash_table, Input, Output, State

from src import utils
from src.tabs import tab1, tab2, tab3

# Initialize the Dash app with Bootstrap stylesheet
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/style.css"],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server


# Define the app layout
app.layout = dbc.Container([
    html.Div(id="client-session-id"),
    # Navbar
    dbc.Navbar(
        dbc.Container(
            [
                html.A('MusicOS', className='navbar-brand')
            ]
        ),
        className='navbar navbar-dark bg-dark mb-3'
    ),

    # Main content
    dbc.Tabs(
        [
            dbc.Tab(tab1.get_tab_content(), label="Control", className="tab-content"),
            dbc.Tab(tab2.get_tab_content(), label="Group Taste", className="tab-content"),
            dbc.Tab(tab3.get_tab_content(), label="Recommendations", className="tab-content"),
        ],
        className="custom-tabs justify-content-center"
    )
])


@app.callback(
    Output('group-music-taste', 'children'),
    Input('client-session-id', 'children')
)
def update_session_plot_figure(session_id: str = None):
    
    if not utils.ping_backend_alive():
        return []

    fig = utils.create_music_taste_graph(session_id)

    return dcc.Graph(id='group_taste_graph_plot', figure=fig)


@app.callback(Output('load-spinner-recommend-output', 'children', allow_duplicate=True),
              [Input('generate-recommendations', 'n_clicks')],
              [State('danceability-dropdown', 'value'),
               State('energy-dropdown', 'value'),
               State('valence-dropdown', 'value'),
               State('include-genre-dropdown', 'value'),
               State('exclude-genre-dropdown', 'value')],
              prevent_initial_call=True)
def update_output_div(n_clicks, danceability, energy, valence, include_genres, exclude_genres):
    if n_clicks is None:
        return None
    else:
        import time
        time.sleep(2)
        
        return [dbc.Toast(
                [html.P("Recommendations generated successfully")],
                id="recommendation-toast",
                header="Recommendations",
                icon="success",
                dismissable=True,
                is_open=True
            )]


@app.callback(Output('load-spinner-recommend-output', 'children', allow_duplicate=True),
              [Input('submit-button', 'n_clicks')],
              [State('search-bar', 'value')],
              prevent_initial_call=True)
def update_output_div_from_search(n_clicks, search_value):
    if n_clicks is None or search_value is None:
        return None
    else:
        import time
        time.sleep(2)
        
        return [dbc.Toast(
                [html.P("Playlist/track added successfully to the session.")],
                id="session-add-toast",
                header="Session Add",
                icon="success",
                dismissable=True,
                is_open=True
            )]


if __name__ == '__main__':
    app.run_server(debug=True)
