import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def get_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "60"}
    data = requests.get(url, params=params).json()
    prices = [p[1] for p in data["prices"]]
    return np.array(prices)

def train():
    prices = get_data()
    scaler = MinMaxScaler()
    prices = scaler.fit_transform(prices.reshape(-1, 1))
    X, y = [], []
    window = 5
    for i in range(len(prices) - window):
        X.append(prices[i:i+window])
        y.append(prices[i+window])
    X = np.array(X)
    y = np.array(y)
    model = Sequential()
    model.add(LSTM(50, input_shape=(window, 1)))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=5, batch_size=8)
    return model, scaler, prices

def predict():
    model, scaler, prices = train()
    last = prices[-5:]
    preds = []
    for _ in range(7):
        p = model.predict(last.reshape(1, 5, 1))
        preds.append(float(scaler.inverse_transform(p)[0][0]))
        last = np.append(last[1:], p).reshape(5, 1)
    return preds