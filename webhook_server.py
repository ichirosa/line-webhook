from flask import Flask, request
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/callback', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "Callback endpoint is alive", 200
    print("=== /callback エンドポイントにPOSTリクエストを受信 ===")
    try:
        print("Headers:", dict(request.headers))
        print("Body:", request.get_data(as_text=True))
    except Exception as e:
        print("⚠️ リクエスト処理中に例外:", e)
    return "OK", 200

@app.route('/', methods=['GET'])
def root():
    return "Flask is running", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)