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


def run_security_aware_scan():
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    files_content = load_repository_files()
    formatted_files = format_files_for_prompt(files_content)
    
    prompt = f"""You are a security expert conducting a thorough security audit of a codebase. 
Your task is to identify security vulnerabilities based on the OWASP Top 10 framework and 
Common Weakness Enumeration (CWE) categories.

Specifically look for:
1. Injection vulnerabilities (SQL injection, command injection, template injection) - OWASP A03
2. Exposed secrets, hardcoded credentials, and API keys - OWASP A02
3. Outdated dependencies with known CVEs - OWASP A06
4. Security misconfigurations in infrastructure-as-code - OWASP A05
5. Overly permissive IAM policies and access controls - OWASP A01

{formatted_files}

For each vulnerability found, provide:
1. File location and line reference where possible
2. Vulnerability type and relevant CWE or OWASP category
3. Severity (Low, Medium, High, Critical)
4. Technical explanation of why this is a vulnerability
5. Specific remediation steps for this exact instance
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
    print("=== CLAUDE SECURITY-AWARE SCAN RESULTS ===")
    print(output)
    
    with open("claude_security_aware_results.txt", "w") as f:
        f.write(output)


if __name__ == "__main__":
    run_security_aware_scan()