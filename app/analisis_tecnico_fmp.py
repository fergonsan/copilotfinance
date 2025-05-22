
import requests
import pandas as pd
import time

# === CONFIGURACIÓN ===
API_KEY = "fqplClJV8qfu2MsYhfkdQL4AZGbeBH9k"
BASE_URL = "https://financialmodelingprep.com/api/v3"

# === Mapeo de tickers personalizados a compatibles con FMP ===
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

# === Consulta de indicadores técnicos ===
def obtener_indicadores_fmp(ticker_original):
    ticker = convertir_ticker_fmp(ticker_original)
    print(f"📡 Consultando indicadores de {ticker_original} ({ticker})...")

    try:
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
            if not isinstance(data, dict) or "technicalAnalysis" not in data:
                return []
            return data["technicalAnalysis"]

        # RSI
        rsi_data = fetch("/technical_indicator/rsi")
        rsi = float(rsi_data[0]["rsi"]) if rsi_data else None

        # MACD
        macd_data = fetch("/technical_indicator/macd")
        macd = float(macd_data[0]["macd"]) if macd_data else None
        macd_signal = float(macd_data[0]["macdSignal"]) if macd_data else None

        # SMA 20
        sma_data = fetch("/technical_indicator/sma", {"time_period": 20})
        sma20 = float(sma_data[0]["sma"]) if sma_data else None

        return pd.DataFrame([{
            "Ticker": ticker_original,
            "RSI": rsi,
            "MACD": macd,
            "MACD_Signal": macd_signal,
            "SMA20": sma20
        }])

    except Exception as e:
        print(f"❌ Error al obtener datos de {ticker_original}: {e}")
        return pd.DataFrame()

# === PRUEBA CON CARTERA ===
if __name__ == "__main__":
    from cartera import leer_y_consolidar_cartera

    cartera = leer_y_consolidar_cartera()
    resultados = []

    for _, fila in cartera.iterrows():
        ticker = fila['Ticker']
        indicadores = obtener_indicadores_fmp(ticker)
        if not indicadores.empty:
            resultados.append(indicadores)
        time.sleep(2)  # Espera entre peticiones para evitar rate limit

    if resultados:
        df_resultado = pd.concat(resultados, ignore_index=True)
        print("\n📊 Indicadores técnicos obtenidos:")
        print(df_resultado)
    else:
        print("⚠️ No se pudieron obtener indicadores para ningún ticker.")
