import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import numpy as np

# Carregar features
df = pd.read_excel("../data/features.xlsx")

# Remover linhas com NaN
df = df.dropna()

# Definir X (features) e y (target)
X = df.drop(columns=["value"], errors="ignore")
y = df["value"]

# Remover coluna 'date' caso ainda exista
if "date" in X.columns:
    X = X.drop(columns=["date"])

# Separar em treino e teste (sem embaralhar)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# 3. Treinar modelos
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)

model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf.fit(X_train, y_train)

# 4. Avaliação
def avaliar(modelo, nome):
    y_pred = modelo.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"🔹 {nome}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print("-" * 30)

avaliar(model_lr, "Regressão Linear")
avaliar(model_rf, "Random Forest")

# 5. Salvar modelos treinados
joblib.dump(model_lr, "../models/model_linear.pkl")
joblib.dump(model_rf, "../models/model_rf.pkl")

print("✅ Modelos salvos em '../models/'")
