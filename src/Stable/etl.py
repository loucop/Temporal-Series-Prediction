import pandas as pd

def carregar_dados(caminho_arquivo):
    """Carrega os dados brutos de XLSX"""
    df = pd.read_excel(caminho_arquivo)
    return df

def limpar_dados(df):
    """Limpa valores nulos e duplicados"""
    df = df.drop_duplicates()
    df = df.dropna()
    return df

def transformar_dados(df, coluna_data, coluna_valor):
    """Transforma a coluna de data em datetime e ordena"""
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    df = df.sort_values(by=coluna_data)
    df = df[[coluna_data, coluna_valor]]
    df = df.reset_index(drop=True)
    return df

def salvar_dados(df, caminho_saida):
    """Salva dados processados em CSV"""
    df.to_csv(caminho_saida, index=False)
    print(f"Dados processados salvos em: {caminho_saida}")

if __name__ == "__main__":
    caminho_entrada = "../data/raw.xlsx"     # agora é XLSX
    caminho_saida = "../data/processed.xlsx" # vamos salvar também em XLSX
    coluna_data = "date"
    coluna_valor = "value"

    df = carregar_dados(caminho_entrada)
    print("Colunas do XLSX:", df.columns)
    df = limpar_dados(df)
    df = transformar_dados(df, coluna_data, coluna_valor)
    df.to_excel(caminho_saida, index=False)
    print(f"Dados processados salvos em: {caminho_saida}")

