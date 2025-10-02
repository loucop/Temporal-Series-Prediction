# main.py (substitui o pipeline.py)

import os
import etl
import features
import train
import plot_results

def main():
    """
    Orquestra a execução de todo o pipeline de machine learning,
    chamando cada etapa na sequência correta.
    """
    print("================================================")
    print("🚀 INICIANDO PIPELINE DE PREVISÃO DE SÉRIES TEMPORAIS 🚀")
    print("================================================")
    
    # Garante que os diretórios de saída existam antes de rodar
    os.makedirs("../data", exist_ok=True)
    os.makedirs("../models", exist_ok=True)
    os.makedirs("../reports", exist_ok=True)
    
    try:
        # Etapa 1: Extração, Transformação e Carga
        etl.main()
        
        # Etapa 2: Criação de Features
        features.main()
        
        # Etapa 3: Treinamento e Avaliação de Modelos
        train.main()
        
        # Etapa 4: Visualização de Resultados
        plot_results.main()
        
        print("\n================================================")
        print("✅ PIPELINE CONCLUÍDO COM SUCESSO! ✅")
        print("================================================")
        
    except Exception as e:
        print("\n================================================")
        print(f"❌ ERRO: O pipeline falhou na execução.")
        print(f"Detalhe do erro: {e}")
        print("================================================")

if __name__ == "__main__":
    main()