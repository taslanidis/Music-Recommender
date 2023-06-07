import dash_bootstrap_components as dbc

from dash import dcc, html


features = [('danceability', 'Danceability'), ('energy', 'Energy'), ('valence', 'Valence')]
feature_forms_list = [
    dbc.FormFloating([
        html.P(feature_name, className='p-feature'),
        dcc.Dropdown(
            id=f'{feature_id}-dropdown',
            options=[
                {'label': 'High', 'value': 1},
                {'label': 'Medium', 'value': 2},
                {'label': 'Low', 'value': 3}
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


def get_tab_content():
    tab_content = dbc.Row([
        # Active users in session
        # Party settings
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H3('Active Guests', className='text-center text-light mb-0')),
                dcc.Loading(
                    id="load-spinner-users",
                    type="default",
                    children=[
                        dbc.CardBody(id='active-users')
                    ],
                    className="mt-5"
                )
            ], className='mb-3 h-100')
        ]),
        # Search bar and submit button
        dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(id='active-user-dropdown', placeholder="Select guest...")
                        ),
                        dbc.Col(
                            dbc.Input(id='search-bar', type='text', placeholder='Playlist or track id...'),
                            width=5
                        ),
                        dbc.Col(
                            dbc.Button('Submit', id='submit-button', color='success', className="btn-block w-100")
                        ),
                    ],
                    className="g-0 mb-3"
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
            ],width=6
        ),

        # Party settings
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H3('Party Settings', className='text-center text-light mb-0')),
                dbc.CardBody(
                    feature_forms_list
                )
            ], className='mb-3')
        ])
    ],
    className="justify-content-center")

    return tab_content