from Score.tratamento_dados import processar_dados
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def model_randon_forest():
    file_input = 'table_values_csv'
    file = processar_dados(file_input)

    # Definindo as variáveis preditoras (features) e a variável alvo (target)
    X = file[['total_canceladas', 'total_ativas', 'total_finalizadas', 'valor_log']]
    y = file['score_percentage'] # score_percentage

    # Separar os dados em conjuntos de treino e teste (80% treino, 20% teste)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)    

    # Criar e treinar o modelo de Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Fazer previsões com o conjunto de teste
    y_pred_rf = rf_model.predict(X_test)

    # Avaliar o modelo
    mse_rf = mean_squared_error(y_test, y_pred_rf)
    r2_rf = r2_score(y_test, y_pred_rf)

    print(f'Random Forest - Mean Squared Error: {mse_rf}')
    print(f'Random Forest - R² Score: {r2_rf}')

    # Salvar o modelo
    joblib.dump(rf_model, 'modelo_score.pkl')


