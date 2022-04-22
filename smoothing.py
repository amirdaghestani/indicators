import pandas as pd


def rma(data, length, source, ffd):
    multiplier = 1/length

    if ffd:
        rma_column = pd.DataFrame(index=range(0, data.shape[0]), columns=[''])
        rma_column.iloc[length] = data[source].iloc[length] * multiplier + \
                                    sma(data, length, source).iloc[length-1] * (1-multiplier)
        for i in range(length + 1, data.shape[0]):
            rma_column.iloc[i] = data[source].iloc[i] * multiplier + rma_column.iloc[i-1] * (1-multiplier)

    else:
        def calc(row):
            index = row.name + 1
            if index - 2*length >= 0:
                rma_dump = data[source].iloc[index-length] * multiplier + \
                           sma(data, length, source).iloc[index-length-1] * (1-multiplier)
                for i in range(index - length + 1, index):
                    rma_dump = data[source].iloc[i] * multiplier + rma_dump * (1 - multiplier)
                return rma_dump
            else:
                pass

        rma_column = data.apply(lambda row: calc(row), axis=1)

    return rma_column


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
        ema_column.iloc[length] = data[source].iloc[length] * multiplier + \
                                    sma(data, length, source).iloc[length-1] * (1-multiplier)
        for i in range(length + 1, data.shape[0]):
            ema_column.iloc[i] = data[source].iloc[i] * multiplier + ema_column.iloc[i-1] * (1-multiplier)

    else:
        def calc(row):
            index = row.name + 1
            if index - 2*length >= 0:
                ema_dump = data[source].iloc[index-length] * multiplier + \
                           sma(data, length, source).iloc[index-length-1] * (1-multiplier)
                for i in range(index - length + 1, index):
                    ema_dump = data[source].iloc[i] * multiplier + ema_dump * (1 - multiplier)
                return ema_dump
            else:
                pass

        ema_column = data.apply(lambda row: calc(row), axis=1)

    return ema_column
