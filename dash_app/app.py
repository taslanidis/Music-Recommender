from dash import Dash, html, dcc, Input, Output
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
        html.Div(id="client-session-id"),
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
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    children=[
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("@"),
                                dbc.Input(placeholder="Playlist ID", type="string"),
                                dbc.Button("Submit", id="input-group-button", n_clicks=0)
                            ],
                            className="mb-3",
                        )
                    ]
                ),
                dbc.Col(
                    children=[
                        dbc.Button(
                            "Reset listening session",
                            id="reset_listening_session"
                        )
                    ]
                )
            ],
            style={"margin-top": "20px"}
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
                    children=[]
                )
            ]
        ) # output menu
    ],
    fluid=True
)


@app.callback(
    Output('session_statistics_table', 'children'),
    Input('client-session-id', 'children')
)
def update_session_plot_figure(session_id: str = None):
    data = requests.get("http://localhost:8000/session/statistics").json()
    
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
    Input('client-session-id', 'children')
)
def update_session_plot_figure(session_id: str = None):
    data = requests.get("http://localhost:8000/session/clustering/plot").json()
    
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


if __name__ == "__main__":
    app.run_server(debug=True)
