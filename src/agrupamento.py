# %%
import pandas as pd
import numpy as np
import folium
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from folium.plugins import MarkerCluster
from kneed import KneeLocator

# %%
# carregar os dados
df = pd.read_csv('data/estado_lat_lon_duplicatas.csv')

# %%
# tirar dados nulos
if df.isnull().values.any():
    print("Tratando valores nulos...")
    df = df.dropna()

# %%
# Normalizando as variáveis para garantir que todas tenham a mesma escala
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[['latitude', 'longitude', 'total_duplicatas']])

# %%
def calculate_wcss(data):
    wcss = []
    for k in range(1, 11):  
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)
    return wcss

def optimal_number_of_clusters(wcss):
    knee = KneeLocator(range(1, len(wcss) + 1), wcss, curve="convex", direction="decreasing")
    return knee.knee

inertia = calculate_wcss(df_scaled)

plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), inertia, marker='o', linestyle='--')
plt.title('Método do Cotovelo')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inércia')
plt.show()

n_clusters = optimal_number_of_clusters(inertia)
print(f"Número ótimo de clusters: {n_clusters}")

# %%
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_scaled)

print(df[['sigla_estado', 'Cluster']])

# %%
novo_arquivo_csv = 'data/estado_clusters.csv'
df.to_csv(novo_arquivo_csv, index=False)

# %%
dff = pd.read_csv('data/estado_clusters.csv')
dff.head(27)

# %%
# 
df['log_total_duplicatas'] = np.log(df['total_duplicatas'] + 1) 

# Definir cores específicas para cada estado
estado_colors = {
    'AC': '#F0FFF0', 'AL': '#FFF0F5', 'AP': '#EE82EE', 'AM': '#FF69B4',
    'BA': '#8B4513', 'CE': '#BA55D3', 'DF': '#808000', 'ES': '#800080',
    'GO': '#FF4500', 'MA': '#CD853F', 'MT': '#00FF00', 'MS': '#FFFF00',
    'MG': '#6A5ACD', 'PA': '#C71585', 'PB': '#DC143C', 'PR': '#FAFAD2',
    'PE': '#FF1493', 'PI': '#F0E68C', 'RJ': '#800000', 'RN': '#FF8C00',
    'RS': '#00FA9A', 'RO': '#7FFFD4', 'RR': '#8A2BE2', 'SC': '#00FFFF',
    'SE': '#6A5ACD', 'SP': '#191970', 'TO': '#0000FF'
}

# Criar mapa centralizado no Brasil
m = folium.Map(location=[-14.235, -51.925], zoom_start=4)

# Camada de satélite utilizando o Esri
folium.TileLayer(
    'Esri.WorldImagery', 
    name='Esri Satellite with Labels',
    overlay=False,
    control=True
).add_to(m)

# Camada padrão do mapa
folium.TileLayer(
    'Esri.WorldStreetMap',  
    name='World StreetMap',
    overlay=True,  
    control=True
).add_to(m)

# Agrupamento de marcadores
marker_cluster = MarkerCluster().add_to(m)

# Adicionar pontos no mapa
for idx, row in df.iterrows():
    estado = row['sigla_estado']
    color = estado_colors.get(estado, '#000000')  # Cor padrão preta caso o estado não tenha cor
    
    # Adicionar bolinhas ao mapa com tooltip que aumenta conforme o zoom
    folium.Circle(
        location=[row['latitude'], row['longitude']],
        radius=row['log_total_duplicatas'] * 5000,  # Ajuste o fator multiplicativo se necessário
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        tooltip=f"Estado: {estado}<br>Total de Duplicatas: {row['total_duplicatas']}" 
    ).add_to(marker_cluster)

# Adicionar legenda manualmente em duas colunas
legend_html = """
<div style="position: fixed; 
            top: 115px; right: 10px; width: 100px; height: auto; 
            background-color: white; z-index:9999; font-size:8px; 
            border:1px solid grey; padding: 5px; border-radius: 5px;">
<h4 style="margin:0; font-size:12px; text-align:center;">Legenda</h4>
<hr style="margin:5px 0; border:none; border-top:1px solid #ccc;">
<div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
"""
for estado, color in estado_colors.items():
    legend_html += f"""
    <div style="width: 48%; margin-bottom: 5px;">
        <i style="background:{color}; width: 10px; height: 10px; float:left; margin-right: 5px; border-radius: 50%;"></i>
        <span style="line-height:10px; font-size:10px;">{estado}</span>
    </div>
    """
legend_html += "</div></div>"

m.get_root().html.add_child(folium.Element(legend_html))


# Adicionar controle de camadas ao mapa
folium.LayerControl().add_to(m)

# Salvar mapa em arquivo HTML
m.save("mapa_interativo.html")

# Mostrar mapa
m

# %%
