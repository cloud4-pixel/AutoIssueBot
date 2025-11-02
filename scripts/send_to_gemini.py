import os
import sys
from google import genai

def get_all_code_files(directory, extensions=(".py", ".js", ".ts", ".java", ".go", ".rb")):
    """אסוף את כל קבצי הקוד מהתיקייה והצאצאים שלה"""
    files = []
    for root, _, filenames in os.walk(directory):
        for name in filenames:
            if name.endswith(extensions):
                files.append(os.path.join(root, name))
    return files

def main():
    if len(sys.argv) < 2:
        print("❌ נא לציין נתיב לתיקייה לבדיקה", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"❌ נתיב לא תקין: {directory}", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ חסר GOOGLE_API_KEY", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    model = "models/gemini-2.5-pro"
    github_output = os.environ.get("GITHUB_OUTPUT")

    all_files = get_all_code_files(directory)
    print(f"🔍 Found {len(all_files)} code files in {directory}")

    if not all_files:
        print("⚠️ No code files found.")
        return

    with open(github_output, "a") as gh_out:
        for file_path in all_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()

                prompt = (
                    "You are a strict but concise code validator. Analyze the following code carefully.\n\n"
                    "If the code contains a definite error that would prevent it from running or working as intended, "
                    "respond with a **short, plain-English explanation** (max 2 short sentences). "
                    "Focus only on real syntax or logic errors. If there is **no clear error**, respond only with: NO.\n\n"
                    "Code:\n"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=f"{prompt}\n{code}"
                )

                result = response.text.strip()
                print(f"✅ [{file_path}] Gemini response: {result}")

                # כתיבה לפלט (שם הקובץ = תוצאה)
                gh_out.write(f"{file_path}={result}\n")

            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
