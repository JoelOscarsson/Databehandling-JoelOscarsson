from dash import html, dcc


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
        return html.Main(
            [
                html.H1("Techy stocks viewer"),
                html.P("Choose a stock"),
                dcc.Dropdown(
                    id="stockpicker-dropdown",
                    options=self._stock_options_dropdown,
                    value="AAPL",
                ),
                html.P(id="highest-value"),
                html.P(id="lowest-value"),
                dcc.RadioItems(
                    id="ohlc-radio", options=self._ohlc_options, value="close"
                ),
                dcc.Graph(id="stock-graph"),
                dcc.Slider(
                    id="time-slider",
                    min=0,
                    max=6,
                    marks=self._slider_marks,
                    value=2,
                    step=None,
                ),
                # storing intermediate value on clients browser in order to share between several callbacks
                dcc.Store(id="filtered-df"),
            ]
        )
