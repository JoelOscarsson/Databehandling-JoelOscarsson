import dash
import dash_bootstrap_components as dbc
import os
from load_data import StockData
from dash import html, dcc  # This is used for Creating layout
from dash.dependencies import Output, Input # för att vi ska kunna kontrollera våra element som vi skapat
import plotly_express as px
from time_filtering import filter_time

# Vi behöver denna pathen för att lägga in i stockdata som vi har i classen
# dirname är pathen till den __file__ parents mapp som är i stock_dashboard
# path = os.path.dirname(__file__), "stocksdata"

# Vi kan joina den här filen med "stocksdata"
# När vi printar denna så ser vi att vi har pathen till stocksdata
directory_path = os.path.dirname(__file__)
path = os.path.join(directory_path, "stocksdata")

print(path)

stockdata_object = StockData(path)

# Vi tog en aktie för att testa att det fungerade
# print(stockdata_object.stock_dataframe("AAPL"))

symbol_dict = {"AAPL": "Apple", "NVDA": "Nvidia", "TSLA": "Tesla", "IBM": "IBM"}

df_dict = {symbol: stockdata_object.stock_dataframe(symbol) for symbol in symbol_dict}

# När vi printade denna så har vi den i dictionary
# Förklarar vi har en dictionary av keys i en dataframe
print(df_dict.keys())

# Vi ser att vi får en lista av dictionaries
# print(df_dict["TSLA"][0])

stock_options_dropdown = [
                {"label": name, "value": symbol} for symbol, name in symbol_dict.items()
            ]

# label är det som syns och value är själva värdet när man klickar på den
ohlc_options = [{"label": option, "value": option} for option in ("open", "high", "low", "close")]

# Vi kör en comprehension för att kunna skapa de olika marksen i slidern
slider_marks = {i: mark for i, mark in enumerate(["1 day", "1 week", "1 month", "3 months", "1 year", "5 year", "Max"])}

# Create dashboard, dash is built on something called flasked(python uses it to create a webserver)
# Create a Dash App
app = dash.Dash(__name__)

# Creating layout
app.layout = html.Main(
    [
        html.H1("Techy stocks viewer"),
        html.P("Choose a stock"),
        # id - vi ger den(dropdown) ett unikt id som vi kan referera till
        dcc.Dropdown(
            id="stockpicker-dropdown",
            options= stock_options_dropdown,
            value="AAPL",
        ),
        # ohlc = open high low close # Det är denna som gör att det går att klicka på label och value
        dcc.RadioItems(id = "ohlc-radio", options = ohlc_options, value = "close"),
        dcc.Graph(id = "stock-graph"),
        # Vi vill kunna se tidslinje
        dcc.Slider(id = "time-slider", min = 0, max = 6, marks = slider_marks, value = 2, step = None)
    ]
)


# decoratorn gör att vi får en uppdaterad funktionalitet uppdaterad value och kan skicka tillbaka till figuren
# Vi ska få in graferna i sidan, vi importerade ett verktyg längst upp på
# input från olika ställen, dropdown, radioitems, sliders
@app.callback(
    Output("stock-graph", "figure"),
    Input("stockpicker-dropdown", "value"),
    Input("ohlc-radio", "value"),
    Input("time-slider", "value")
)
def update_graph(stock, ohlc, time_index): # första parametern -> första input, andra parameter -> andra input
    # tuple unpacks a list
    # dff för df filter(filtera, en df) 
    dff_daily, dff_intraday = df_dict[stock]


    # Vi kör intraday men om den är större så ser vi daglig data
    dff = dff_intraday if time_index <= 2 else dff_daily

    # För att filtrera så måste vi räkna från dagar, vi kan inte gå rakt på och gå från månad -> år osv
    days = {i: day for i, day in enumerate([1, 7, 30, 90, 365, 365*5])}

    dff = dff if time_index == 6 else filter_time(dff, days = days[time_index])

    return px.line(dff, x = dff.index, y = ohlc, title = symbol_dict[stock])





# När vi kör dashen så vill vi att appen ska köra något speciellt
# "Vi får Serving Flask app", __name__ är ju "main"
if __name__ == "__main__":
    app.run_server(debug=True)