import pandas as pd
from smoothing import sma, ema
from indicators import rsi, macd, cci, stoch, stoch_rsi

data = pd.read_csv('khesapa.csv')
n = 20

data['RSI'] = stoch_rsi(data, 12, 12, 12, ['sma', False])[0]

pd.set_option("display.max_rows", None, "display.max_columns", None)
print(data)
