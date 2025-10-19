import time
import csv
from datetime import datetime
from datetime import date # ① 日付操作のためにdateモジュールを追加
import os
import subprocess

# ログファイル名
# ② ファイル名を日付とユーザー名を含む形式に変更
LOG_FILE_BASE_PATH = f"/Users/ichirosa/Desktop/{date.today().strftime('%Y-%m-%d')}_usage_log.csv"
INTERVAL_SECONDS = 10 # ログを取得する間隔（10秒）

def get_active_app_title_mac():
    """AppleScriptを使用して最前面のアプリケーション名とウィンドウタイトルを取得する関数 (Mac用)"""
    try:
        # AppleScriptのコード: 最前面のアプリ名とそのウィンドウタイトルを取得する
        script = """
        tell application "System Events"
            set frontApp to name of first process whose frontmost is true
        end tell
        
        try
            tell application frontApp
                set windowTitle to name of front window
            end tell
            return frontApp & " - " & windowTitle
        on error
            return frontApp & " - (No window title)"
        end try
        """
        
        # osascriptコマンドでAppleScriptを実行
        result = subprocess.check_output(['osascript', '-e', script], text=True, encoding='utf-8').strip()
        return result
        
    except Exception as e:
        return f"Error: {e}"

def write_log(timestamp, app_name):
    """取得したログをCSVファイルに書き込む関数"""
    try:
        # ③ 毎回ファイルパスを計算することで、日付が変わっても自動で新しいファイルに切り替わる
        current_log_file = f"/Users/ichirosa/Desktop/{date.today().strftime('%Y-%m-%d')}_usage_log.csv"
        
        is_new_file = not os.path.exists(current_log_file) or os.path.getsize(current_log_file) == 0
        
        with open(current_log_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            if is_new_file:
                writer.writerow(["Timestamp", "Active Application and Title"])

            writer.writerow([timestamp, app_name])
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    # 実行時のファイルパスを表示するために、メイン関数内でパスを再計算
    current_log_file = f"/Users/ichirosa/Desktop/{date.today().strftime('%Y-%m-%d')}_usage_log.csv"

    print("-------------------------------------------------")
    print(f"PC利用ログの記録を開始しました。ログファイル: {current_log_file}") # ④ 表示されるファイル名も修正
    print("記録を停止するには、この画面で Ctrlキー + Cキー を同時に押してください。")
    print("-------------------------------------------------")
    
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        active_app_title = get_active_app_title_mac() 
        write_log(now, active_app_title)
        print(f"[{now}] 記録: {active_app_title}")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n--- 記録を停止しました。 ---")