# %%
from analise_exploratoria import *
import pandas as pd
import json

# %%
df = pd.read_csv('data/asset_trade_bills.csv')
dp = pd.read_csv('data/participants.csv')

# --------------------------------------------------------------------------------------------------------------------------
# JSON
#%%
#Guardando os dicionarios em txt formato json
all_dicionarios = {
    'kinds_counts': kinds_counts,
    'service_counts': service_counts,
    'goods_counts': goods_counts,
    'cancelados_counts': cancelados_counts,
    'active_counts': active_counts,
    'finished_counts': finished_counts,
    'qtd_estado_goods': qtd_estado_goods,
    'qtd_estados_canceled_goods': qtd_estados_canceled_goods,
    'qtd_estados_finished_goods': qtd_estados_finished_goods,
    'qtd_estados_active_goods': qtd_estados_active_goods,
    'qtd_estado_services': qtd_estado_services,
    'qtd_estados_cancelados_services': qtd_estados_cancelados_services,
    'qtd_estados_finished_services': qtd_estados_finished_services,
    'qtd_estados_active_services': qtd_estados_active_services
}

with open('data/dicionarios_counts_final.json', 'w') as file:
    json.dump(all_dicionarios, file, indent=4)
