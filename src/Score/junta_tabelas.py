import pandas as pd

# Carregar o arquivo original e o arquivo com os scores
filename_original = 'table_values_csv.csv'
filename_scores = 'classified_scores_endorser_payer.csv'

df_original = pd.read_csv(filename_original)
df_scores = pd.read_csv(filename_scores)

# Juntar o score_x baseado no document_number_x
df_combined_x = pd.merge(df_original, df_scores[['document_number_x', 'score_x']],
                         left_on='document_number_x', right_on='document_number_x', how='left')

# Juntar o score_y baseado no document_number_y
df_combined_xy = pd.merge(df_combined_x, df_scores[['document_number_y', 'score_y']],
                          left_on='document_number_y', right_on='document_number_y', how='left')

# Salvar o DataFrame combinado com os scores em um novo arquivo CSV
df_combined_xy.to_csv('table_values_with_scores.csv', index=False)

print("O arquivo com os scores foi salvo como 'table_values_with_scores.csv'.")
