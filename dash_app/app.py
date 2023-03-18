from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import requests
import plotly.express as px
import pandas as pd


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "./dash_app/assets/custom.css"],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "MusicOS - The music recommender"

server = app.server

app.layout = dbc.Container(
    children=[
        html.Div(id='hidden_placeholder'),
        html.Div(id='hidden_placeholder_2'),
        html.Div(id="client_session_id"),
        dbc.Row(
            children=[
                dbc.Nav(
                    children=[
                        dbc.Container(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(
                                            "MusicOS",
                                            className="mb-0 h1"
                                        ),
                                        width="auto",
                                        class_name="mr-auto"
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            "A music recommendation software",
                                            className="navbar-text align-center"
                                        ),
                                        width="auto"
                                    )
                                ],
                                justify="between"
                            ),
                            fluid=True
                        )
                    ],
                    class_name="navbar-light bg-light",
                    fill=True
                )
            ]
        ), # menu bar
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Card(
                            [
                                html.H5("Session settings")
                            ],
                            class_name="h-auto border"
                        )
                    ]
                ),
                dbc.Col(
                    children=[
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("@"),
                                dbc.Input(placeholder="Playlist ID", type="string", id="playlist_input"),
                                dbc.Button("Submit", id="input_group_button", n_clicks=0)
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    dbc.Button(
                                        "Generate Recommendations", 
                                        id="generate_recommendations", 
                                        n_clicks=0, 
                                        class_name="btn-dark"
                                    )
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Reset listening session",
                                        id="reset_listening_session",
                                        n_clicks=0,
                                        class_name="align-self-end"
                                    )
                                )
                            ],
                            class_name="justify-content-between"
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Alert(
                            children=[
                                html.P("Successfully added playlist or track")
                            ],
                            id="successful_addition",
                            class_name="alert",
                            dismissable=True,
                            fade=False,
                            is_open=False
                        ),
                        dbc.Alert(
                            children=[
                                html.P("Successfully generated recommendations")
                            ],
                            id="successful_generation",
                            class_name="alert",
                            dismissable=True,
                            fade=False,
                            is_open=False
                        )
                    ]
                ),
                dbc.Col(
                    id="QR-code"
                )
            ],
            style={"margin-top": "20px", "height": "200px"}
        ), # control menu
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Div(id="session_statistics_table"),
                        html.Div(id="session_track_plot")
                    ]
                ),
                dbc.Col(
                    children=[
                        html.Div(id="recommendation_container")
                    ]
                )
            ]
        ) # output menu
    ],
    fluid=True
)


@app.callback(
    Output('session_statistics_table', 'children'),
    Input('client_session_id', 'children')
)
def update_session_stats(session_id: str = None):
    data = requests.get("http://localhost:8000/session/statistics", timeout=120).json()
    
    if len(data) == 0:
        return [html.Span("Add tracks to the session to get statistics & recommendations")]

    rows = [
        dbc.Row(
            [
                dbc.Col([html.H5(key)], class_name="statistics"),
                dbc.Col([html.P(str(value))], class_name="statistics")
            ],
        class_name="statistics"
        ) for key, value in data.items()
    ]

    return rows


@app.callback(
    Output('session_track_plot', 'children'),
    Input('client_session_id', 'children')
)
def update_session_plot_figure(session_id: str = None):
    data = requests.get("http://localhost:8000/session/clustering/plot", timeout=120).json()
    
    for d in data:
        d['tsne_coordinate'] = {'x': d['tsne_coordinate'][0], 'y': d['tsne_coordinate'][1]}
    
    df = pd.json_normalize(data)

    if df.empty:
        return [html.Span("Add tracks to the session to get statistics & recommendations")]

    fig = px.scatter(df, x="tsne_coordinate.x", y="tsne_coordinate.y",
                     color="cluster", hover_name="track_name",
                     title="Input tracks categorized based on multiple characteristics"
                    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=False
    )

    fig.update_layout(transition_duration=200)

    return dcc.Graph(id='graph_session_track_plot', figure=fig)


@app.callback(
    Output('successful_addition', 'is_open'),
    Input('input_group_button', 'n_clicks'),
    State('playlist_input', 'value')
)
def add_playlist_to_session(n_clicks, playlist_input):
    
    if n_clicks == 0:
        return
    
    # TODO: add output to say that a playlist was added successfully
    response = requests.get(f"http://localhost:8000/session/add/{playlist_input}")
    success = response.status_code == 200

    return success


@app.callback(
    Output('successful_generation', 'is_open'),
    Input('reset_listening_session', 'n_clicks')
)
def reset_listening_session(n_clicks):
    
    if n_clicks == 0:
        return

    response = requests.get(f"http://localhost:8000/session/reset")
    success = response.status_code == 200
    
    return success


@app.callback(
    Output('recommendation_container', 'children'),
    Input('generate_recommendations', 'n_clicks')
)
def generate_recommendations(n_clicks):
    
    if n_clicks == 0:
        return

    response = requests.post(f"http://localhost:8000/session/recommendations")
    success = response.status_code == 200
    
    if success:
        response = response.json()

        # TODO: prettify this
        # show table with all recommendations
        return response
    else:
        print(response.json())


def recommendation_statistics():
    # TODO: show some statistics
    pass


if __name__ == "__main__":
    app.run_server(debug=True)
