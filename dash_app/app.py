from dash import Dash, html
import dash_bootstrap_components as dbc


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "MusicOS - The music recommender"

server = app.server

app.layout = dbc.Container(
    children=[
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
            children=[]
        ) # output menu
    ],
    fluid=True
)

if __name__ == "__main__":
    app.run_server(debug=True)
