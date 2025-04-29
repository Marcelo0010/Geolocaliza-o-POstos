#Chamandado as Bibliotecas
import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point
import numpy as np
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import base64

# === CONVERSÃO DE COORDENADAS PARA DECIMAL===
def dms_to_decimal(dms):
    try:
        if pd.isna(dms):
            return np.nan
        dms = dms.replace(",", ".")
        parts = dms.split(":")
        if len(parts) == 3:
            degrees = float(parts[0])
            minutes = float(parts[1]) / 60
            seconds = float(parts[2]) / 3600
            decimal = abs(degrees) + minutes + seconds
            return -decimal if degrees < 0 else decimal
        return np.nan
    except:
        return np.nan

# === LEITURA E LIMPEZA DE DADOS ===
file_path = r"ADICIONE AQUI O CAMINHO DO ARQUIVO"
df = pd.read_excel(file_path, sheet_name="Folha1")
df["LATITUDE"] = df["LATITUDE"].apply(dms_to_decimal)
df["LONGITUDE"] = df["LONGITUDE"].apply(dms_to_decimal)
df = df.dropna(subset=["LATITUDE", "LONGITUDE"])

# Renomear para padronizar
df.rename(columns={"Município": "Municipio"}, inplace=True)

# === TIRANDO ALGUMAS ESTATÍSTICAS ===
postos_unicos = df.drop_duplicates(subset=["CNPJ"])
total_postos_unicos = len(postos_unicos)

postos_por_produto = df.drop_duplicates(subset=["CNPJ", "Produto"])
contagem_por_produto = postos_por_produto["Produto"].value_counts().reset_index()
contagem_por_produto.columns = ["Produto", "Quantidade"]

tancagem_total = df.groupby("Produto")["Tancagem (m³)"].sum().reset_index()

# === GERANDO O MAPA FOLIUM ===
m = folium.Map(location=[df["LATITUDE"].mean(), df["LONGITUDE"].mean()], zoom_start=8)

# Cores para os produtos
cores = ["red", "green", "blue", "purple", "orange", "black", "gray", "pink", "cadetblue"]
produtos_unicos = df["Produto"].dropna().unique()
cores_produto = {produto: cores[i % len(cores)] for i, produto in enumerate(produtos_unicos)}

# Criando as Camadas por produto
for produto in produtos_unicos:
    camada = folium.FeatureGroup(name=f"Postos - {produto}", show=False)
    df_filtrado = df[df["Produto"] == produto]
    for _, row in df_filtrado.iterrows():
        popup = f"<b>{row['Razão Social']}</b><br>Produto: {produto}<br>Tancagem: {row['Tancagem (m³)']} m³"
        folium.CircleMarker(
            location=[row["LATITUDE"], row["LONGITUDE"]],
            radius=max(5, row["Tancagem (m³)"] / 500),
            popup=folium.Popup(popup, max_width=300),
            color=cores_produto[produto],
            fill=True,
            fill_color=cores_produto[produto],
            fill_opacity=0.7,
        ).add_to(camada)
    m.add_child(camada)

# Usinas
usinas = pd.DataFrame({
    "Nome": [
        "USINA GIASA",
        "Miriri Alimentos e Bioenergia S/A",
        "Japungu Agroindustrial LTDA",
        "Agro Industrial Tabu",
        "D'PADUA Destilação Produção Agroindústria e Comércio SA",
        "Usina Monte Alegre"
    ],
    "Latitude": [-7.3525, -6.9451, -6.9911, -7.5091, -6.6117, -6.8588],
    "Longitude": [-35.0257, -35.1326, -35.0230, -34.8767, -35.0572, -35.1297]
})

for _, row in usinas.iterrows():
    camada = folium.FeatureGroup(name=row["Nome"], show=False)
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"<b>{row['Nome']}</b>",
        icon=folium.Icon(color="darkgreen", icon="industry", prefix="fa")
    ).add_to(camada)
    folium.Circle(
        radius=20000,
        location=[row["Latitude"], row["Longitude"]],
        popup=f"Raio de 20 km da {row['Nome']}",
        color="crimson",
        fill=True,
        fill_opacity=0.1
    ).add_to(camada)
    m.add_child(camada)

# Controle de camadas
folium.LayerControl(collapsed=False).add_to(m)

# === SALVAR ===
output_html = r"D:ADICIONE O CAMINHO DESEJÁVEL AQUI\mapa_postos_usinas.html"
m.save(output_html)

# Codificar mapa para embed
with open(map_file, 'r', encoding='utf-8') as f:
    mapa_html = f.read()
mapa_encoded = base64.b64encode(mapa_html.encode()).decode()
