import pandas as pd

def carregar_dados(caminho_arquivo):
    """Carrega dados processados do XLSX"""
    df = pd.read_excel(caminho_arquivo)
    return df

def criar_lags(df, coluna_valor, lags=[1,2,3]):
    """
    Cria colunas com valores passados da série temporal.
    Ex: lag 1 = valor do dia anterior
    """
    for lag in lags:
        df[f"{coluna_valor}_lag{lag}"] = df[coluna_valor].shift(lag)
    return df

def criar_medias_moveis(df, coluna_valor, janelas=[3,7]):
    """
    Cria médias móveis para capturar tendência da série.
    Ex: 3 dias = média dos últimos 3 dias
    """
    for janela in janelas:
        df[f"{coluna_valor}_ma{janela}"] = df[coluna_valor].rolling(window=janela).mean()
    return df

def preparar_dados_modelo(df, coluna_valor):
    """
    Remove linhas com valores nulos (devidos a lags e médias móveis)
    Separa X e y para treino
    """
    df = df.dropna()
    X = df.drop(columns=[coluna_valor, 'date'])
    y = df[coluna_valor]
    return X, y

if __name__ == "__main__":
    caminho_entrada = "../data/processed.xlsx"
    coluna_valor = "value"

    df = carregar_dados(caminho_entrada)
    df = criar_lags(df, coluna_valor, lags=[1,2,3])
    df = criar_medias_moveis(df, coluna_valor, janelas=[3,7])
    X, y = preparar_dados_modelo(df, coluna_valor)

    print("Features geradas:")
    print(X.head())
    print("\nTarget:")
    print(y.head())

    # Salvar as features com target em Excel
    df.to_excel("../data/features.xlsx", index=False)
    print("✅ Features salvas em: ../data/features.xlsx")
