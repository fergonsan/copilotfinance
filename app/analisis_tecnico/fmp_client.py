import requests
import pandas as pd

API_KEY = "fqplClJV8qfu2MsYhfkdQL4AZGbeBH9k"
BASE_URL = "https://financialmodelingprep.com/api/v3"

def convertir_ticker_fmp(ticker_original):
    reemplazos = {
        "BME:BBVA": "BBVA.MC",
        "EUR:BTCEUR": "BTCUSD",
        "EUR:ETHEUR": "ETHUSD",
        "XETR-SXRV": "SXRV.DE",
        "XETR-36BZ": "36BZ.DE",
        "XETR-ZPRG": "ZPRG.DE",
    }
    return reemplazos.get(ticker_original, ticker_original)

def obtener_indicadores_fmp(ticker_original):
    ticker = convertir_ticker_fmp(ticker_original)

    def fetch(endpoint, extra_params={}):
        params = {
            "symbol": ticker,
            "interval": "daily",
            "time_period": 14,
            "series_type": "close",
            "apikey": API_KEY,
            **extra_params
        }
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("technicalAnalysis", [])

    try:
        rsi = fetch("/technical_indicator/rsi")
        macd = fetch("/technical_indicator/macd")
        sma = fetch("/technical_indicator/sma", {"time_period": 20})

        if not rsi or not macd or not sma:
            return None

        return pd.DataFrame([{
            "Ticker": ticker_original,
            "Fuente": "FMP",
            "RSI": float(rsi[0]["rsi"]),
            "MACD": float(macd[0]["macd"]),
            "MACD_Signal": float(macd[0]["macdSignal"]),
            "SMA20": float(sma[0]["sma"])
        }])
    except:
        return None