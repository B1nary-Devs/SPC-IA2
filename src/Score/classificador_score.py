import pandas as pd
import numpy as np
import joblib



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
    df['total_monetario'] = np.log1p(df['total_monetario'])

    # Fazer a previsão do score para esses novos dados
    predicted_score = model.predict(df)

    # Exibir a previsão
    print(f'O score previsto para os novos dados é: {predicted_score[0]}')

    return predicted_score[0]


# Carregar o arquivo CSV gerado anteriormente
df = pd.read_csv('aggregated_endorser_payer.csv')

# Adicionar prints para verificar o progresso
print("Iniciando o cálculo dos scores...")

# Criar a coluna score_x (para document_number_x)
for index, row in df.iterrows():
    df.at[index, 'score_x'] = model_score(
        row['total_canceladas_payer'] if 'total_canceladas_payer' in row else 0,
        row['total_ativas_payer'] if 'total_ativas_payer' in row else 0,
        row['total_finalizadas_payer'] if 'total_finalizadas_payer' in row else 0,
        row['total_valor_payer'] if 'total_valor_payer' in row else 0
    ) if pd.notna(row['total_canceladas_payer']) else None

    # Exibir progresso a cada 100 linhas processadas
    if index % 100 == 0:
        print(f"Processando linha {index} para score_x")

# Criar a coluna score_y (para document_number_y)
for index, row in df.iterrows():
    df.at[index, 'score_y'] = model_score(
        row['total_canceladas_endorser'] if 'total_canceladas_endorser' in row else 0,
        row['total_ativas_endorser'] if 'total_ativas_endorser' in row else 0,
        row['total_finalizadas_endorser'] if 'total_finalizadas_endorser' in row else 0,
        row['total_valor_endorser'] if 'total_valor_endorser' in row else 0
    ) if pd.notna(row['total_canceladas_endorser']) else None

    # Exibir progresso a cada 100 linhas processadas
    if index % 100 == 0:
        print(f"Processando linha {index} para score_y")

# Salvar o DataFrame com as novas colunas de score em um arquivo CSV
df.to_csv('classified_scores_endorser_payer.csv', index=False)

print("O arquivo com os scores foi salvo como 'classified_scores_endorser_payer.csv'.")
