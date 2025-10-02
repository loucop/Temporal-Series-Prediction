# etl.py

import pandas as pd
import config  # 1. Importamos nosso novo arquivo de configuração

def carregar_dados(caminho_arquivo: str) -> pd.DataFrame:
    """
    Carrega os dados brutos de um arquivo XLSX.
    Adiciona type hinting para clareza.
    """
    print(f"Carregando dados de: {caminho_arquivo}")
    return pd.read_excel(caminho_arquivo)

def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa valores nulos e duplicados de forma eficiente."""
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    return df

def transformar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Garante o tipo datetime na coluna de data, ordena, seleciona
    colunas relevantes e reseta o índice.
    """
    # Usa os nomes das colunas a partir do config
    df[config.DATE_COLUMN] = pd.to_datetime(df[config.DATE_COLUMN])
    df.sort_values(by=config.DATE_COLUMN, inplace=True)

    # Mantém apenas as colunas que usaremos nos próximos passos
    colunas_para_manter = [config.DATE_COLUMN, config.TARGET_COLUMN] + config.EXOGENOUS_FEATURES
    # Filtra para manter apenas as colunas que realmente existem no DataFrame
    colunas_existentes = [col for col in colunas_para_manter if col in df.columns]
    df = df[colunas_existentes]

    df.reset_index(drop=True, inplace=True)
    return df

def main():
    """
    Função principal que orquestra todo o processo de ETL.
    """
    print("--- Iniciando processo de ETL ---")

    # 2. Usa os caminhos e nomes de colunas do config
    df_raw = carregar_dados(config.RAW_DATA_PATH)
    
    print("Colunas originais:", df_raw.columns.tolist())
    
    df_clean = limpar_dados(df_raw)
    df_transformed = transformar_dados(df_clean)
    
    # 3. Salva os dados processados no caminho definido no config
    df_transformed.to_excel(config.PROCESSED_DATA_PATH, index=False)
    print(f"✅ Dados processados e salvos em: {config.PROCESSED_DATA_PATH}")

# Boa prática: garante que o código principal só rode quando o script é executado diretamente
if __name__ == "__main__":
    main()