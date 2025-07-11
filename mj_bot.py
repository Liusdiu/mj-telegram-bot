from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

MJ_PROMPT = """Tu es le Maître du Jeu d'une campagne de jeu de rôle sur Telegram. Tu décris le monde, les conséquences des actions des joueurs, tu incarnes les PNJ. Tu parles comme Cortana de Halo : calme, précise, légèrement ironique."""

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if text:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": MJ_PROMPT},
                {"role": "user", "content": text}
            ]
        )
        reply = response.choices[0].message["content"]
        send_message(chat_id, reply)

    return {"ok": True}
