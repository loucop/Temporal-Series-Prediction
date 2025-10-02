# config.py

"""
Arquivo de configuração centralizado para o pipeline de machine learning.
"""

# --- Caminhos de Arquivos ---
RAW_DATA_PATH = "../data/raw.xlsx"
PROCESSED_DATA_PATH = "../data/processed.xlsx"
FEATURES_DATA_PATH = "../data/features.xlsx"
MODELS_PATH = "../models/"
MODEL_LR_PATH = f"{MODELS_PATH}model_linear.pkl"
MODEL_RF_PATH = f"{MODELS_PATH}model_rf.pkl"

# --- Colunas do DataFrame ---
DATE_COLUMN = "date"
TARGET_COLUMN = "value"
# Adicionando a coluna de temperatura para mantê-la se quisermos usá-la como feature
EXOGENOUS_FEATURES = ["temperatura_rj"]

# --- Parâmetros de Features ---
LAGS_TO_CREATE = [1, 2, 3, 7]
MA_WINDOWS_TO_CREATE = [3, 7, 14]

# --- Parâmetros de Treino ---
TEST_SIZE = 0.2
RANDOM_STATE = 42
RF_ESTIMATORS = 100