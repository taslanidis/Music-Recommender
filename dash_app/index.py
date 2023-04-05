import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, dash_table, Input, Output, State

from src import utils


# Initialize the Dash app with Bootstrap stylesheet
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/style.css"],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

features = [('danceability', 'Danceability'), ('energy', 'Energy'), ('valence', 'Valence')]
feature_forms_list = [
    dbc.FormFloating([
        html.P(feature_name, className='p-feature'),
        dcc.Dropdown(
            id=f'{feature_id}-dropdown',
            options=[
                {'label': 'High', 'value': 'high'},
                {'label': 'Medium', 'value': 'medium'},
                {'label': 'Low', 'value': 'low'}
            ],
            clearable=True,
            value=None,
            placeholder="All",
            style={"border": "round"}
        )
        ],
        style={'display': 'grid', 'align-items': 'center'}
    )
    for feature_id, feature_name in features
]

feature_forms_list.extend(
    [
        dbc.FormFloating([
            html.P(f'{mode_name} Genres', className='p-feature'),
            dcc.Dropdown(
                id=f'{mode_id}-genre-dropdown',
                options=[
                    {'label': 'Blues', 'value': 'Blues'},
                    {'label': 'Rock', 'value': 'Rock'},
                    {'label': 'Pop', 'value': 'Pop'}
                ],
                clearable=True,
                value=None,
                multi=True,
                placeholder=placeholder,
                style={"border": "round"}
            )
            ],
            style={'display': 'grid', 'align-items': 'center'}
        )
        for mode_name, mode_id, placeholder in [('Include', 'include', 'All'), ('Exclude', 'exclude', 'None')]
    ]
)


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
    dbc.Row([
        # Search bar and submit button
        dbc.Col(
            [
                dbc.InputGroup(
                    [
                        dbc.Input(id='search-bar', type='text', placeholder='Search...'),
                        dbc.Button('Submit', id='submit-button', color='success')
                    ],
                    className='mb-3'
                ),
                html.Div(
                    dbc.Button('Generate Recommendations', id='generate-recommendations', color='success'),
                    className="d-grid gap-2"
                ),
                dcc.Loading(
                    id="load-spinner-recommend",
                    type="circle",
                    children=[html.Div(children=[], id="load-spinner-recommend-output")],
                    className="mt-5"
                )
            ], 
            width=3
        ),

        # Party settings
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H3('Party Settings', className='text-center text-light mb-0')),
                dbc.CardBody(
                    feature_forms_list
                )
            ], className='mb-3')
        ], width=3),

        # Current songs
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H3('Current Songs', className='text-center text-light mb-0')),
                dbc.CardBody(
                    dash_table.DataTable(
                        id='current-songs-table',
                        columns=[
                            {'name': 'Title', 'id': 'title'},
                            {'name': 'Artist', 'id': 'artist'},
                            {'name': 'Duration', 'id': 'duration'}
                        ],
                        data=[
                            {'title': 'Song 1', 'artist': 'Artist 1', 'duration': '3:45'},
                            {'title': 'Song 2', 'artist': 'Artist 2', 'duration': '4:20'},
                            {'title': 'Song 3', 'artist': 'Artist 3', 'duration': '2:30'}
                        ],
                        style_header={'backgroundColor': '#343a40', 'color': 'white', 'fontWeight': 'bold'},
                        style_cell={
                            'backgroundColor': '#495057',
                            'color': 'white',
                            'textAlign': 'center'
                        },
                        style_data_conditional=[{
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#343a40'
                        }]
                    )
                )
            ])
        ])
    ]),
    # Recommended tracks
    dbc.Row([
        dbc.Card([
            dbc.CardHeader(html.H3('Recommended Tracks', className='text-center text-light mb-0')),
            dbc.CardBody(
                [
                    dbc.Col(
                        id="group-music-taste",
                        className='md-6'
                    ),
                    dbc.Col(
                        id="recommended-tracks",
                        className='md-6'
                    )
                ]
            )
        ])
    ])
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
