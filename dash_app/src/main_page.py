import dash_bootstrap_components as dbc

from dash import html

from src.tabs import tab1, tab2, tab3


class PageCreator:

    @staticmethod
    def get_main_layout():
        return dbc.Container([
            html.Div(id="client-session-id"),
            # Navbar
            dbc.Navbar(
                dbc.Container(
                    [
                        html.A('MusicOS', className='navbar-brand')
                    ]
                ),
                className='navbar navbar-dark bg-dark mb-3'
            ),

            # Main content
            dbc.Tabs(
                [
                    dbc.Tab(tab1.get_tab_content(), label="Control", className="tab-content"),
                    dbc.Tab(tab2.get_tab_content(), label="Group Taste", className="tab-content"),
                    dbc.Tab(tab3.get_tab_content(), label="Recommendations", className="tab-content"),
                ],
                className="custom-tabs justify-content-center"
            )
        ])