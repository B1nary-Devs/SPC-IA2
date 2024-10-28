# Importação das dependências
import pandas as pd
import numpy as np
import json
import uuid
from datetime import datetime

# Leitura do arquivo CSV
filename = 'table_values_with_scores.csv'
df = pd.read_csv(filename, sep=',', low_memory=False)

# Dropando colunas desnecessárias ou com muitos nulos
df = df.drop(columns=[
    'id_x', 'number', 'nfe_number', 'nfe_series',
    'contact_phone_number_y', 'contact_phone_number',
    'created_at_x', 'updated_at_x', 'created_at_y', 'updated_at_y', 'invoice_number',
    'authorized_third_party_id', 'paymaster_id', 'update_reason_kind'
], axis=1)

# Converter colunas de datas para o tipo datetime
df['due_date'] = pd.to_datetime(df['due_date'])
df['created_at'] = pd.to_datetime(df['created_at'])
df['updated_at'] = pd.to_datetime(df['updated_at'])
df['new_due_date'] = pd.to_datetime(df['new_due_date'])

def remover_decimal(valor):
    # Verifica se o valor termina com '.0' e remove
    if valor.endswith('.0'):
        return valor[:-2]
    return valor

# Aplicar a função às colunas 'score_x' e 'score_y'
df['score_x'] = df['score_x'].round(0).astype(str).apply(remover_decimal)
df['score_y'] = df['score_y'].round(0).astype(str).apply(remover_decimal)
df['contact_email_x'] = df['contact_email_x'].fillna('')


# Criar a coluna 'status' com base nas condições
# 1. Se 'finished_at' tiver valor, colocar 'finalizado'
# 2. Se 'new_due_date' for anterior a hoje, colocar 'vencida'
# 3. Se 'new_due_date' for posterior a hoje, colocar 'a vencer'
df['status'] = np.where(pd.notna(df['finished_at']), 'finalizado',
                        np.where(df['new_due_date'] < datetime.now(), 'vencida', 'a vencer'))

# Remover linhas com valores nulos nas colunas específicas
df_cleaned = df.dropna(subset=['participant_id_x', 'name', 'state_y', 'document_number', 'company_name', 'kind_y'])
df = df_cleaned
df.isna().sum()

# Converter colunas para inteiros
df['document_number_x'] = df['document_number_x'].astype(int)
df['document_number_y'] = df['document_number_y'].astype(int)
df['document_number'] = df['document_number'].astype(int)
# Remover o ".0" ao converter os valores de contact_phone_number_x para string
df['contact_phone_number_x'] = df['contact_phone_number_x'].apply(lambda x: str(int(x)) if pd.notna(x) else None)

# Função para gerar a estrutura do sacado
def gerar_sacado(grupo):
    sacado = {
        "cessionaria_sacado_id": str(uuid.uuid4()),
        "cessionaria_sacado_cnpj": grupo['document_number_x'],
        "cessionaria_sacado_score": grupo['score_x'],
        "cessionaria_sacado_duplicadas_data_inicial": grupo['due_date'].strftime('%Y-%m-%d') if pd.notna(grupo['due_date']) else None,
        "cessionaria_sacado_duplicadas_data_final": grupo['new_due_date'].strftime('%Y-%m-%d') if pd.notna(grupo['new_due_date']) else None,
        "cessionaria_sacado_duplicata_status": grupo['status'],
        "cessionaria_sacado_nome": grupo['name_x'],
        "cessionaria_sacado_contato": grupo['contact_phone_number_x'],
        "cessionaria_sacado_email": grupo['contact_email_x'],
        "cessionaria_sacado_data_pagamento": grupo['new_due_date'].strftime('%Y-%m-%d') if grupo['status'] == 'finalizado' and pd.notna(grupo['new_due_date']) else None
    }
    return sacado


# Função para gerar a estrutura final agrupada por cessionária (endosser)
def gerar_estrutura_json(df):
    cessionarias = []

    # Agrupar por Cessionária (document_number_y e name_y)
    grouped = df.groupby(['document_number_y', 'name_y', 'score_y'])

    for (cessionaria_cnpj, cessionaria_nome, cossionaria_socre), grupo in grouped:
        sacados = grupo.apply(gerar_sacado, axis=1).tolist()

        cessionaria = {
            "cessionaria_nome": cessionaria_nome,
            "cessionaria_cnpj": str(cessionaria_cnpj),
            "cessionaria_score": cossionaria_socre,
            "cessionaria_sacado": sacados
        }

        cessionarias.append(cessionaria)

    return cessionarias

# Chamar a função para gerar a estrutura JSON
estrutura_json = gerar_estrutura_json(df)

# Exibir o JSON estruturado
print(json.dumps(estrutura_json, indent=4, ensure_ascii=False))

# Caso você queira salvar a estrutura JSON em um arquivo
with open('resultado_cessionarias8.json', 'w', encoding='utf-8') as f:
    json.dump(estrutura_json, f, ensure_ascii=False, indent=4)