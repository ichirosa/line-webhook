import yfinance as yf
import pandas as pd

symbol = "8316.T"
df = yf.download(symbol, start="2023-01-01", interval="1d")
df = df[["Close"]].dropna().reset_index()
print(df.tail())# MACD計算
df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()
df["MACD"] = df["EMA12"] - df["EMA26"]
df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
df["Histogram"] = df["MACD"] - df["Signal"]

# ヒストグラムの符号変化を検出
df["Sign"] = df["Histogram"].apply(lambda x: 1 if x > 0 else -1)
df["Divergence"] = df["Sign"].diff()

# 変化があった行だけ抽出
alerts = df[df["Divergence"] != 0]
print(alerts[["Date", "Close", "MACD", "Signal", "Histogram", "Divergence"]].tail())