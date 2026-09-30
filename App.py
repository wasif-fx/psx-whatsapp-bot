
from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# === CONFIG - YAHAN APNI VALUES DALO ===
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "EAAVwYmVQC5cBSuvF05ZC2EAb8UX6AV85CaginFpXV... YAHAN PURA TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "1294935970376093")
VERIFY_TOKEN = "psxbot123"

# === PSX DATA LOGIC ===
def get_psx_report():
    # TODO: Yahan real PSX data API lagao
    # Abhi sample report hai, kal se real data se connect kar denge
    
    today = datetime.now().strftime("%d %B %Y")
    
    report = f"""📊 *PSX ONE-SHOT REPORT* - {today}

🔥 *VOLUME SPIKE (Kal se 2x):*
• OGDC - 2.8x (4.2M vs 1.5M)
• PPL - 2.3x (3.1M vs 1.3M)
• PSO - 2.1x (2.8M)

🚀 *BREAKOUT (20-Day High Break):*
• LUCK - 755 pe close - 20 din ka high tod diya
• OGDC - 136.5 pe close - Resistance break

🔻 *NEECHE / WEAK:*
• TRG - -3.2% (Support toda)
• UNITY - -2.1%

📍 *S/R LEVELS (Kal ke liye Important):*
• OGDC: Support 133.5 | Resistance 138.0
• PPL: Support 87.0 | Resistance 92.0
• LUCK: Support 740 | Resistance 760
• PSO: Support 162 | Resistance 168

💡 *Breakout ka matlab: Aj ka close pichle 20 din ke high se upar*
⚠️ _Ye sirf data hai, khareedne/bechne ka mashwara nahi._

Next report ke liye likho: *aj ka market*"""

    return report

def send_whatsapp(to_number, message):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    resp = requests.post(url, headers=headers, json=data)
    print("WhatsApp API Response:", resp.text)
    return resp

# Verification for Meta
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

# Incoming messages
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Incoming:", data)
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg = entry['messages'][0]
            from_number = msg['from']
            user_text = msg.get('text', {}).get('body', '').lower()

            # Roman Urdu keywords
            keywords = ["aj", "market", "volume", "breakout", "s/r", "sr", "batao", "report", "psx"]
            if any(k in user_text for k in keywords):
                report = get_psx_report()
                send_whatsapp(from_number, report)
            else:
                send_whatsapp(from_number, "Salam! 👋\n' *aj ka market batao* ' likho, me pura volume + breakout + S/R report bhej dunga 📊")
    except Exception as e:
        print(f"Error: {e}")

    return "OK", 200

@app.route("/")
def home():
    return "PSX WhatsApp Bot is Running ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
