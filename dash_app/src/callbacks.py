import dash_bootstrap_components as dbc

from dash import dcc, html, Input, Output, State

from src.utils import ping_backend_alive, create_music_taste_graph, add_to_session


class CallbackManager:

    @staticmethod
    def attach_callbacks_to_app(app):

        @app.callback(
            Output('group-music-taste', 'children'),
            Input('client-session-id', 'children')
        )
        def update_session_plot_figure(session_id: str = None):
            
            if not ping_backend_alive():
                return []

            fig = create_music_taste_graph(session_id)

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

                success = True
                if not ping_backend_alive():
                    success = False
                else:
                    success = add_to_session(search_value)
                
                if success:
                    return [dbc.Toast(
                            [html.P("Playlist/track added successfully to the session.")],
                            id="session-add-toast",
                            header="Session Add",
                            icon="success",
                            dismissable=True,
                            is_open=True
                        )]

                return [dbc.Toast(
                            [html.P("Playlist/track failed to be added to the session.")],
                            id="session-add-toast",
                            header="Session Add",
                            icon="warning",
                            dismissable=True,
                            className="warning",
                            is_open=True
                        )]