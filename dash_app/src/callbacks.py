import dash_bootstrap_components as dbc

from dash import dcc, html, Input, Output, State, dash_table

from src.utils import BackendCommunicator


class CallbackManager:

    @staticmethod
    def attach_callbacks_to_app(app):

        EditableDataTableCallbacks.attach_to_app(app)
        MusicTasteGraphCallbacks.attach_to_app(app)

        @app.callback(
            Output('active-users-store', 'data', allow_duplicate=True),
            Input('client-session-id', 'children'),
            prevent_initial_call='initial_duplicate'
        )
        def update_active_users(session_id: str = None):
            
            if not BackendCommunicator.ping_backend_alive():
                return []

            active_user_list = BackendCommunicator.get_active_users()

            return active_user_list
        

        @app.callback(
            Output('active-user-dropdown', 'options'),
            Input('active-users-store', 'data')
        )
        def update_active_user_dropdown(users):
            return users if isinstance(users,list) else []


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
                success = BackendCommunicator.generate_recommendations(
                    danceability=danceability,
                    energy=energy,
                    valence=valence,
                    include_genres=include_genres,
                    exclude_genres=exclude_genres
                )
                
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
            


class EditableDataTableCallbacks:

    @staticmethod
    def attach_to_app(app):

        @app.callback(
            Output('active-users-store', 'data', allow_duplicate=True),
            Input('editing-rows-button', 'n_clicks'),
            State('active-users-store', 'data'),
            State('add-guest-id', 'value'),
            prevent_initial_call=True)
        def add_row_in_store(n_clicks, rows, new_guest_id):
            
            if n_clicks > 0 and new_guest_id is not None and len(new_guest_id) > 0:
                success = BackendCommunicator.add_user_to_session(new_guest_id)
                
                if success:
                    rows.append(new_guest_id)
            
            return rows
        

        @app.callback(
            Output('adding-rows-table', 'data'),
            Input('active-users-store', 'data'))
        def add_row_in_table(users):
            return [{'guestid': user} for user in users]


        @app.callback(
            Output('active-users', 'children'),
            Input('client-session-id', 'children')
        )
        def update_active_users(session_id: str = None):
            
            if not BackendCommunicator.ping_backend_alive():
                return ["Backend is not available at the time. Please try again later..."]

            active_user_list = BackendCommunicator.get_active_users()

            return [
                dbc.InputGroup([
                    dbc.Input(placeholder="Guest...", id="add-guest-id"),
                    dbc.Button('Add', id='editing-rows-button', outline=True, color="secondary", n_clicks=0)
                ],class_name="mb-3"),
                dash_table.DataTable(
                    id="adding-rows-table",
                    data=[{'guestid': guest_id} for guest_id in active_user_list],
                    columns=[{'name': 'Guest Name', 'id': 'guestid'}],
                    editable=True,
                    row_deletable=True,
                    cell_selectable=False
                )
            ]
        

class MusicTasteGraphCallbacks:

    @staticmethod
    def attach_to_app(app):

        @app.callback(
            Output('group-music-taste', 'children'),
            Input('client-session-id', 'children'),
            Input('tabs', 'active_tab'),
            State('group-music-taste', 'children')
        )
        def update_session_plot_figure(session_id: str, selected_tab, result):
            
            if selected_tab != 'tab-1':
                return result
            
            if not BackendCommunicator.ping_backend_alive():
                return []

            graph = BackendCommunicator.create_music_taste_graph(session_id)

            return graph
    

        @app.callback(
            Output('group-music-taste-top-genres', 'children'),
            Input('client-session-id', 'children'),
            Input('tabs', 'active_tab'),
            State('group-music-taste', 'children')
        )
        def update_session_genre_stats(session_id: str, selected_tab, result):
            
            if selected_tab != 'tab-1':
                return result

            if not BackendCommunicator.ping_backend_alive():
                return []

            stats = BackendCommunicator.get_session_stats()

            if len(stats) == 0:
                return html.P("Invite your guests to send spotify music! Current session is empty.")

            return dash_table.DataTable(
                        id='top-genres-table',
                        columns=[
                            {'name': 'Genre', 'id': 'genre'},
                            {'name': 'Frequency', 'id': 'frequency'}
                        ],
                        data=[{'genre': key, 'frequency': value} for key, value in stats['top_genres'].items()],
                        cell_selectable=False
                    )