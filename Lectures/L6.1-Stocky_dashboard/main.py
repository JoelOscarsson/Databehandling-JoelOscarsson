import dash
import dash_bootstrap_components as dbc
import os
from load_data import StockData
from dash import html, dcc  # dcc - dash core components
from dash.dependencies import Output, Input
import plotly_express as px
from time_filtering import filter_time
import pandas as pd

directory_path = os.path.dirname(__file__)
path = os.path.join(directory_path, "stocksdata")

print(path)

stockdata_object = StockData(path)

# pick one stock
# print(stockdata_object.stock_dataframe("AAPL"))

symbol_dict = {"AAPL": "Apple", "NVDA": "Nvidia", "TSLA": "Tesla", "IBM": "IBM"}

df_dict = {symbol: stockdata_object.stock_dataframe(symbol) for symbol in symbol_dict}

stock_options_dropdown = [
    {"label": name, "value": symbol} for symbol, name in symbol_dict.items()
]

ohlc_options = [
    {"label": option, "value": option} for option in ("open", "high", "low", "close")
]

slider_marks = {
    i: mark
    for i, mark in enumerate(
        ["1 day", "1 week", "1 month", "3 months", "1 year", "5 year", "Max"]
    )
}

print(df_dict.keys())
# print(df_dict["TSLA"][0])

# create a Dash App
app = dash.Dash(__name__)

app.layout = html.Main(
    [
        html.H1("Techy stocks viewer"),
        html.P("Choose a stock"),
        dcc.Dropdown(
            id="stockpicker-dropdown",
            options=stock_options_dropdown,
            value="AAPL",
        ),
        html.P(id="highest-value"),
        html.P(id="lowest-value"),
        dcc.RadioItems(id="ohlc-radio", options=ohlc_options, value="close"),
        dcc.Graph(id="stock-graph"),
        dcc.Slider(
            id="time-slider", min=0, max=6, marks=slider_marks, value=2, step=None
        ),
        # storing intermediate value on clients browser in order to share between several callbacks
        dcc.Store(id="filtered-df"),
    ]
)


@app.callback(
    Output("filtered-df", "data"),
    Input("stockpicker-dropdown", "value"),
    Input("time-slider", "value"),
)
def filter_df(stock, time_index):
    dff_daily, dff_intraday = df_dict[stock]

    dff = dff_intraday if time_index <= 2 else dff_daily

    days = {i: day for i, day in enumerate([1, 7, 30, 90, 365, 365 * 5])}

    dff = dff if time_index == 6 else filter_time(dff, days=days[time_index])

    return dff.to_json()


@app.callback(
    Output("highest-value", "children"),
    Output("lowest-value", "children"),
    Input("filtered-df", "data"),
    Input("ohlc-radio", "value"),
)
def highest_lowest_value_update(json_df, ohlc):
    dff = pd.read_json(json_df)
    highest_value = dff[ohlc].max()
    lowest_value = dff[ohlc].min()
    return highest_value, lowest_value


@app.callback(
    Output("stock-graph", "figure"),
    Input("filtered-df", "data"),
    Input("stockpicker-dropdown", "value"),
    Input("ohlc-radio", "value"),
)
def update_graph(json_df, stock, ohlc):
    dff = pd.read_json(json_df)
    return px.line(dff, x=dff.index, y=ohlc, title=symbol_dict[stock])


if __name__ == "__main__":
    app.run_server(debug=True)