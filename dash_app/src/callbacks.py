import dash_bootstrap_components as dbc

from dash import dcc, html, Input, Output, State, dash_table

from src.utils import BackendCommunicator


class CallbackManager:

    @staticmethod
    def attach_callbacks_to_app(app):

        @app.callback(
            Output('active-users', 'children'),
            Input('client-session-id', 'children')
        )
        def update_active_users(session_id: str = None):
            
            if not BackendCommunicator.ping_backend_alive():
                return []

            active_user_list = BackendCommunicator.get_active_users()

            if len(active_user_list) > 0:
                return dash_table.DataTable(
                    data=[{'guestid': guest_id} for guest_id in active_user_list],
                    columns=[{'name': 'GuestID', 'id': 'guestid'}],
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

            return html.P("No active guests yet. Invite them to Join!")
        

        @app.callback(
            Output('active-user-dropdown', 'options'),
            Input('client-session-id', 'children')
        )
        def update_active_user_dropdown(session_id: str = None):
            
            if not BackendCommunicator.ping_backend_alive():
                return []

            active_user_list = BackendCommunicator.get_active_users()

            return active_user_list


        @app.callback(
            Output('group-music-taste', 'children'),
            Input('client-session-id', 'children')
        )
        def update_session_plot_figure(session_id: str = None):
            
            if not BackendCommunicator.ping_backend_alive():
                return []

            graph = BackendCommunicator.create_music_taste_graph(session_id)

            return graph


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
                success = BackendCommunicator.generate_recommendations()
                
                if success:
                    return [dbc.Toast(
                        [html.P("Recommendations generated successfully")],
                        id="recommendation-toast",
                        header="Recommendations",
                        icon="success",
                        dismissable=True,
                        is_open=True
                    )]

                return [dbc.Toast(
                    [html.P("Recommendations failed to generate")],
                    id="recommendation-toast",
                    header="Recommendations",
                    icon="warning",
                    className="warning",
                    dismissable=True,
                    is_open=True
                )]


        @app.callback(Output('load-spinner-recommend-output', 'children', allow_duplicate=True),
                    [Input('submit-button', 'n_clicks')],
                    [State('search-bar', 'value'), State('active-user-dropdown', 'value')],
                    prevent_initial_call=True)
        def update_output_div_from_search(n_clicks, search_value, user_id):
            if n_clicks is None or search_value is None:
                return None
            else:

                success = True
                if not BackendCommunicator.ping_backend_alive():
                    success = False
                else:
                    success = BackendCommunicator.add_to_session(search_value, user_id)
                
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