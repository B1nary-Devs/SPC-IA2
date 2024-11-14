import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

def prever_proximos_meses(df, order=(1,1,0)):
    # # Garantir que o índice 'mes_referencia' está configurado corretamente
    # df.set_index('mes_referencia', inplace=True)

    df['data'] = pd.to_datetime(df['mes_referencia'].astype(str), format='%m')
    df.set_index('data', inplace=True)
    df.index = pd.date_range(start=df.index[0], periods=len(df), freq='MS')
    
    
    # Escolher o modelo ARIMA com a ordem fornecida
    modelo = ARIMA(df['total_registros'], order=order)
    model_fit = modelo.fit()

    # Previsão para os próximos 2 meses
    forecast = model_fit.forecast(steps=2)

    previsoes = np.array(forecast)
    # Ajustar a previsão para inteiros
    previsoes = previsoes.astype(int)

    return previsoes


def tratamentoDado(df):
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Extrai o mês da coluna de datas
    df['mes_referencia'] = df['created_at'].dt.month
    
    # Agora podemos agrupar por mês e período (antes ou após o dia 15) e contar os registros (total_registros)
    df_mensal = df.groupby(['mes_referencia']).agg(
        total_registros=('id_x', 'size')
    ).reset_index()

    df_mensal = df_mensal[~df_mensal['mes_referencia'].isin([9, 10, 11, 12])]

    return df_mensal

def previsao(df):
    df_tratado = tratamentoDado(df)
    previsao = prever_proximos_meses(df_tratado)
    return previsao


# filename = 'table_values_csv.csv'
df = pd.read_csv(r'C:\Users\Noite\Documents\api\SPC-IA\SPC-IA2\src\Conciliacao\table_values_csv.csv', sep=',',low_memory=False)
previsao = previsao(df)

print(previsao)