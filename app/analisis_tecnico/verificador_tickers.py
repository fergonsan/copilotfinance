# === archivo: analisis_tecnico/verificador_tickers.py ===
import yfinance as yf
import pandas as pd
import time

# Lista de tickers personalizados y sus posibles reemplazos
REEMPLAZOS_SUGERIDOS = {
    "BME:BBVA": ["BBVA.MC"],
    "EUR:BTCEUR": ["BTC-USD"],
    "EUR:ETHEUR": ["ETH-USD"],
    "XETR-SXRV": ["SXRV.DE"],
    "XETR-36BZ": ["36BZ.DE"],
    "XETR-ZPRG": ["ZPRG.DE"],
    "R9B": ["R9B.F"],
    "BY6": ["BY60.F"]
}

def verificar_ticker_yahoo(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        name = info.get("shortName")
        return name is not None
    except:
        return False

def test_tickers(cartera_tickers):
    resultados = []
    for ticker in cartera_tickers:
        print(f"🔎 Verificando {ticker}...")
        sugerencias = REEMPLAZOS_SUGERIDOS.get(ticker, [])
        valido = verificar_ticker_yahoo(ticker)
        sugerido_valido = None

        if not valido:
            for s in sugerencias:
                if verificar_ticker_yahoo(s):
                    sugerido_valido = s
                    break

        resultados.append({
            "Ticker original": ticker,
            "¿Válido?": "✅" if valido else "❌",
            "Sugerencia válida": sugerido_valido or "-"
        })
        time.sleep(8)

    return pd.DataFrame(resultados)

# === EJEMPLO USO ===
if __name__ == "__main__":
    from cartera import leer_y_consolidar_cartera
    cartera = leer_y_consolidar_cartera()
    tickers = cartera['Ticker'].tolist()
    df_verificados = test_tickers(tickers)
    df_verificados.to_excel("output/verificacion_tickers.xlsx", index=False)
    print("\n✅ Verificación completada. Revisa output/verificacion_tickers.xlsx")
