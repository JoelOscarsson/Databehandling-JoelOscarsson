import pandas as pd
import os  # Os is a way to provide functions for interaction with operating system


class StockData:
    def __init__(self, data_folder_path: str) -> None:
        self._data_folder_path = data_folder_path
        # Skulle passa väldigt bra att ha som property pga felmeddelanden

    # Vi ska konkatenera stocknames och endings
    def stock_dataframe(self, stockname: str) -> list:
        stock_df_list = []

        for path_ending in [
            "_TIME_SERIES_DAILY_ADJUSTED.csv",
            "_TIME_SERIES_INTRADAY_EXTENDED.csv",
        ]:
            # Vi använder os path för man ska kunna plocka ut om man sitter på mac/windows/linux
            # Vi Konkatenerar, vi joinar med datafolderpathen

            # example:
            # data_folder_path: C:\Users\j_osc\OneDrive\Documents\Github\Databehandling-JoelOscarsson/Code-alongs/stocksdata
            # stockname: AAPL
            # path_ending: _TIME_SERIES_DAILY_ADJUSTED.csv

            # resulting path: C:\Users\j_osc\OneDrive\Documents\Github\Databehandling-JoelOscarsson/Code-alongs/stocksdata/AAPL_TIME_SERIES_DAILY_ADJUSTED.csv
            path = os.path.join(self._data_folder_path, stockname + path_ending)

            # index_col(annars kommer den skapa egna index)
            # parse_dates=True (Får vi datetimeobjekt direkt)

            # Ett tips när vi gör detta är att köra i jupyter först för att se så det fungerar
            stock = pd.read_csv(path, index_col = 0, parse_dates=True)
            stock.index.rename("Date", inplace = True)

            stock_df_list.append(stock)

        return stock_df_list



