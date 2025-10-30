import os
import sys
from google import genai

def main():
    # קרא את מפתח ה־API מהסביבה
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Missing GOOGLE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    try:
        # צור לקוח Gemini (API החדש)
        client = genai.Client(api_key=api_key)

        # בחר את המודל
        model = "gemini-1.5-pro"

        # בדוק שהמודל קיים
        available_models = [m.name for m in client.models.list()]
        if model not in available_models:
            print(f"⚠️  Model '{model}' not found. Available models:\n{available_models}", file=sys.stderr)
            sys.exit(1)

        # קרא את תוכן הקובץ
        file_path = "app.py"
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}", file=sys.stderr)
            sys.exit(1)

        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        # שלח ל-Gemini
        response = client.models.generate_content(
            model=model,
            contents=f"Analyze this text file:\n{file_content}"
        )

        # הדפס את התשובה
        print("✅ Gemini response:\n")
        print(response.text)

    except Exception as e:
        print(f"❌ Error communicating with Gemini: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
