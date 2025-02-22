from flask import Flask, request
import requests

app = Flask(__name__)

# 🆔 แมป DEVICE_ID กับ Telegram Chat ID
DEVICE_MAPPING = {
    "device_A": "-4748941264",  # เครื่อง A → กลุ่ม A
    "device_B": "-100444555666",  # เครื่อง B → กลุ่ม B
}

TOKEN = "8134810874:AAEClDIW1U90KpjssRYCG0IypWrSdYmWyPA"


@app.route("/sms", methods=["POST"])
def sms_webhook():
    data = request.json
    text = data.get("text")
    device_id = request.headers.get("DEVICE_ID")  # ดึงค่า DEVICE_ID

    # ตรวจสอบว่า DEVICE_ID ต้องส่งไปกลุ่มไหน
    chat_id = DEVICE_MAPPING.get(device_id)

    if not chat_id:
        return {"status": "error", "message": "Unknown Device"}, 400

    # ส่งข้อความไป Telegram
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(telegram_url, json={"chat_id": chat_id, "text": f"📩 SMS: {text}"})

    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
