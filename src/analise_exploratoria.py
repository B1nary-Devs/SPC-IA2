
# %%
import etl
import pandas as pd
import matplotlib.pyplot as plt

# %% 
df = pd.read_csv('data/asset_trade_bills.csv')
df.describe()

# Contagens
# %%
# Filtrar apenas os registros do tipo 'finished'
df_service = df[df['state'] == 'finished']

# Contar quantos 'finished' existem por mês
finished_counts = df_service['periodo'].value_counts().to_dict()
# print(finished_counts)

# %%
# Filtrar apenas os registros do tipo 'active'
df_service = df[df['state'] == 'active']

# Contar quantos 'active' existem por mês
active_counts = df_service['periodo'].value_counts().to_dict()
# print(active_counts)

# %%
# Filtrar apenas os registros do tipo 'canceled'
df_service = df[df['state'] == 'canceled']

# Contar quantos 'canceled' existem por mês
cancelados_counts = df_service['periodo'].value_counts().to_dict()
# print(cancelados_counts)

# %%
# Contar quantos 'kinds' existem por mês
kinds_counts = df['periodo'].value_counts().to_dict()
# print(kinds_counts)

# %%
## Contagem de goods e services
df.groupby('kind').size().sort_values().to_dict()

# ---

## Kind GOODS

# %%
# Filtrar apenas os registros do tipo 'goods'
df_service = df[df['kind'] == 'goods']

# Contar quantos 'goods' existem por mês
goods_counts = df_service['periodo'].value_counts().to_dict()
# print(goods_counts)

# %%
## Contagem dos estados que possuem mais vendas de goods
qtd_estado_goods = df.query('kind == "goods"')['sigla_estado'].value_counts().head().to_dict()
# print(qtd_estado_goods)

# %%
## Contagem dos estados que possuem mais cancelados a partir do kind goods
qtd_estados_canceled_goods = df.query('kind == "goods" and state == "canceled"')['sigla_estado'].value_counts().head().to_dict()
# print(qtd_estados_canceled_goods)

# %%
## Contagem dos estados que possuem mais finalizados a partir do kind goods
qtd_estados_finished_goods = df.query('kind == "goods" and state == "finished"')['sigla_estado'].value_counts().head().to_dict()
# print(qtd_estados_finished_goods)

# %%
## Contagem dos estados que possuem mais active a partir do kind goods
qtd_estados_active_goods = df.query('kind == "goods" and state == "finished"')['sigla_estado'].value_counts().head().to_dict()
# print(qtd_estados_active_goods)

# ---

## Kind SERVICES

# %%
# Filtrar apenas os registros do tipo 'service'
df_service = df[df['kind'] == 'services']

# Contar quantos 'service' existem por mês
service_counts = df_service['periodo'].value_counts().to_dict()
# print(service_counts)

# %%
## Contagem dos estados que possuem mais vendas de services
qtd_estado_services = df.query('kind == "services"')['sigla_estado'].value_counts().head().to_dict()
# print(qtd_estado_services)

# %%
## Contagem dos estados que possuem mais cancelados a partir do kind services
qtd_estados_cancelados_services = df.query('kind == "services" and state == "canceled"')['sigla_estado'].value_counts().head().to_dict()
# print(qtd_estados_cancelados_services)

# %%
## Contagem dos estados que possuem mais finalizados a partir do kind services
qtd_estados_finished_services = df.query('kind == "services" and state == "finished"')['sigla_estado'].value_counts().head().to_dict()
# print(qtd_estados_finished_services)

# %%
## Contagem dos estados que possuem mais active a partir do kind services
qtd_estados_active_services = df.query('kind == "services" and state == "finished"')['sigla_estado'].value_counts().head().to_dict()
# print(qtd_estados_active_services)

# --------------------------------------------------------------------------------------------------------------------------

# Porcentagens

# Kind GOODS
# %%
### Porcentagem dos estados que possuem mais canceled a partir do kind goods
porc_estados_canceled_goods = df.query('kind == "goods" and state == "canceled"')['sigla_estado'].value_counts(normalize=True).head().mul(100).round(2).to_dict()
# print(porc_estados_canceled_goods)

# %%
### Porcentagem dos estados que possuem mais active a partir do kind goods
porc_estados_active_goods = df.query('kind == "goods" and state == "active"')['sigla_estado'].value_counts(normalize=True).head().mul(100).round(2).to_dict()
# print(porc_estados_active_goods)

# %%
### Porcentagem dos estados que possuem mais finalizados a partir do kind goods
porc_estados_finished_goods = df.query('kind == "goods" and state == "finished"')['sigla_estado'].value_counts(normalize=True).head().mul(100).round(2).to_dict()
# print(porc_estados_finished_goods)

# ---

# Kind SERVICES
# %%
### Porcentagem dos estados que possuem mais cancelados a partir do kind services
porc_estados_canceled_services = df.query('kind == "services" and state == "canceled"')['sigla_estado'].value_counts(normalize=True).head().mul(100).round(2).to_dict()
# print(porc_estados_canceled_services)

# %%
### Porcentagem dos estados que possuem mais ativos a partir do kind goods
porc_estados_active_services = df.query('kind == "services" and state == "active"')['sigla_estado'].value_counts(normalize=True).head().mul(100).round(2).to_dict()
# print(porc_estados_active_services)

# %%
### Porcentagem dos estados que possuem mais finalizados a partir do kind goods
porc_estados_finished_services = df.query('kind == "services" and state == "finished"')['sigla_estado'].value_counts(normalize=True).head().mul(100).round(2).to_dict()
# print(porc_estados_finished_services)


# --------------------------------------------------------------------------------------------------------------------------

# Gráficos
# %%
# Gráfico quantitativo de goods e services
df.groupby('kind').size().sort_values().plot(kind='barh')

# Kind GOODS
# %%
# Gráfico apresentando os estados que possuem mais vendas de goods
df.query('kind == "goods"')['sigla_estado'].value_counts().head().plot(kind='barh')

# %%
# Grafico dos estados que possuem mais cancelados a partir do kind goods
df.query('kind == "goods" and state == "canceled"')['sigla_estado'].value_counts().head().plot(kind='barh')

# %%
# Grafico dos estados que possuem mais finalizados a partir do kind goods
df.query('kind == "goods" and state == "finished"')['sigla_estado'].value_counts().head().plot(kind='barh')

# %%
# Grafico dos estados que possuem mais ativos a partir do kind goods
df.query('kind == "goods" and state == "active"')['sigla_estado'].value_counts().head().plot(kind='barh')

# ---

# Kind SERVICES

# %%
# Gráfico apresentando os estados que possuem mais vendas de services
df.query('kind == "services"')['sigla_estado'].value_counts().head().plot(kind='barh')

# %%
# Grafico dos estados que possuem mais cancelados a partir do kind services
df.query('kind == "services" and state == "canceled"')['sigla_estado'].value_counts().head().plot(kind='barh')

# %%
# Grafico dos estados que possuem mais finalizados a partir do kind services
df.query('kind == "services" and state == "finished"')['sigla_estado'].value_counts().head().plot(kind='barh')

# %%
# Grafico dos estados que possuem mais ativos a partir do kind services
df.query('kind == "services" and state == "active"')['sigla_estado'].value_counts().head().plot(kind='barh')
