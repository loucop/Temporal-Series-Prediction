# utils.py

import pandas as pd
import config

def carregar_dados_de_features(caminho_arquivo: str) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Carrega o dataset de features, que já foi limpo de NaNs.
    Separa e retorna as features (X), o alvo (y) e a série de datas.
    """
    df = pd.read_excel(caminho_arquivo)
    
    # Garante que a coluna de data esteja no formato correto
    df[config.DATE_COLUMN] = pd.to_datetime(df[config.DATE_COLUMN])
    
    # O alvo (y) é a coluna definida no config
    y = df[config.TARGET_COLUMN]
    
    # As features (X) são todas as colunas, exceto o alvo e a data
    X = df.drop(columns=[config.TARGET_COLUMN, config.DATE_COLUMN], errors='ignore')
    
    # As datas são retornadas para uso futuro (ex: plots)
    dates = df[config.DATE_COLUMN]
    
    return X, y, dates