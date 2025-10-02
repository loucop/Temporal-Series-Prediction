# features.py

import pandas as pd
import numpy as np
import config

def carregar_dados_processados(caminho_arquivo: str) -> pd.DataFrame:
    print(f"Carregando dados processados de: {caminho_arquivo}")
    df = pd.read_excel(caminho_arquivo)
    df[config.DATE_COLUMN] = pd.to_datetime(df[config.DATE_COLUMN])
    return df

# <<<--- ESTA FUNÇÃO ESTAVA FALTANDO ---<<<
def criar_features_de_lag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria colunas com valores passados (lags) da série temporal.
    Os lags a serem criados são definidos no arquivo config.
    """
    for lag in config.LAGS_TO_CREATE:
        df[f"{config.TARGET_COLUMN}_lag_{lag}"] = df[config.TARGET_COLUMN].shift(lag)
    return df

# <<<--- ESTA É A FUNÇÃO QUE CORRIGIMOS ANTERIORMENTE ---<<<
def criar_features_de_media_movel(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria médias móveis usando apenas dados passados para evitar data leakage.
    O .shift(1) garante que a média móvel para a data D use dados até D-1.
    """
    for janela in config.MA_WINDOWS_TO_CREATE:
        df[f"{config.TARGET_COLUMN}_ma_{janela}"] = df[config.TARGET_COLUMN].rolling(window=janela).mean().shift(1)
    return df

def criar_features_de_data(df: pd.DataFrame) -> pd.DataFrame:
    df['dia_da_semana'] = df[config.DATE_COLUMN].dt.dayofweek
    df['mes'] = df[config.DATE_COLUMN].dt.month
    df['semana_do_ano'] = df[config.DATE_COLUMN].dt.isocalendar().week.astype(int)
    return df

def criar_features_de_eventos(df: pd.DataFrame) -> pd.DataFrame:
    """Cria features binárias (0 ou 1) para eventos especiais."""
    # Como os dados agora são realistas, vamos remover os eventos hardcoded
    # para forçar o modelo a aprender com os padrões de data.
    # Se você tivesse uma lista real de feriados, a adicionaria aqui.
    return df

def main():
    print("\n--- Iniciando processo de criação de features ---")
    df_processed = carregar_dados_processados(config.PROCESSED_DATA_PATH)

    df_with_lags = criar_features_de_lag(df_processed)
    df_with_ma = criar_features_de_media_movel(df_with_lags)
    df_with_dates = criar_features_de_data(df_with_ma)
    df_with_events = criar_features_de_eventos(df_with_dates)

    # Remove as linhas com NaN
    df_with_events.dropna(inplace=True)

    # CRIA O TIME INDEX
    df_with_events.reset_index(drop=True, inplace=True)
    df_with_events['time_index'] = df_with_events.index

    df_with_events.to_excel(config.FEATURES_DATA_PATH, index=False)
    print(f"✅ Features criadas e salvas em: {config.FEATURES_DATA_PATH}")
    print("\nAmostra do DataFrame com as novas features:")
    print(df_with_events.head())

if __name__ == "__main__":
    main()