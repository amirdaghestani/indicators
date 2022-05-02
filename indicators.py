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


def rsi(data, length, source, ma):
    def change(row):
        index = row.name
        if index > 0:
            value = row[source] - data[source].iloc[index - 1]
        else:
            value = np.NAN
        return value

    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['change', 'up_move', 'down_move', 'up', 'down', 'rsi'])
    dump_df['change'] = data.apply(lambda row: change(row), axis=1)
    dump_df['up_move'] = dump_df[~dump_df['change'].isnull()].apply(lambda row: max(0, row['change']), axis=1)
    dump_df['down_move'] = dump_df[~dump_df['change'].isnull()].apply(lambda row: -min(0, row['change']), axis=1)
    dump_df['up'] = method(dump_df, length, 'up_move', ma[0], ma[1])
    dump_df['down'] = method(dump_df, length, 'down_move', ma[0], ma[1])

    rsi_column = np.where(dump_df['down'] == 0, 100, 100 - 100/(1 + dump_df['up']/dump_df['down']))

    return rsi_column


def macd(data, fast_len, slow_len, smooth_len, source, osc_ma, sig_ma):
    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['osc_line', 'sig_line'])
    dump_df['osc_line'] = method(data, fast_len, source, osc_ma[0], osc_ma[1]) - \
                          method(data, slow_len, source, osc_ma[0], osc_ma[1])

    dummy = pd.DataFrame(index=range(0, slow_len-1)).squeeze()
    values = method(dump_df[slow_len-1:data.shape[0]].reset_index(), smooth_len, 'osc_line', sig_ma[0], sig_ma[1]).squeeze()
    dump_df['sig_line'] = pd.concat([dummy, values], ignore_index=True)

    return [dump_df['osc_line'], dump_df['sig_line']]


def cci(data, osc_len, ma_len, ma):
    def md(row):
        index = row.name + 1
        subset = abs(dump_df['tp'].iloc[index - osc_len:index] - row['ma'])
        return subset.mean()

    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['tp', 'ma', 'md'])
    dump_df['tp'] = (data['High'] + data['Low'] + data['Close'])/3
    dump_df['ma'] = method(dump_df, ma_len, 'tp', ma[0], ma[1])
    dump_df['md'] = dump_df.apply(lambda row: md(row), axis=1)

    cci_column = (dump_df['tp'] - dump_df['ma'])/(0.015 * dump_df['md'])
    return cci_column


def stoch(data, fast_len, slow_len, d_len):
    def calc(row):
        index = row.name + 1
        if index - fast_len >= 0:
            min_price = min(data['Low'].iloc[index - fast_len:index])
            max_price = max(data['High'].iloc[index - fast_len:index])
            if max_price == min_price:
                value = np.NAN
            else:
                value = 100 * (row['Close'] - min_price) / (max_price - min_price)
        else:
            value = np.NAN
        return value

    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['fast_k', 'slow_k', 'd'])
    dump_df['fast_k'] = data.apply(lambda row: calc(row), axis=1)
    dump_df['slow_k'] = sma(dump_df, slow_len, 'fast_k')
    dump_df['d'] = sma(dump_df, d_len, 'slow_k')

    return [dump_df['fast_k'], dump_df['slow_k'], dump_df['d']]


def stoch_rsi(data, k_len, d_len, rsi_len, stoch_len, source, rsi_method):
    def calc(row):
        index = row.name + 1
        if index - stoch_len >= 0:
            min_rsi = min(dump_df['rsi'].iloc[index - stoch_len:index])
            max_rsi = max(dump_df['rsi'].iloc[index - stoch_len:index])
            if max_rsi == min_rsi:
                value = np.NAN
            else:
                value = 100 * (row['rsi'] - min_rsi)/(max_rsi - min_rsi)
        else:
            value = np.NAN
        return value

    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['rsi', 'fast_k', 'slow_k', 'd'])
    dump_df['rsi'] = rsi(data, rsi_len, source, rsi_method)
    dump_df['fast_k'] = dump_df.apply(lambda row: calc(row), axis=1)

    dummy = pd.DataFrame(index=range(0, rsi_len+stoch_len-1))
    values = sma(dump_df[rsi_len+stoch_len-1:data.shape[0]].reset_index(), k_len, 'fast_k')
    dump_df['slow_k'] = pd.concat([dummy, values], ignore_index=True)

    dummy = pd.DataFrame(index=range(0, rsi_len+stoch_len+k_len-2))
    values = sma(dump_df[rsi_len+stoch_len+k_len-2:data.shape[0]].reset_index(), d_len, 'slow_k')
    dump_df['d'] = pd.concat([dummy, values], ignore_index=True)

    return [dump_df['fast_k'], dump_df['slow_k'], dump_df['d']]


def bbp(data, length, source, ma):
    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['ma', 'bull', 'bear'])
    dump_df['ma'] = method(data, length, source, ma[0], ma[1])
    dump_df['bull'] = data['High'] - dump_df['ma']
    dump_df['bear'] = data['Low'] - dump_df['ma']

    bbp_column = dump_df['bull'] + dump_df['bear']
    return bbp_column


def adx(data, di_len, ma_len, ffd):
    def tr(row):
        index = row.name
        ele1 = abs(row['High'] - row['Low'])
        ele2 = abs(row['High'] - data['Close'].iloc[index - 1])
        ele3 = abs(row['Low'] - data['Close'].iloc[index - 1])
        value = max(ele1, ele2, ele3)
        return value

    def dh(row):
        index = row.name
        if index > 0:
            value = row['High'] - data['High'].iloc[index - 1]
        else:
            value = 0
        return value

    def dl(row):
        index = row.name
        if index > 0:
            value = data['Low'].iloc[index - 1] - row['Low']
        else:
            value = 0
        return value

    def pdx(row):
        if row['dh'] > row['dl'] and row['dh'] > 0:
            value = row['dh']
        else:
            value = 0
        return value

    def ndx(row):
        if row['dh'] < row['dl'] and row['dl'] > 0:
            value = row['dl']
        else:
            value = 0
        return value

    dump_df = pd.DataFrame(index=range(0, data.shape[0]), columns=['tr', 'dh', 'dl', 'pdx', 'ndx', 'true_range',
                                                                   'rma-pdx', 'rma-ndx', 'pdmi', 'ndmi', 'dx'])
    dump_df['tr'] = data.apply(lambda row: tr(row), axis=1)
    dump_df['dh'] = data.apply(lambda row: dh(row), axis=1)
    dump_df['dl'] = data.apply(lambda row: dl(row), axis=1)
    dump_df['pdx'] = dump_df.apply(lambda row: pdx(row), axis=1)
    dump_df['ndx'] = dump_df.apply(lambda row: ndx(row), axis=1)
    dump_df['true_range'] = rma(dump_df, di_len, 'tr', ffd)
    dump_df['rma-pdx'] = rma(dump_df, di_len, 'pdx', ffd)
    dump_df['rma-ndx'] = rma(dump_df, di_len, 'ndx', ffd)
    dump_df['pdmi'] = 100 * dump_df['rma-pdx'].div(dump_df['true_range'])
    dump_df['ndmi'] = 100 * dump_df['rma-ndx'].div(dump_df['true_range'])
    dump_df['dx'] = abs(dump_df['pdmi'] - dump_df['ndmi'])/np.where(dump_df['pdmi'] + dump_df['ndmi'] == 0, 1,
                                                                    dump_df['pdmi'] + dump_df['ndmi'])

    if ffd:
        dummy = pd.DataFrame(index=range(0, di_len))
        adx_values = 100 * rma(dump_df[di_len:data.shape[0]].reset_index(), ma_len, 'dx', ffd)
        adx_column = pd.concat([dummy, adx_values], ignore_index=True).squeeze()
    else:
        adx_column = 100 * rma(dump_df, ma_len, 'dx', ffd)
    return adx_column
