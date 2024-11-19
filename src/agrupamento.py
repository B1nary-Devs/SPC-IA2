# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# %%
# carregar os dados
df = pd.read_csv('data/estado_lat_lon_duplicatas.csv')

# %%
# tirar dados nulos
if df.isnull().values.any():
    print("Tratando valores nulos...")
    df = df.dropna()

# %%
# rodar kmeans
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(df[['latitude', 'longitude', 'total_duplicatas']])

print(df[['sigla_estado', 'Cluster']])

# %%
novo_arquivo_csv = 'data/estado_clusters.csv'
df.to_csv(novo_arquivo_csv, index=False)

# %%
dff = pd.read_csv('data/estado_clusters.csv')
dff.head(10)

# %%
# Plotar os clusters em um gráfico de dispersão
plt.figure(figsize=(10, 6))

# Scatter plot usando latitude e longitude
scatter = plt.scatter(
    df['longitude'],
    df['latitude'],
    c=df['Cluster'],  # Coluna de clusters define as cores
    cmap='viridis',  # Colormap para os clusters
    s=df['total_duplicatas'],  # Tamanho dos pontos proporcional ao total de duplicatas
    alpha=0.8  # Transparência para melhor visualização
)

# Adicionar rótulos para os estados
for i, row in df.iterrows():
    plt.text(
        row['longitude'], 
        row['latitude'], 
        row['sigla_estado'], 
        fontsize=9, 
        ha='right'
    )

# Configurações do gráfico
plt.colorbar(scatter, label="Cluster")  # Barra de cores para os clusters
plt.title("Agrupamento de Estados por Geolocalização e Total de Duplicatas", fontsize=14)
plt.xlabel("Longitude", fontsize=12)
plt.ylabel("Latitude", fontsize=12)
plt.grid(True)
plt.show()

# %%
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# %%
# Atribuindo cores aos clusters
colors = ['#5DF534', '#425B26', '#151716', '#876E03', '#E8CECF', '#023411', '#042E54', '#2572D3', '#FD0D0C', '#169C90']
df['color'] = df['Cluster'].map({i: colors[i] for i in range(len(colors))})

# Criando a figura 3D
fig = plt.figure(figsize=(10, 7))
ax = plt.axes(projection="3d")

# Colunas para o gráfico 3D
x_column = 'longitude'  # Coluna correspondente ao eixo X
y_column = 'latitude'   # Coluna correspondente ao eixo Y
z_column = 'total_duplicatas'  # Coluna correspondente ao eixo Z

# Criando o gráfico de dispersão 3D
scatter = ax.scatter3D(
    df[x_column],
    df[y_column],
    df[z_column],
    c=df['color'],  # Cores baseadas no cluster
    alpha=0.8,      # Transparência
    s=50            # Tamanho dos pontos
)

# Configurando os rótulos dos eixos
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Total de Duplicatas')

# Adicionando título
plt.title('Clusters Gerados pelo K-means')

# Exibindo o gráfico
plt.show()

# %%
import folium
import pandas as pd

# %%
# Criar um mapa centralizado no Brasil
mapa = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

# Adicionar marcadores para cada estado
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['total_duplicatas'] / 250,  # Escalar o tamanho
        popup=f"{row['sigla_estado']}: {row['total_duplicatas']} duplicatas",
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(mapa)

# Salvar o mapa como arquivo HTML ou exibir no notebook
mapa.save("mapa_interativo.html")
mapa

# %%
