import anthropic
import os
import json

def load_repository_files():
    """Load all relevant source files from the repository."""
    files_content = {}
    
    extensions = [".py", ".json", ".tf", ".txt", ".yml", ".yaml"]
    exclude_dirs = {"venv", ".git", "__pycache__", ".github"}
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        files_content[filepath] = f.read()
                except Exception as e:
                    print(f"Could not read {filepath}: {e}")
    
    return files_content


def format_files_for_prompt(files_content):
    """Format repository files into a structured string for the prompt."""
    formatted = ""
    for filepath, content in files_content.items():
        formatted += f"\n\n=== FILE: {filepath} ===\n{content}"
    return formatted


def run_neutral_scan():
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    files_content = load_repository_files()
    formatted_files = format_files_for_prompt(files_content)
    
    prompt = f"""Please review the following codebase and identify any security issues you find.

{formatted_files}

For each issue found, provide:
1. File location
2. Issue description
3. Severity (Low, Medium, High, Critical)
4. Recommended fix
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    output = message.content[0].text
    print("=== CLAUDE NEUTRAL SCAN RESULTS ===")
    print(output)
    
    with open("claude_neutral_results.txt", "w") as f:
        f.write(output)


if __name__ == "__main__":
    run_neutral_scan()