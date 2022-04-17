import pandas as pd


def rma(data, length, source, ffd):
    pass


def sma(data, length, source):
    def calc(row):
        index = row.name + 1
        subset = data[source].iloc[index - length:index]
        return subset.mean()

    sma_column = data.apply(lambda row: calc(row), axis=1)
    return sma_column


def ema(data, length, source, ffd):
    multiplier = 2/(1+length)

    if ffd:
        ema_column = pd.DataFrame(index=range(0, data.shape[0]), columns=[''])
        ema_column.iloc[length-1] = data[source].iloc[length-1] * multiplier + \
                                    sma(data, length, source).iloc[length-1] * (1-multiplier)
        for i in range(length, data.shape[0]):
            ema_column.iloc[i] = data[source].iloc[i] * multiplier + ema_column.iloc[i-1] * (1-multiplier)

    else:
        def calc(row):
            index = row.name + 1
            if index-length >= 0:
                ema_dump = data[source].iloc[index-length] * multiplier + \
                           sma(data, length, source).iloc[index-length] * (1-multiplier)
                for i in range(index - length + 1, index):
                    ema_dump = data[source].iloc[i] * multiplier + ema_dump * (1 - multiplier)
                return ema_dump
            else:
                pass

        ema_column = data.apply(lambda row: calc(row), axis=1)

    return ema_column
