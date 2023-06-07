import dash_bootstrap_components as dbc

from dash import html, dcc


def get_tab_content():
    tab_content = dbc.Row([
        # Current songs
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H3('Group Taste', className='text-center text-light mb-0')),
                dbc.CardBody(
                    [
                        dcc.Loading(
                            dbc.Col(
                                id="group-music-taste-top-genres"
                            ),
                            type="graph"
                        ),
                        dbc.Col(
                            id="group-music-taste"
                        )
                    ]
                )
            ],
            class_name="graphcard")
        ])
    ])

    return tab_content