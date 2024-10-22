import joblib
import pandas as pd
import numpy as np

def model_score(total_canceladas, total_ativas, total_finalizadas, total_monetario):
    # Carregar o modelo
    model = joblib.load('modelo_score.pkl')

    # Criar um dicionário com os dados
    data = {
        'total_canceladas': [total_canceladas],
        'total_ativas': [total_ativas],
        'total_finalizadas': [total_finalizadas],
        'total_monetario': [total_monetario]
    }

    # Convertendo o dicionário para um DataFrame para o modelo fazer previsões
    df = pd.DataFrame(data)

    # Aplicar a transformação logarítmica ao valor_total
    df['valor_log'] = np.log1p(df['total_monetario'])

    # Fazer a previsão do score para esses novos dados
    predicted_score = model.predict(df)

    # Exibir a previsão
    print(f'O score previsto para os novos dados é: {predicted_score[0]}')

    return predicted_score

