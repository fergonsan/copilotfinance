import yfinance as yf
import pandas as pd
import ta

def obtener_datos_y_calcular_indicadores(ticker, dias=90):
    """
    Descarga los datos de cotización de los últimos `dias` y calcula indicadores técnicos.
    """
    try:
        # Mapeo para convertir tickers raros si hace falta
        ticker_mapeado = convertir_ticker_yfinance(ticker)
        data = yf.download(ticker_mapeado, period=f"{dias}d", interval="1d")

        if data.empty:
            print(f"[!] No se pudo obtener datos para {ticker}")
            return None

        # Calcular indicadores
        data['SMA20'] = ta.trend.sma_indicator(data['Close'], window=20)
        data['SMA50'] = ta.trend.sma_indicator(data['Close'], window=50)
        data['SMA200'] = ta.trend.sma_indicator(data['Close'], window=200)

        data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()

        macd = ta.trend.MACD(data['Close'])
        data['MACD'] = macd.macd()
        data['MACD_Signal'] = macd.macd_signal()

        return data

    except Exception as e:
        print(f"Error con {ticker}: {e}")
        return None

def convertir_ticker_yfinance(ticker_original):
    """
    Convierte tickers personalizados de tu hoja a los formatos esperados por yfinance.
    """
    # Mapeo específico si lo necesitas
    reemplazos = {
        "XETR-SXRV": "SXRV.DE",
        "XETR-36BZ": "36BZ.DE",
        "XETR-ZPRG": "ZPRG.DE",
        "BME:BBVA": "BBVA.MC",
        "EUR:BTCEUR": "BTC-USD",
        "EUR:ETHEUR": "ETH-USD",
    }
    return reemplazos.get(ticker_original, ticker_original)

# === TEST UNITARIO CON LA CARTERA ===
if __name__ == "__main__":
    from cartera import leer_y_consolidar_cartera

    cartera = leer_y_consolidar_cartera()

    for _, fila in cartera.iterrows():
        ticker = fila['Ticker']
        print(f"\n📊 Indicadores para {ticker}")
        datos = obtener_datos_y_calcular_indicadores(ticker)

        if datos is not None:
            ultimos = datos.tail(1)[['Close', 'SMA20', 'SMA50', 'RSI', 'MACD', 'MACD_Signal']]
            print(ultimos.to_string(index=False))
