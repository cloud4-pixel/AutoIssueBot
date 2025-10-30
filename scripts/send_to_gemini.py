import os
from google import genai

def main():
    # קרא את מפתח ה־API מהסביבה
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY environment variable")

    # צור לקוח Gemini
    client = genai.Client(api_key=api_key)

    # בחר את המודל
    model = "gemini-1.5-pro"

    # קרא את תוכן הקובץ
    with open("app.py", "r", encoding="utf-8") as f:
        file_content = f.read()

    # שלח ל-Gemini
    response = client.models.generate_content(
        model=model,
        contents=f"Analyze this text file:\n{file_content}"
    )

    # הדפס את התשובה
    print(response.text)

if __name__ == "__main__":
    main()
