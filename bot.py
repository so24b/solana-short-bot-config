import requests
import json
import time

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def update_config_from_github(config):
    url = config.get("github_config_url")
    if url:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    f.write(r.text)
                print("[+] Config updated from GitHub")
        except Exception as e:
            print("[-] Failed to update config:", e)

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("[-] Telegram error:", e)

def main():
    while True:
        config = load_config()
        update_config_from_github(config)

        token = config["telegram_bot_token"]
        chat_id = config["telegram_chat_id"]
        tag = config["telegram_tag"]

        # شبیه‌سازی بررسی شرایط (اینجا بعدا الگوریتم اضافه میشه)
        message = f"📈 New signal detected! {tag}\nToken: TEST\nTarget: +20%\nStopLoss: -10%"
        send_telegram_message(token, chat_id, message)

        time.sleep(60)  # هر ۱ دقیقه یک بار

if __name__ == "__main__":
    main()
