import dash
import dash_bootstrap_components as dbc
import os
from load_data import StockData

# Vi behöver denna pathen för att lägga in i stockdata som vi har i classen
# dirname är pathen till den __file__ parents mapp som är i stock_dashboard
#path = os.path.dirname(__file__), "stocksdata"

# Vi kan joina den här filen med "stocksdata"
# När vi printar denna så ser vi att vi har pathen till stocksdata
directory_path = os.path.dirname(__file__)
path = os.path.join(directory_path, "stocksdata")

print(path)


stockdata_object = StockData(path)
print(stockdata_object.stock_dataframe("AAPL"))