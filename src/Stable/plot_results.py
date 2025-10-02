import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Carregar features
df = pd.read_excel("../data/features.xlsx")

# Remover linhas com NaN (de lags e médias móveis)
df = df.dropna()

# Separar X e y
X = df.drop(columns=["value", "date"], errors="ignore")
y = df["value"]

# Carregar modelos
model_lr = joblib.load("../models/model_linear.pkl")
model_rf = joblib.load("../models/model_rf.pkl")

# Fazer previsões
y_pred_lr = model_lr.predict(X)
y_pred_rf = model_rf.predict(X)

# Plotar
plt.figure(figsize=(12,6))
plt.plot(df["date"], y, label="Real", marker='o')
plt.plot(df["date"], y_pred_lr, label="Linear Regression", linestyle='--', marker='x')
plt.plot(df["date"], y_pred_rf, label="Random Forest", linestyle='--', marker='s')
plt.xlabel("Data")
plt.ylabel("Valor")
plt.title("Previsões vs Valores Reais")
plt.legend()
plt.grid(True)
plt.show()
