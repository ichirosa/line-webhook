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
print(alerts[["Date", "Close", "MACD", "Signal", "Histogram", "Divergence"]].tail())import requests

# LINE Messaging APIのチャネルアクセストークン（取得したものに置き換えてください）
token = "ここにあなたのチャネルアクセストークンを貼り付け"

# 通知メッセージの生成（最新の乖離変化を1件だけ通知）
if not alerts.empty:
    latest = alerts.iloc[-1]
    message = f"""📈 MACD乖離変化通知
日付: {latest['Date'].date()}
終値: {latest['Close']}
MACD: {latest['MACD']:.2f}
Signal: {latest['Signal']:.2f}
Histogram: {latest['Histogram']:.2f}
乖離変化: {latest['Divergence']}"""

    # LINE Messaging APIへ送信
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "to": "ここにあなたのユーザーIDを貼り付け",
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(url, headers=headers, json=payload)
    print("通知送信結果:", response.status_code, response.text)