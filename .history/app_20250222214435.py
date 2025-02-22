from flask import Flask, request
import requests

app = Flask(__name__)

# 🔥 ตั้งค่าข้อมูล Telegram Bot Token และ Chat ID แยกตามเครื่อง
DEVICE_CONFIG = {
    "A": {
        "TOKEN": "8134810874:AAEClDIW1U90KpjssRYCG0IypWrSdYmWyPA",
        "CHAT_ID": "-4748941264",
    },
    "B": {"TOKEN": "TELEGRAM_BOT_TOKEN_B", "CHAT_ID": "TELEGRAM_CHAT_ID_B"},
    "C": {"TOKEN": "TELEGRAM_BOT_TOKEN_C", "CHAT_ID": "TELEGRAM_CHAT_ID_C"},
}


def send_to_telegram(device, message):
    """ส่งข้อความไปยัง Telegram ตามเครื่องที่กำหนด"""
    if device in DEVICE_CONFIG:
        TOKEN = DEVICE_CONFIG[device]["TOKEN"]
        CHAT_ID = DEVICE_CONFIG[device]["CHAT_ID"]

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, json=payload)


@app.route("/sms-forward/<device>", methods=["POST"])
def receive_sms(device):
    """รับ Webhook SMS และส่งไปยังกลุ่ม Telegram ตามเครื่อง"""
    data = request.json
    sender = data.get("from", "Unknown")
    text = data.get("text", "")

    message = f"📩 SMS จาก {sender}:\n{text}"

    # 🔥 ส่งข้อความไปยัง Telegram ตามเครื่องที่กำหนด
    if device in DEVICE_CONFIG:
        send_to_telegram(device, message)
        return {"status": "ok", "device": device}, 200
    else:
        return {"status": "error", "message": "Invalid device"}, 400


if __name__ == "__main__":
    app.run(port=5000)
