import os
import sys
from google import genai

def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Missing GOOGLE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    try:
        client = genai.Client(api_key=api_key)
        model = "models/gemini-2.5-pro"

        file_path = "app.py"
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}", file=sys.stderr)
            sys.exit(1)

        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        prompt = (
            "You are a strict but concise code validator. Analyze the following code carefully.\n\n"
            "If the code contains a definite error that would prevent it from running or working as intended, "
            "respond with a **short, plain-English explanation** of the issue (max 2 short sentences). "
            "Focus only on real syntax or logic errors — ignore missing API keys, environment setup, or best practices.\n\n"
            "If there is **no clear error**, respond with just the word: **NO**.\n\n"
            "Format your response to be suitable for inclusion in a GitHub Issue body (plain text, no markdown code blocks).\n\n"
            "Code:\n"
        )


        response = client.models.generate_content(
            model=model,
            contents=f"{prompt}\n{file_content}"
        )

        result = response.text.strip()
        print(f"✅ Gemini response: {result}")

        # החלק החשוב 👇 — כתיבה ל־GITHUB_OUTPUT
        github_output = os.environ.get("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"gemini_result={result}\n")

    except Exception as e:
        print(f"❌ Error communicating with Gemini: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
