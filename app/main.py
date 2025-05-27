import pandas as pd
import os
import time
from pathlib import Path
from cartera import leer_y_consolidar_cartera
from analisis_tecnico.indicadores import obtener_indicadores_con_fallback

# === Crear carpeta de salida ===
Path("../output").mkdir(exist_ok=True)

# === Leer cartera consolidada ===
cartera = leer_y_consolidar_cartera()
print(f"\n📄 Cartera consolidada ({len(cartera)} activos):")
print(cartera[['Ticker', 'Cantidad', 'Precio Medio Compra']])

# === Obtener indicadores con fallback
resultados = []

for _, fila in cartera.iterrows():
    ticker = fila["Ticker"]
    print(f"\n🔎 Procesando {ticker}...")
    df_ind = obtener_indicadores_con_fallback(ticker)
    if not df_ind.empty:
        resultados.append(df_ind)
    time.sleep(20)  # evitar bloqueo de Yahoo o FMP

# === Unir con datos de cartera
if resultados:
    df_indicadores = pd.concat(resultados, ignore_index=True)
    df_final = pd.merge(cartera, df_indicadores, on="Ticker", how="left")
    ruta = Path("../output") / "indicadores_cartera.xlsx"
    df_final.to_excel(ruta, index=False)
    print(f"\n✅ Indicadores exportados a: {ruta}")
else:
    print("⚠️ No se pudieron obtener indicadores para ningún activo.")
