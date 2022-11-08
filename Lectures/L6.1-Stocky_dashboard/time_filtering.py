from datetime import datetime
from dateutil.relativedelta import relativedelta # Använder vi för att beräkna dagar

def filter_time(df, days = 0):
    last_day = df.index[0].date()
    # Nedanför räknar vi ut hur långt bakåt vi kollar, senaste dagen- 7 dagar = ett visst antal dagar
    start_day = last_day-relativedelta(days = days)
    # Vi måste sortera för det inte är monotont växande
    df = df.sort_index().loc[start_day:last_day]
    return df