import pandas as pd


class Trend():

    def BB_calculation(self, prices_df, cd, n=20, sigma=2):           
        bb = pd.DataFrame()
        bb[cd] = prices_df[cd]
        bb['center'] = prices_df[cd].rolling(n).mean()
        bb['ub'] = bb['center'] + sigma * prices_df[cd].rolling(n).std()
        bb['lb'] = bb['center'] - sigma * prices_df[cd].rolling(n).std()

        bb['pct_b'] = (bb[cd] - bb['lb']) / (bb['ub'] - bb['lb'])

        bb['band_size'] = ( bb['ub'] - bb['lb'] ) / bb['center'] * 10000
        bb.loc[bb['band_size'] == 0, 'band_size'] = 0.0001
        bb['band_size_prev'] = bb['band_size'].shift(1).copy()

        bb['volume'] = prices_df['volume']
        bb['volume_prev'] = bb['volume'].shift(1).copy()

        bb['size_chg'] = round(( bb['band_size'] - bb['band_size_prev'] ) / bb['band_size_prev'] * 100, 2)
        bb['volume_chg'] = round((bb['volume'] - bb['volume_prev']) / bb['volume_prev'] * 100, 2)
        bb.fillna(method='ffill', inplace=True)

        return (bb)
    
    
    def MA(self, df, cd, long=20, short=5):
        ma = pd.DataFrame()
        ma[cd] = df[cd].copy()
        ma['MA short'] = df[cd].rolling(long).mean()
        ma['MA long'] = df[cd].rolling(short).mean()
        return (ma)
    
    
    def RSI(self, df, cd, period=5):
        rsi_df = pd.DataFrame()
        rsi_df[cd] = df[cd].copy()
        rsi_df = rsi_df.dropna()
        rsi_df['diff'] = rsi_df[cd] - rsi_df[cd].shift(1)
        for p in rsi_df.iloc[period:].index:
            d, ad, u, au = 0, 0., 0, 0.
            for i in range(period):
                diff = rsi_df.shift(i).loc[p, 'diff']
                if diff >= 0:
                    u += 1
                    au += diff
                elif diff < 0:
                    d += 1
                    ad -= diff
            if not au + ad == 0:
                rsi = round (au / (au + ad), 4) * 100
            else:
                rsi = 0
            rsi_df.loc[p, 'RSI'] = rsi
        return (rsi_df)
    
    
    def WRSI(self, df, cd, period=20):
        rsi_df = pd.DataFrame()
        rsi_df[cd] = df[cd].copy()
        rsi_df = rsi_df.dropna()
        rsi_df['diff'] = rsi_df[cd] - rsi_df[cd].shift(1)
        for p in rsi_df.iloc[period:].index:
            d, ad, u, au, multiple = 0, 0., 0, 0., 0.
            for i in range(period):
                multiple = (period - i) / period
                diff = rsi_df.shift(i).loc[p, 'diff']
                if diff >= 0:
                    u += 1
                    au += diff * multiple
                elif diff < 0:
                    d += 1
                    ad -= diff * multiple
            if not au + ad == 0:
                rsi = round (au / (au + ad), 4) * 100
            else:
                rsi = 0
            rsi_df.loc[p, 'WRSI'] = rsi
        rsi_df['WRSI_diff'] = rsi_df['WRSI'] - rsi_df['WRSI'].shift(1)
        return (rsi_df)

    
    def MACD(self, df, cd, long=26, short=12, signal=9):
        macd = pd.DataFrame()
        macd[cd] = df[cd].copy()
        macd['MA long'] = df[cd].rolling(long).mean()
        macd['MA short'] = df[cd].rolling(short).mean()
        macd['MA signal'] = df[cd].rolling(signal).mean()
        macd['MACD'] = macd['MA short'] - macd['MA long']
        macd['oscillator'] = macd['MACD'] - macd['MA signal']
        # macd['oscillator'] > 0, 상승추세
        # macd['oscillator'] < 0, 하락추세
        return (macd)
    
    
    def stochastic_osc(self, df, cd, period_n=5, period_m=3, period_t=3):
        sto = pd.DataFrame()
        sto[cd] = df[cd].copy()
        sto['fast_k'] = 0.
        #sto['max'] = 0.
        for d in range(period_n - 1, len(sto[cd])):
            max_val = sto[cd].iloc[d-period_n+1:d+1].max()
            min_val = sto[cd].iloc[d-period_n+1:d+1].min()
            now_val = sto[cd].iloc[d]
            if not max_val - min_val == 0:
                sto['fast_k'].iloc[d] = round((now_val - min_val) / (max_val - min_val) * 100, 0)
            else:
                sto['fast_k'].iloc[d] = 0
            #sto['max'].iloc[d] = max_val
        sto['fast_d'] = round(sto['fast_k'].rolling(period_m).mean(), 0)
        sto['slow_k'] = round(sto['fast_k'].rolling(period_t).mean(), 0)
        sto['slow_d'] = round(sto['fast_d'].rolling(period_t).mean(), 0)
        # sto['slow_k'] > sto['slow_d'], 매수
        return (sto)