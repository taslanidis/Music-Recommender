import dash

from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

# Initialize the Dash app with Bootstrap stylesheet
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/style.css"],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# Define the app layout
app.layout = dbc.Container([
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
        dbc.Col([
            dbc.InputGroup(
                [
                    dbc.Input(id='search-bar', type='text', placeholder='Search...'),
                    dbc.Button('Submit', id='submit-button', color='success')
                ],
                className='mb-3'
            )
        ], width=3),

        # Party settings
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H3('Party Settings', className='text-center text-light mb-0')),
                dbc.CardBody([
                    dbc.FormFloating([
                        dbc.Label('Danceability'),
                        dcc.Dropdown(
                            id='danceability-dropdown',
                            options=[
                                {'label': 'High', 'value': 'high'},
                                {'label': 'Medium', 'value': 'medium'},
                                {'label': 'Low', 'value': 'low'}
                            ],
                            value='medium',
                            className='form-control'
                        )
                    ]),
                    dbc.FormFloating([
                        dbc.Label('Energy'),
                        dcc.Dropdown(
                            id='energy-dropdown',
                            options=[
                                {'label': 'High', 'value': 'high'},
                                {'label': 'Medium', 'value': 'medium'},
                                {'label': 'Low', 'value': 'low'}
                            ],
                            value='medium',
                            className='form-control'
                        )
                    ]),
                    dbc.FormFloating([
                        dbc.Label('Valence'),
                        dcc.Dropdown(
                            id='valence-dropdown',
                            options=[
                                {'label': 'Sad', 'value': 'sad'},
                                {'label': 'Happy', 'value': 'happy'}
                            ],
                            value='happy',
                            className='form-control'
                        )
                    ]),
                    dbc.FormFloating([
                        dbc.Label('Genre'),
                        dcc.Dropdown(
                            id='genre-dropdown',
                            options=[
                                {'label': 'Alternative', 'value': 'alternative'},
                                {'label': 'Blues', 'value': 'blues'},
                                # Add more genres here...
                            ],
                            multi=True,
                            className='form-control'
                        )
                    ])
                ])
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
            dbc.CardBody([
                dbc.Col([
                    html.H3('Recommended Tracks', className='text-light'),
                    # Insert list of recommended tracks here
                ], className='md-6'),
                dbc.Col([
                    dcc.Graph(id='recommended-tracks-graph')
                ], className='md-6')
            ])
        ])
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
