import dash_bootstrap_components as dbc
from dash import dcc, html


class Layout:
    def __init__(self, symbol_dict: dict) -> None:
        self._symbol_dict = symbol_dict

        self._stock_options_dropdown = [
            {"label": name, "value": symbol} for symbol, name in symbol_dict.items()
        ]

        self._ohlc_options = [
            {"label": option, "value": option}
            for option in ("open", "high", "low", "close")
        ]

        self._slider_marks = {
            i: mark
            for i, mark in enumerate(
                ["1 day", "1 week", "1 month", "3 months", "1 year", "5 year", "Max"]
            )
        }

    def layout(self):
        return dbc.Container(
            [
                dbc.Card(
                    dbc.CardBody(html.H1("Techy stocks viewer")), className="mt-3"
                ),  # In this card i want my techy stocks viewer
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            html.P("Choose a stock"),
                            className="mt-2",
                            lg="4",
                            xl={"offset": 2, "size": 1},
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="stockpicker-dropdown",
                                options=self._stock_options_dropdown,
                                value="AAPL",
                            ),
                            lg="4",
                            xl="3",
                        ),
                        dbc.Col(
                            dbc.Card(
                                dcc.RadioItems(
                                    id="ohlc-radio",
                                    className="m-1",
                                    options=self._ohlc_options,
                                    value="close",
                                )
                            ),
                            lg="4",
                            xl="3",  # lg står för large screen
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(id="stock-graph"),
                            dcc.Slider(
                                id="time-slider",
                                min=0,
                                max=6,
                                marks=self._slider_marks,
                                value=2,
                                step=None,
                            ),
                        ),
                        dbc.Col(),
                    ]
                ),
                html.P(id="highest-value"),
                html.P(id="lowest-value"),
                # storing intermediate value on clients browser in order to share between several callbacks
                dcc.Store(id="filtered-df"),
            ],  # fluid=True # Om jag sätter denna som true så åker grafen blocket ut i sidorna. Default är 1 enhet på varje sida fri 10 i mitten
        )
