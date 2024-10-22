import pandas as pd
import numpy as np

def processar_dados(file_input):
    # Lê e trata os dados
    df = readDoc(file_input)
    df_tratado = tratamento(df)
    
    # Agrupa os dados por payer e endorser
    df_payer = agrupamento_payer(df_tratado)
    df_endorser = agrupamento_endosser(df_tratado)
    
    # Junta as tabelas
    df_consolidado = juncao_tabela_total(df_payer, df_endorser)
    
    # Normaliza os scores
    df_final = normalizacao_score(df_consolidado)
    
    return df_final


def readDoc(fileName):
    filename = fileName
    # filename = 'table_values_csv.csv'
    df = pd.read_csv(filename, sep=',',low_memory=False)
    print(df.head())
    return df


def tratamento(df):
    # Dropando colunas desnecessaria ou com muito nulos
    df = df.drop(columns=['id_x', 'number', 'new_due_date', 'nfe_number', 'nfe_series', 'contact_phone_number_x', 'contact_phone_number_y', 'contact_phone_number', 'contact_email_x', 'finished_at', 'created_at_x', 'updated_at_x', 'new_due_date.1', 'contact_email_y', 'created_at_y', 'updated_at_y', 'invoice_number', 'authorized_third_party_id', 'paymaster_id', 'update_reason_kind' ], axis=1)

    # Converter colunas de datas para o tipo datetime
    df['due_date'] = pd.to_datetime(df['due_date'])
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    
    # Remover linhas com valores nulos nas colunas específicas
    df_cleaned = df.dropna(subset=['participant_id_x', 'name', 'state_y', 'document_number', 'company_name', 'kind_y'])
    df = df_cleaned
    df.isna().sum()

    # Converter a coluna para inteiros
    df['document_number_x'] = df['document_number_x'].astype(int)
    df['document_number_y'] = df['document_number_y'].astype(int)
    df['document_number'] = df['document_number'].astype(int)

    return df

def agrupamento_payer(df):
    # Agrupamento por payer_id
    df_payer = df.groupby('document_number_x').agg(
        total_canceladas_payer=('state_x', lambda x: (x == 'canceled').sum()),
        total_ativas_payer=('state_x', lambda x: (x == 'active').sum()),
        total_finalizadas_payer=('state_x', lambda x: (x == 'finished').sum()),
        total_valor_payer=('value', 'sum')
    ).reset_index()

    #Top 1 canceladas
    top_1_payer_c = df_payer.nlargest(1, 'total_canceladas_payer')

    #Top 1 atrivas
    top_1_payer_a = df_payer.nlargest(1, 'total_ativas_payer')

    #Top 1 finalizadas
    top_1_payer_f = df_payer.nlargest(1, 'total_finalizadas_payer')

    #Top 1 valor
    top_1_payer_v = df_payer.nlargest(1, 'total_valor_payer')

    #Dropando o dado com mais casos
    df_payer = df_payer[~df_payer['document_number_x'].isin(top_1_payer_c['document_number_x'])]
    df_payer = df_payer[~df_payer['document_number_x'].isin(top_1_payer_a['document_number_x'])]
    df_payer = df_payer[~df_payer['document_number_x'].isin(top_1_payer_f['document_number_x'])]
    df_payer = df_payer[~df_payer['document_number_x'].isin(top_1_payer_v['document_number_x'])]

    top_1_payer_c = df_payer.nlargest(1, 'total_canceladas_payer')
    top_1_payer_a = df_payer.nlargest(1, 'total_ativas_payer')
    top_1_payer_f = df_payer.nlargest(1, 'total_finalizadas_payer')
    top_1_payer_v = df_payer.nlargest(1, 'total_valor_payer')

    return df_payer

def agrupamento_endosser(df):
    # Agrupar por endorser_original_id
    df_endorser = df.groupby('document_number_y').agg(
        total_canceladas_endorser=('state_x', lambda x: (x == 'canceled').sum()),
        total_ativas_endorser=('state_x', lambda x: (x == 'active').sum()),
        total_finalizadas_endorser=('state_x', lambda x: (x == 'finished').sum()),
        total_valor_endorser=('value', 'sum')
    ).reset_index()


    #Top 1 canceladas
    top_1_endorser_c = df_endorser.nlargest(1, 'total_canceladas_endorser')

    #Top 1 atrivas
    top_1_endorser_a = df_endorser.nlargest(1, 'total_ativas_endorser')

    #Top 1 finalizadas
    top_1_endorser_f = df_endorser.nlargest(1, 'total_finalizadas_endorser')

    #Top 1 valor
    top_1_endorser_v = df_endorser.nlargest(1, 'total_valor_endorser')

    #Dropando o dado com mais casos
    df_endorser = df_endorser[~df_endorser['document_number_y'].isin(top_1_endorser_c['document_number_y'])]
    df_endorser = df_endorser[~df_endorser['document_number_y'].isin(top_1_endorser_a['document_number_y'])]
    df_endorser = df_endorser[~df_endorser['document_number_y'].isin(top_1_endorser_f['document_number_y'])]
    df_endorser = df_endorser[~df_endorser['document_number_y'].isin(top_1_endorser_v['document_number_y'])]

    return df_endorser


def juncao_tabela_total(df_payer, df_endorser):
    # Renomear colunas para manter consistência
    df_payer = df_payer.rename(columns={'document_number_x': 'document_number', 'total_canceladas_payer': 'total_canceladas', 'total_ativas_payer': 'total_ativas', 'total_finalizadas_payer': 'total_finalizadas', 'total_valor_payer': 'total_valor'})
    df_endorser = df_endorser.rename(columns={'document_number_y': 'document_number', 'total_canceladas_endorser': 'total_canceladas', 'total_ativas_endorser': 'total_ativas', 'total_finalizadas_endorser': 'total_finalizadas', 'total_valor_endorser': 'total_valor'})

    # Concatenar as tabelas
    df_consolidado = pd.concat([df_payer, df_endorser], ignore_index=True)
    return df_consolidado

def normalizacao_score(df):
    df_media_desvio = df

    # Valor Logarizado
    # Aplicar a transformação logarítmica ao valor_total
    df_media_desvio['total_monetario'] = np.log1p(df_media_desvio['total_valor'])

    # # SCORE Logarizado
    df_media_desvio['score'] = (
        ((df_media_desvio['total_finalizadas'] * 0.77) +    # Peso 77% para finalizadas
        (df_media_desvio['total_ativas'] * 0.015) +         # Peso 1.5% para ativas
        (df_media_desvio['total_monetario'] * 0.27)) -            # Peso 27% para valor normalizado
        (df_media_desvio['total_canceladas'] * 0.10)        # Peso 10% para canceladas
    )

    # Normalizando o score para uma escala percentual
    df_media_desvio['score_percentage'] = (
        (df_media_desvio['score'] - df_media_desvio['score'].min()) /
        (df_media_desvio['score'].max() - df_media_desvio['score'].min()) * 
        100
    )
    
    return df_media_desvio

    
