import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import re

# === Función de limpieza robusta ===
def limpiar_valor(valor_str):
    """
    Limpia strings como '1,026.80€', '2.172,73€' o '4,26' y los convierte a float correctamente.
    """
    if isinstance(valor_str, (int, float)):
        return float(valor_str)

    valor_str = str(valor_str).replace("€", "").strip()

    # Formato americano: 1,026.80
    if re.match(r"^\d{1,3}(,\d{3})*\.\d+$", valor_str):
        valor_str = valor_str.replace(",", "")
        return float(valor_str)

    # Formato europeo: 1.026,80
    if re.match(r"^\d{1,3}(\.\d{3})*,\d+$", valor_str):
        valor_str = valor_str.replace(".", "").replace(",", ".")
        return float(valor_str)

    # Por si acaso: 4,26 → 4.26
    valor_str = valor_str.replace(",", ".")
    try:
        return float(valor_str)
    except:
        return None

# === Función principal del módulo ===
def leer_y_consolidar_cartera():
    # Rutas
    ruta_credenciales = Path(__file__).resolve().parents[2] / "data" / "credentials.json"
    credenciales = str(ruta_credenciales)

    # === CONFIGURA ESTO ===
    sheet_id = "1hvDI9dWDerNY1AFGPe3Rg365cuLO78iBcYR-LzdU6ok"
    hoja = "Cartera"

    # Conexión con Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credenciales, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet(hoja)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Normalización de nombres de columnas
    df.rename(columns=lambda col: col.strip(), inplace=True)
    df['Ticker'] = df['Ticker'].astype(str).str.upper()

    # Limpieza de valores numéricos
    df['Precio Compra'] = df['Precio Compra'].apply(limpiar_valor)
    df['Cantidad'] = df['Cantidad'].apply(limpiar_valor)

    # Eliminar datos inválidos
    df = df.dropna(subset=['Cantidad', 'Precio Compra'])
    df = df[df['Cantidad'] > 0]

    # Calcular valor total por entrada
    df['Valor Total'] = df['Cantidad'] * df['Precio Compra']

    # Consolidar por Ticker
    df_consolidado = df.groupby('Ticker').agg({
        'Tipo': 'first',
        'Sector': 'first',
        'Cantidad': 'sum',
        'Valor Total': 'sum'
    }).reset_index()

    # Calcular precio medio ponderado
    df_consolidado['Precio Medio Compra'] = df_consolidado['Valor Total'] / df_consolidado['Cantidad']
    df_consolidado.drop(columns='Valor Total', inplace=True)

    return df_consolidado

# === Ejemplo de ejecución ===
if __name__ == "__main__":
    cartera = leer_y_consolidar_cartera()
    print(cartera)
