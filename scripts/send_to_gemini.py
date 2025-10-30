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
        model = "models/gemini-2.5-pro"

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

        prompt = "You are a strict code validator. Analyze the following code and decide if it contains a definite," \
        "guaranteed error that would prevent it from running or working as intended (syntax errors, runtime errors, " \
        "invalid imports, or logical flaws that always cause failure). Ignore hypothetical issues, environment assumptions, " \
        "missing API keys, or best-practice concerns. Respond with ONE WORD only: - ERROR → if there is a definite, unavoidable problem." \
        " - OK → if the code can run successfully as-is. Code:"

        # שלח ל-Gemini
        response = client.models.generate_content(
            model=model,
            contents=f"{prompt}\n{file_content}"
        )

        # הדפס את התשובה
        print("✅ Gemini response:\n")
        print(response.text)

    except Exception as e:
        print(f"❌ Error communicating with Gemini: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
