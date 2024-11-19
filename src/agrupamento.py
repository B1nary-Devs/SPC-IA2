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
# Método do Cotovelo: Calcular a inércia para diferentes valores de k
inertia = []
for k in range(1, 11):  # Testando de 1 a 10 clusters
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_scaled)
    inertia.append(kmeans.inertia_)

# Plotando o gráfico do método do cotovelo
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), inertia, marker='o', linestyle='--')
plt.title('Método do Cotovelo')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inércia')
plt.show()

# %%
# Escolher o número de clusters baseado no cotovelo (por exemplo, k=3)
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_scaled)

print(df[['sigla_estado', 'Cluster']])

# %%
novo_arquivo_csv = 'data/estado_clusters.csv'
df.to_csv(novo_arquivo_csv, index=False)

# %%
dff = pd.read_csv('data/estado_clusters.csv')
dff.head(10)

# %%
# Transformação logarítmica no total de duplicatas para evitar bolhas muito pequenas
df['log_total_duplicatas'] = np.log(df['total_duplicatas'] + 1)  # Adiciona 1 para evitar log(0)

# Criar o mapa centralizado no Brasil
m = folium.Map(location=[-14.235, -51.925], zoom_start=4)

# Adicionar a camada de satélite utilizando o provedor Esri
folium.TileLayer(
    'Esri.WorldImagery',  # Usando a camada de satélite do Esri
    name='Esri Satellite with Labels',
    overlay=False,  # A camada de satélite será sobreposta ao mapa
    control=True
).add_to(m)

# Adicionar a camada padrão do mapa (CartoDB positron)
folium.TileLayer(
    'Esri.WorldStreetMap',  # Usando o estilo de mapa padrão CartoDB
    name='World StreetMap',
    overlay=True,  # A camada padrão será sobreposta também
    control=True
).add_to(m)

# Criar o agrupamento de marcadores
marker_cluster = MarkerCluster().add_to(m)

# Gerar cores únicas para cada estado utilizando matplotlib
estado_colors = {estado: plt.cm.get_cmap("tab10")(i) for i, estado in enumerate(df['sigla_estado'].unique())}

# Adicionar os pontos (bolhas) no mapa
for idx, row in df.iterrows():
    estado = row['sigla_estado']
    
    # Obter a cor do estado
    color = estado_colors[estado]
    hex_color = matplotlib.colors.rgb2hex(color)  # Converter para formato hex
    
    # Adicionar a bolinha com tooltip (informação visível ao passar o mouse)
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['log_total_duplicatas'] * 2,  # Ajustando o tamanho com base no valor logarítmico
        color=hex_color,
        fill=True,
        fill_color=hex_color,
        fill_opacity=0.6,
        tooltip=f"Estado: {estado}<br>Total de Duplicatas: {row['total_duplicatas']}"  # Exibe total de duplicatas ao passar o mouse
    ).add_to(marker_cluster)

# Adicionar o controle de camadas para alternar entre o satélite e o mapa padrão
folium.LayerControl().add_to(m)

m.save("mapa_interativo.html")

# Exibir o mapa no Jupyter
m
# %%
