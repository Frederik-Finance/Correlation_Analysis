import os
import pandas as pd
from binance.client import Client
import numpy as np
import config
import seaborn as sns
import pickle


client = Client(config.apiKey, config.apiSecret)


def _pickle(folder_name, filename, lst):
    abs_path = os.path.abspath(os.curdir)

    file_path = os.path.join(abs_path, folder_name, filename)

    if not os.path.exists(os.path.join(abs_path, folder_name)):
        os.makedirs(os.path.join(abs_path, folder_name))

    with open(file_path, 'wb') as fp:
        pickle.dump(lst, fp)


# get all symbols
info = client.get_exchange_info()

symbols = [x['symbol'] for x in info['symbols']]

relevant = [symbol for symbol in symbols if symbol.endswith('USDT')]

print(relevant)
_pickle('pickles', 'relevant', relevant)


def getdata(symbol, tf='1m'):
    try:
        frame = pd.DataFrame(client.get_historical_klines(
            symbol, tf, '1 hour ago'))
        if len(frame) > 0:
            frame = frame.iloc[:, :5]
            frame.columns = ['Time', 'Open', 'High', 'Low', 'Close']
            frame = frame.set_index('Time')
            # unit stays unix time
            frame.index = pd.to_datetime(frame.index)
            frame = frame.astype(float)
            return frame
    except Exception as e:
        print(e)


dfs = []

for coin in relevant:
    print(coin)
    dfs.append(getdata(coin))


mergeddf = pd.concat(dict(zip(relevant, dfs)), axis=1)

closesdf = mergeddf.loc[:, mergeddf.columns.get_level_values(1).isin([
    'Close'])]

closesdf.columns = closesdf.columns.droplevel(1)


logretdf = np.log(closesdf.pct_change()+1)

corr_df = logretdf.corr()


_pickle('pickles', 'mergeddf', mergeddf)
_pickle('pickles', 'closesdf', closesdf)
_pickle('pickles', 'logretdf', logretdf)
_pickle('pickles', 'corr_df', corr_df)
