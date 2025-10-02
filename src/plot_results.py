# plot_results.py (Versão Híbrida - CORRIGIDO)

import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
import config
from utils import carregar_dados_de_features

def main():
    print("\n--- Iniciando processo de visualização de resultados (ESTRATÉGIA HÍBRIDA) ---")

    X, y, dates = carregar_dados_de_features(config.FEATURES_DATA_PATH)
    
    # =============================================================================
    # CORREÇÃO CRUCIAL: REPLICANDO A REMOÇÃO DAS FEATURES DO FUTURO
    # =============================================================================
    print("Removendo features com conhecimento futuro para consistência com o treino...")
    features_com_conhecimento_futuro = [
        'temperatura_rj', 
        'evento_black_friday', 
        'evento_vespera_natal', 
        'semana_natal'
    ]
    X = X.drop(columns=features_com_conhecimento_futuro, errors='ignore')
    # =============================================================================

    # Agora, o X usado aqui é idêntico ao X usado no train.py
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, shuffle=False, random_state=config.RANDOM_STATE
    )
    
    train_dates = dates.iloc[:len(y_train)]
    test_dates = dates.iloc[len(y_train):]
    
    print("Carregando modelos salvos...")
    model_lr = joblib.load(config.MODEL_LR_PATH)
    model_rf_residuos = joblib.load(config.MODEL_RF_PATH)

    print("Gerando previsões no conjunto de teste...")
    previsao_tendencia_teste = model_lr.predict(X_test)
    previsao_residuos_teste = model_rf_residuos.predict(X_test)
    previsao_final_hibrida = previsao_tendencia_teste + previsao_residuos_teste

    print("Gerando gráfico de resultados...")
    plt.figure(figsize=(18, 8))
    
    plt.plot(train_dates, y_train, label="Dados de Treino (Real)", color='gray')
    plt.plot(test_dates, y_test, label="Dados de Teste (Real)", color='blue', marker='o', markersize=4)
    plt.plot(test_dates, previsao_tendencia_teste, label="Previsão da Tendência (Linear)", color='orange', linestyle=':')
    plt.plot(test_dates, previsao_final_hibrida, label="Previsão Híbrida (LR + RF)", color='green', linestyle='--')

    plt.title("Previsão Híbrida em Dados de Teste vs Valores Reais (Simulação Honesta)")
    plt.xlabel("Data")
    plt.ylabel("Valor")
    plt.legend()
    plt.grid(True)
    
    caminho_grafico = "../reports/previsoes_hibrido_honesto.png"
    plt.savefig(caminho_grafico)
    print(f"✅ Gráfico salvo em: {caminho_grafico}")
    plt.show()

if __name__ == "__main__":
    main()