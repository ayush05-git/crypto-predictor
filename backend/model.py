import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor

def get_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "60"}
    data = requests.get(url, params=params).json()
    prices = [p[1] for p in data["prices"]]
    return np.array(prices)

def train():
    prices = get_data()
    scaler = MinMaxScaler()
    prices_scaled = scaler.fit_transform(prices.reshape(-1, 1)).flatten()

    X, y = [], []
    window = 5
    for i in range(len(prices_scaled) - window):
        X.append(prices_scaled[i:i + window])
        y.append(prices_scaled[i + window])

    X = np.array(X)
    y = np.array(y)

    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
    model.fit(X, y)

    return model, scaler, prices_scaled

def predict():
    model, scaler, prices_scaled = train()
    last = list(prices_scaled[-5:])
    preds = []

    for _ in range(7):
        x = np.array(last[-5:]).reshape(1, -1)
        p = model.predict(x)[0]
        preds.append(float(scaler.inverse_transform([[p]])[0][0]))
        last.append(p)

    return preds
