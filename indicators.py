import numpy as np
import pandas as pd
from smoothing import sma, ema, rma


def method(data, length, source, smooth, ffd):
    action = {
        True: {
            'sma': sma(data, length, source),
            'ema': ema(data, length, source, True),
            'rma': rma(data, length, source, True)
        },
        False: {
            'sma': sma(data, length, source),
            'ema': ema(data, length, source, False),
            'rma': ema(data, length, source, False),
        }
    }

    return action[ffd][smooth]

'''
ma[smooth, ffd]
'''
def rsi(data, length, source, ma):
    def change(row):
        index = row.name
        value = row[source] - data[source].iloc[index - 1]
        return value

    dump_df = pd.DataFrame(0, index=range(0, data.shape[0]), columns=['up_move', 'down_move'])
    dump_df['up_move'] = data.apply(lambda row: max(0, change(row)), axis=1)
    dump_df['down_move'] = data.apply(lambda row: min(0, change(row)), axis=1)

    rsi_column = 100 - 100/(1 + abs(method(dump_df, length, 'up_move', ma[0], ma[1])/method(dump_df, length, 'down_move'
                                                                                            , ma[0], ma[1])))

    return rsi_column


def macd(data, fast_len, slow_len, smooth_len, osc_ma, sig_ma, source):
    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['osc_line', 'sig_line'])
    dump_df['osc_line'] = method(data, fast_len, source, osc_ma[0], osc_ma[1]) - \
                          method(data, slow_len, source, osc_ma[0], osc_ma[1])

    dump_df['sig_line'] = method(dump_df, smooth_len, 'osc_line', sig_ma[0], sig_ma[1])

    return [dump_df['osc_line'], dump_df['sig_line']]

'''
ma = [method, ffd]
'''


def cci(data, length, ma):
    def md(row):
        index = row.name + 1
        subset = abs(dump_df['tp'].iloc[index - length:index] - row['mean_val'])
        return subset.mean()

    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['tp', 'mean_val', 'tp_ma', 'md'])
    dump_df['tp'] = (data['High'] + data['Low'] + data['Close'])/3
    dump_df['mean_val'] = sma(dump_df, length, 'tp')
    dump_df['tp_ma'] = method(dump_df, length, 'tp', ma[0], ma[1])
    dump_df['md'] = dump_df.apply(lambda row: md(row), axis=1)

    cci_column = (dump_df['tp'] - dump_df['tp_ma'])/(0.15 * dump_df['md'])
    return cci_column


def stoch(data, fast_k, slow_k, d):
    def fast_k_calc(row):
        index = row.name + 1
        if index - fast_k >= 0:
            min_price = min(data['Low'].iloc[index - fast_k:index])
            max_price = max(data['High'].iloc[index - fast_k:index])
            max_price = max(data['High'].iloc[index - fast_k:index])
            value = 100 * (row['Close'] - min_price)/(max_price - min_price)
        else:
            value = np.NAN
        return value

    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['fast_k', 'slow_k', 'd'])
    dump_df['fast_k'] = data.apply(lambda row: fast_k_calc(row), axis=1)
    dump_df['slow_k'] = sma(dump_df, slow_k, 'fast_k')
    dump_df['d'] = sma(dump_df, d, 'slow_k')

    return [dump_df['fast_k'], dump_df['slow_k'], dump_df['d']]


def stoch_rsi(data, fast_k, slow_k, d, rsi_method):
    def fast_k_calc(row):
        index = row.name + 1
        if index - fast_k >= 0:
            min_rsi = min(dump_df['rsi'].iloc[index - fast_k:index])
            max_rsi = max(dump_df['rsi'].iloc[index - fast_k:index])
            value = 100 * (row['rsi'] - min_rsi)/(max_rsi - min_rsi)
        else:
            value = np.NAN
        return value

    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['rsi', 'fast_k', 'slow_k', 'd'])
    dump_df['rsi'] = rsi(data, fast_k, 'Close', rsi_method)
    dump_df['fast_k'] = dump_df.apply(lambda row: fast_k_calc(row), axis=1)
    dump_df['slow_k'] = sma(dump_df, slow_k, 'fast_k')
    dump_df['d'] = sma(dump_df, d, 'slow_k')

    return [dump_df['fast_k'], dump_df['slow_k'], dump_df['d']]


def bbp(data, length, source, ma):
    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['ma', 'bull', 'bear'])
    dump_df['ma'] = method(data, length, source, ma[0], ma[1])
    dump_df['bull'] = data['High'] - dump_df['ma']
    dump_df['bear'] = data['Low'] - dump_df['ma']

    bbp_column = dump_df['bull']/dump_df['bear']
    return bbp_column

