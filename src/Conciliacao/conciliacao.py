import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

def prever_proximos_meses(df, order=(1,1,0)):
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
    # Extrai o ano da coluna de datas
    df['ano_referencia'] = df['created_at'].dt.year

    # Agora podemos agrupar por mês e período (antes ou após o dia 15) e contar os registros (total_registros)
    df_mensal = df.groupby(['mes_referencia', 'ano_referencia']).agg(
        total_registros=('id_x', 'size')
    ).reset_index()

    df_anual = df_mensal[df_mensal['ano_referencia'] == 2024]

    return df_anual

def previsao(df):
    df_tratado = tratamentoDado(df)
    previsao = prever_proximos_meses(df_tratado)
    return previsao


# filename = 'table_values_csv.csv'
df = pd.read_csv(r'C:\Users\Noite\Documents\api\SPC-IA\SPC-IA2\src\Conciliacao\table_values_csv.csv', sep=',',low_memory=False)
previsao = previsao(df)

print(previsao)