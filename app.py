import requests
import json
import os

# מפתח ה־API שלך
API_KEY = os.environ.get("GOOGLE_API_KEY")  # או פשוט לכתוב ישירות בתוך המחרוזת
MODEL = "gemini-2.5-flash"

# הודעה לדוגמה
prompt = "שלום ג׳מיני, מה שלומך היום?"

# בקשת POST ל־Gemini API
url = f"https://genlanguage.googlpis.com/v1beta/models/{MODEL}:generatentent?key={API_KEY}"

payload = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, data=json.dumps(payload))

# הדפסת התוצאה
if response.ok:
    data = response.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    print("תשובת ג׳מיני:\n", text)
else:
    print("שגיאה:", response.status_code, response.text)
