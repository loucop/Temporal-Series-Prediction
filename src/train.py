# train.py (Com adição do R-squared)

import numpy as np
import joblib
from sklearn.model_selection import train_test_split
# 1. IMPORTAR A FUNÇÃO r2_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score 
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import config
from utils import carregar_dados_de_features

def avaliar(y_true, y_pred, nome_modelo):
    """
    Calcula e exibe as métricas de avaliação do modelo, incluindo R².
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)  # 2. CALCULA O R-SQUARED

    print(f"--- Métricas para {nome_modelo} ---")
    print(f"MAE (Erro Médio Absoluto): {mae:.2f}")
    print(f"RMSE (Raiz do Erro Quadrático Médio): {rmse:.2f}")
    print(f"R² (R-squared): {r2:.2f}") # 3. EXIBE O R-SQUARED
    print("-" * 30)

def main():
    """
    Função principal que orquestra o treinamento e avaliação dos modelos.
    """
    print("\n--- Iniciando processo de treinamento (SIMULAÇÃO REALISTA SEM 'COLA') ---")
    
    X, y, _ = carregar_dados_de_features(config.FEATURES_DATA_PATH)

    print("\nRemovendo features com conhecimento futuro para uma avaliação honesta...")
    features_com_conhecimento_futuro = [
        'temperatura_rj',
        'evento_black_friday',
        'evento_vespera_natal',
        'semana_natal'
    ]
    X = X.drop(columns=features_com_conhecimento_futuro, errors='ignore')

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, shuffle=False, random_state=config.RANDOM_STATE
    )
    
    print("\nTreinando Modelo de Tendência (Regressão Linear)...")
    model_lr = LinearRegression()
    model_lr.fit(X_train, y_train)
    
    y_pred_lr = model_lr.predict(X_test)
    avaliar(y_test, y_pred_lr, "Apenas Tendência (Regressão Linear)")
    
    print("\nTreinando Modelo de Resíduos (Random Forest)...")
    previsao_tendencia_treino = model_lr.predict(X_train)
    residuos_treino = y_train - previsao_tendencia_treino
    
    model_rf_residuos = RandomForestRegressor(
        n_estimators=config.RF_ESTIMATORS, 
        random_state=config.RANDOM_STATE
    )
    model_rf_residuos.fit(X_train, residuos_treino)

    print("\nGerando previsão final com o Modelo Híbrido...")
    previsao_tendencia_teste = model_lr.predict(X_test)
    previsao_residuos_teste = model_rf_residuos.predict(X_test)
    previsao_final_hibrida = previsao_tendencia_teste + previsao_residuos_teste
    
    avaliar(y_test, previsao_final_hibrida, "Modelo Híbrido (LR + RF) - Sem 'Cola'")

    print("\nSalvando modelos treinados...")
    joblib.dump(model_lr, config.MODEL_LR_PATH)
    joblib.dump(model_rf_residuos, config.MODEL_RF_PATH)

    print(f"✅ Modelos salvos na pasta: '{config.MODELS_PATH}'")

if __name__ == "__main__":
    main()