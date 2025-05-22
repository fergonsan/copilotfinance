import yfinance as yf
import pandas as pd
import ta

def obtener_indicadores_yf(ticker):
    try:
        data = yf.download(ticker, period="90d", interval="1d")
        if data.empty:
            return None

        data['SMA20'] = ta.trend.sma_indicator(data['Close'], window=20)
        data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()
        macd = ta.trend.MACD(data['Close'])
        data['MACD'] = macd.macd()
        data['MACD_Signal'] = macd.macd_signal()

        row = data.tail(1)
        return pd.DataFrame([{
            "Ticker": ticker,
            "Fuente": "YF",
            "RSI": row['RSI'].values[0],
            "MACD": row['MACD'].values[0],
            "MACD_Signal": row['MACD_Signal'].values[0],
            "SMA20": row['SMA20'].values[0]
        }])
    except:
        return None