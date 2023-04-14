import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, dash_table, Input, Output, State

from src import utils


def get_tab_content():
    tab_content = dbc.Row([
        # Current songs
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H3('Group Taste', className='text-center text-light mb-0')),
                dbc.CardBody(
                    [
                        dbc.Col(
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
                        ),
                        dbc.Col(
                            id="group-music-taste"
                        )
                    ]
                )
            ])
        ])
    ])

    return tab_content