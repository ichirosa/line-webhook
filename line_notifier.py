import os
import requests
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# 環境変数の取得
USER_ID = os.getenv("USER_ID")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def send_line_message(message):
    if not USER_ID or not LINE_CHANNEL_ACCESS_TOKEN:
        print("❌ 環境変数が未設定です。LINE通知を送信できません。")
        return

    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message}]
    }

    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)

    if response.status_code == 200:
        print(f"✅ LINE通知送信成功: {message}")
    else:
        print(f"❌ LINE通知失敗: {response.status_code} - {response.text}")