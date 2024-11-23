# %%
import pandas as pd
import re
import os
from unidecode import unidecode
from geopy.distance import geodesic
import json

# %%
# Dicionário de coordenadas dos estados
estado_coords = {
    'AC': (-9.9756, -70.8078),  # Acre
    'AL': (-9.6445, -35.7378),  # Alagoas
    'AP': (-1.4478, -51.7731),  # Amapá
    'AM': (-3.0986, -60.0219),  # Amazonas
    'BA': (-12.9714, -38.5014),  # Bahia
    'CE': (-3.7197, -38.5389),  # Ceará
    'DF': (-15.7801, -47.9292),  # Distrito Federal
    'ES': (-19.1953, -40.2927),  # Espírito Santo
    'GO': (-16.6749, -49.2455),  # Goiás
    'MA': (-5.4483, -44.2948),  # Maranhão
    'MT': (-12.5755, -55.7081),  # Mato Grosso
    'MS': (-20.9037, -54.9081),  # Mato Grosso do Sul
    'MG': (-19.9167, -43.9333),  # Minas Gerais
    'PA': (-2.8278, -53.2193),  # Pará
    'PB': (-6.8825, -35.2042),  # Paraíba
    'PR': (-25.4278, -51.9253),  # Paraná
    'PE': (-8.0543, -35.2042),  # Pernambuco
    'PI': (-5.0901, -42.8153),  # Piauí
    'RJ': (-22.9083, -43.1828),  # Rio de Janeiro
    'RN': (-5.8142, -35.2042),  # Rio Grande do Norte
    'RS': (-30.0333, -51.2167),  # Rio Grande do Sul
    'RO': (-9.2500, -63.9167),  # Rondônia
    'RR': (-3.0694, -60.8278),  # Roraima
    'SC': (-27.5950, -48.5490),  # Santa Catarina
    'SE': (-10.8925, -37.0833),  # Sergipe
    'SP': (-23.5505, -46.6333),  # São Paulo
    'TO': (-9.5378, -48.3328)   # Tocantins
}

# Dicionário para conversão de nomes de estados para siglas
estados_siglas = {
    'ACRE': 'AC', 'ALAGOAS': 'AL', 'AMAPA': 'AP', 'AMAZONAS': 'AM',
    'BAHIA': 'BA', 'CEARA': 'CE', 'DISTRITO FEDERAL': 'DF', 'ESPIRITO SANTO': 'ES',
    'GOIAS': 'GO', 'MARANHAO': 'MA', 'MATO GROSSO': 'MT', 'MATO GROSSO DO SUL': 'MS',
    'MINAS GERAIS': 'MG', 'PARA': 'PA', 'PARAIBA': 'PB', 'PARANA': 'PR',
    'PERNAMBUCO': 'PE', 'PIAUI': 'PI', 'RIO DE JANEIRO': 'RJ', 'RIO GRANDE DO NORTE': 'RN',
    'RIO GRANDE DO SUL': 'RS', 'RONDONIA': 'RO', 'RORAIMA': 'RR', 'SANTA CATARINA': 'SC',
    'SAO PAULO': 'SP', 'SERGIPE': 'SE', 'TOCANTINS': 'TO'
}

# Dicionário do mês
meses = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Marco', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

# %%
def calcular_distancia(sigla_estado_atual, sigla_estado_frequente):
    if sigla_estado_atual in estado_coords and sigla_estado_frequente in estado_coords:
        coordenadas_atual = estado_coords[sigla_estado_atual]
        coordenadas_frequente = estado_coords[sigla_estado_frequente]
        distancia = geodesic(coordenadas_atual, coordenadas_frequente).kilometers
        return distancia
    else:
        return None

def limpar_texto(texto):
    if isinstance(texto, str):
        texto = re.sub(r'[\d\-]', '', texto)
        texto = unidecode(texto).upper()
    else:
        texto = ''
    return texto

def obter_sigla_estado(texto):
    for estado, sigla in estados_siglas.items():
        if texto == estado:
            return sigla
    palavras = texto.split()
    for palavra in palavras:
        for estado, sigla in estados_siglas.items():
            if palavra == estado or palavra == sigla:
                return sigla
    return None


# %%
df = pd.read_csv('data/asset_trade_bills.csv')

dp = pd.read_csv('data/participants.csv')

# %%

df['payment_place'] = df['payment_place'].apply(limpar_texto)
df['sigla_estado'] = df['payment_place'].apply(obter_sigla_estado)

#Preenchendo valores ausentes 
df['sigla_estado'].fillna('NA', inplace=True)
df['participant_id'].fillna(0, inplace=True) 

# Mesclar com nome do participante no csv 
df = pd.merge(df, dp[['id', 'name']], left_on='participant_id', right_on='id', how='left')

# Cálculo de estado padrão, distancia e possível fraude
df['estado_frequente'] = df.groupby('participant_id')['sigla_estado'].transform(lambda x: x.mode()[0])
df['distancia'] = df.apply(lambda row: calcular_distancia(row['sigla_estado'], row['estado_frequente']), axis=1)
df['is_fraud'] = df['distancia'].apply(lambda x: 1 if x > 0 else 0)

# Tratamento de dados para ter o mês das operações
# Converter a coluna 'new_due_date_formated' para datetime, lidando com formatos mistos
df['new_due_date_formated'] = pd.to_datetime(df['new_due_date'], errors='coerce', dayfirst=False)

# Criar a coluna 'mes' extraindo o mês da data
df['mes'] = df['new_due_date_formated'].dt.month

# Criar a coluna 'periodo' mapeando os números do mês para os nomes
df['periodo'] = df['mes'].map(meses)

nome_arquivo = 'data/asset_trade_bills.csv'
df.to_csv(nome_arquivo, index=False)

# %% 
novo_df = df.groupby('sigla_estado').agg(
    total_duplicatas=('sigla_estado', 'size')
).reset_index()

novo_df['latitude'] = novo_df['sigla_estado'].apply(lambda x: estado_coords.get(x, (None, None))[0])
novo_df['longitude'] = novo_df['sigla_estado'].apply(lambda x: estado_coords.get(x, (None, None))[1])

novo_arquivo_csv = 'data/estado_lat_lon_duplicatas.csv'
novo_df.to_csv(novo_arquivo_csv, index=False)

print(f"Novo arquivo criado: {novo_arquivo_csv}")

# %%
de = pd.read_csv('data/estado_lat_lon_duplicatas.csv')
# %%
de.describe()
de.head(10)
# %%
