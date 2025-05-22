import pandas as pd
import os
from datetime import date
from analisis_tecnico.fmp_client import obtener_indicadores_fmp
from analisis_tecnico.yf_client import obtener_indicadores_yf

def obtener_indicadores_con_fallback(ticker):
    nombre_archivo = f"cache_indicadores/{ticker}_{date.today()}.csv"
    os.makedirs("cache_indicadores", exist_ok=True)

    if os.path.exists(nombre_archivo):
        return pd.read_csv(nombre_archivo)

    df = obtener_indicadores_fmp(ticker)
    if df is None:
        df = obtener_indicadores_yf(ticker)

    if df is not None:
        df.to_csv(nombre_archivo, index=False)
        return df

    return pd.DataFrame([{
        "Ticker": ticker,
        "Fuente": None,
        "RSI": None,
        "MACD": None,
        "MACD_Signal": None,
        "SMA20": None
    }])
