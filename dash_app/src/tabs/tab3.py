import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, dash_table, Input, Output, State


def get_tab_content():
    tab_content = dbc.Row([
        # Recommended tracks
        dbc.Row([
            dbc.Card([
                dbc.CardHeader(html.H3('Recommended Tracks', className='text-center text-light mb-0')),
                dbc.CardBody(
                    [
                        dbc.Col(
                            id="recommended-tracks"
                        )
                    ]
                )
            ])
        ])
    ])

    return tab_content