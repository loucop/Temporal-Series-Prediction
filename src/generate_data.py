# generate_data.py (Versão Finalíssima - Salvando na pasta correta)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

print("--- Gerando dataset final com simulação honesta ---")

# --- 1. Parâmetros da Simulação ---
datas = pd.date_range(start="2022-01-01", periods=3*365, freq="D")
n_periodos = len(datas)

# --- 2. Componentes PREVISÍVEIS da Série ---
tendencia_linear = np.arange(100, 100 + 0.5 * n_periodos, 0.5)
tendencia_log = np.log1p(np.arange(n_periodos)) * 20
tendencia = tendencia_linear + tendencia_log
sazonalidade_anual = 15 * -np.cos(np.arange(n_periodos) * (2 * np.pi / 365.25))
dias_da_semana = datas.dayofweek
pesos_dia_semana = {0:-8, 1:-5, 2:-2, 3:0, 4:10, 5:25, 6:5}
sazonalidade_semanal = np.array([pesos_dia_semana[dia] for dia in dias_da_semana])
sazonalidade = sazonalidade_anual + sazonalidade_semanal

# --- 3. Criação da Base Previsível e DataFrame Inicial ---
valor_previsivel = tendencia + sazonalidade
df = pd.DataFrame({
    "date": datas,
    "value_base": valor_previsivel
})

# --- 4. Criação de Features a partir da Base Previsível ---
for ano in df['date'].dt.year.unique():
    bf_date = df[(df['date'].dt.month == 11) & (df['date'].dt.dayofweek == 4) & (df['date'].dt.year == ano)]['date'].max()
    if pd.notna(bf_date):
        df.loc[df['date'] == bf_date - pd.Timedelta(days=2), 'value_base'] *= 0.8
        df.loc[df['date'] == bf_date - pd.Timedelta(days=1), 'value_base'] *= 0.7
        df.loc[df['date'] == bf_date, 'value_base'] *= 1.9
        df.loc[df['date'] == bf_date + pd.Timedelta(days=1), 'value_base'] *= 0.85

# --- 5. Adição dos Componentes IMPREVISÍVEIS ---
volatilidade = np.where(pd.Series(dias_da_semana).isin([5, 6]), 12, 5)
ruido = np.random.normal(0, volatilidade)
choques = np.zeros(n_periodos)
n_choques = 15
indices_choques = np.random.choice(np.arange(n_periodos), n_choques, replace=False)
for idx in indices_choques:
    choques[idx] = np.random.uniform(-100, 150)

# --- 6. Criação da Coluna de Valor Final e Limpeza ---
df['value'] = df['value_base'] + ruido + choques
df.drop(columns=['value_base'], inplace=True)
indices_para_remover = df.sample(frac=0.01).index
df.loc[indices_para_remover, 'value'] = np.nan

# =============================================================================
# --- 7. Salvar e Visualizar (COM A MUDANÇA) ---
# =============================================================================
# Define o diretório de saída (um nível acima, na pasta 'data')
output_dir = "../data"
# Garante que o diretório de saída exista; se não, ele o cria
os.makedirs(output_dir, exist_ok=True)

# Define o caminho completo do arquivo
caminho_saida = os.path.join(output_dir, "raw.xlsx") 

# Salva o arquivo no caminho correto
df.to_excel(caminho_saida, index=False)
print(f"✅ Arquivo '{caminho_saida}' criado com sucesso!")
# =============================================================================

# Visualização
plt.figure(figsize=(18, 8))
plt.plot(df['date'], df['value'], marker='.', linestyle='-', markersize=2)
plt.title("Série Temporal Sintética - Versão Final (Simulação Honesta)")
plt.xlabel("Data")
plt.ylabel("Valor")
plt.grid(True)
plt.show()