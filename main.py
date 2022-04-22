import pandas as pd
from smoothing import sma, ema
from indicators import rsi, macd, cci, stoch, stoch_rsi, adx, bbp


indices = ['ghapino', 'foulad', 'akhaber', 'faluleh', 'varna', 'sepid']
for index in indices:
    data = pd.read_csv(index + '.csv')
    computed = data
    computed['SMA20'] = sma(data, 20, 'Close')
    computed['SMA50'] = sma(data, 50, 'Close')
    computed['SMA100'] = sma(data, 100, 'Close')
    computed['SMA200'] = sma(data, 200, 'Close')
    computed['EMA20,ffd=True'] = ema(data, 20, 'Close', True)
    computed['EMA20,ffd=False'] = ema(data, 20, 'Close', False)
    computed['EMA50,ffd=True'] = ema(data, 50, 'Close', True)
    computed['EMA50,ffd=False'] = ema(data, 50, 'Close', False)
    computed['EMA100,ffd=True'] = ema(data, 100, 'Close', True)
    computed['EMA100,ffd=False'] = ema(data, 100, 'Close', False)
    computed['EMA200,ffd=True'] = ema(data, 200, 'Close', True)
    computed['EMA200,ffd=False'] = ema(data, 200, 'Close', False)
    computed['ADX14,ffd=True'] = adx(data, 14, 14, True)
    computed['ADX14,ffd=False'] = adx(data, 14, 14, False)
    computed['BBP13,method=EMA,ffd=True'] = bbp(data, 13, 'Close', ['ema', True])
    computed['BBP13,method=EMA,ffd=False'] = bbp(data, 13, 'Close', ['ema', False])
    computed['RSI14,method=SMA,ffd=True'] = rsi(data, 14, 'Close', ['sma', True])
    computed['RSI14,method=SMA,ffd=False'] = rsi(data, 14, 'Close', ['sma', False])
    stoch533 = stoch(data, 5, 3, 3)
    stoch1433 = stoch(data, 14, 3, 3)
    stoch2155 = stoch(data, 21, 5, 5)
    computed['Stoch5-3-3_line'] = stoch533[1]
    computed['Stoch5-3-3_signal'] = stoch533[2]
    computed['Stoch14-3-3_line'] = stoch1433[1]
    computed['Stoch14-3-3_signal'] = stoch1433[2]
    computed['Stoch21-5-5_line'] = stoch2155[1]
    computed['Stoch21-5-5_signal'] = stoch2155[2]
    stochrsi13855True = stoch_rsi(data, 5, 5, 8, 13, 'Close', ['sma', True])
    stochrsi13855False = stoch_rsi(data, 5, 5, 8, 13, 'Close', ['sma', False])
    stochrsi211388True = stoch_rsi(data, 8, 8, 13, 21, 'Close', ['sma', True])
    stochrsi211388False = stoch_rsi(data, 8, 8, 13, 21, 'Close', ['sma', False])
    computed['StochRSI13-8-5-5_line,rsi-method=[sma,True]'] = stochrsi13855True[1]
    computed['StochRSI13-8-5-5_signal,rsi-method=[sma,True]'] = stochrsi13855True[2]
    computed['StochRSI13-8-5-5_line,rsi-method=[sma,False]'] = stochrsi13855False[1]
    computed['StochRSI13-8-5-5_signal,rsi-method=[sma,False]'] = stochrsi13855False[2]
    computed['StochRSI21-13-8-8_line,rsi-method=[sma,True]'] = stochrsi211388True[1]
    computed['StochRSI21-13-8-8_signal,rsi-method=[sma,True]'] = stochrsi211388True[2]
    computed['StochRSI21-13-8-8_line,rsi-method=[sma,False]'] = stochrsi211388False[1]
    computed['StochRSI21-13-8-8_signal,rsi-method=[sma,False]'] = stochrsi211388False[2]
    computed['CCI14,method=SMA'] = cci(data, 14, 14, ['sma', False])
    computed['CCI20,method=SMA'] = cci(data, 20, 20, ['sma', False])
    computed['CCI30,method=SMA'] = cci(data, 30, 30, ['sma', False])
    macd6131True = macd(data, 6, 13, 1, 'Close', ['ema', True], ['ema', True])
    macd6131False = macd(data, 6, 13, 1, 'Close', ['ema', False], ['ema', False])
    macd12269True = macd(data, 12, 26, 9, 'Close', ['ema', True], ['ema', True])
    macd12269False = macd(data, 12, 26, 9, 'Close', ['ema', False], ['ema', False])
    macd245218True = macd(data, 24, 52, 18, 'Close', ['ema', True], ['ema', True])
    macd245218False = macd(data, 24, 52, 18, 'Close', ['ema', False], ['ema', False])
    computed['MACD6-13-1_line,method=[EMA,True]'] = macd6131True[0]
    computed['MACD6-13-1_signal,method=[EMA,True]'] = macd6131True[1]
    computed['MACD6-13-1_line,method=[EMA,False]'] = macd6131False[0]
    computed['MACD6-13-1_signal,method=[EMA,False]'] = macd6131False[1]
    computed['MACD12-26-9_line,method=[EMA,True]'] = macd12269True[0]
    computed['MACD12-26-9_signal,method=[EMA,True]'] = macd12269True[1]
    computed['MACD12-26-9_line,method=[EMA,False]'] = macd12269False[0]
    computed['MACD12-26-9_signal,method=[EMA,False]'] = macd12269False[1]
    computed['MACD24-52-18_line,method=[EMA,True]'] = macd245218True[0]
    computed['MACD24-52-18_signal,method=[EMA,True]'] = macd245218True[1]
    computed['MACD24-52-18_line,method=[EMA,False]'] = macd245218False[0]
    computed['MACD24-52-18_signal,method=[EMA,False]'] = macd245218False[1]

    computed.to_csv(index + '_comp.csv', index=False)
