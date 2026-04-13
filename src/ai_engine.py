import os
import json

# load .env from root folder explicitly
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from google import genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file at project root.")

client = genai.Client(api_key=api_key)
SYSTEM_PROMPT = """You are a senior Varroc automotive design engineer specialising in 
DFM (Design for Manufacturability). Respond ONLY with valid JSON. 
No markdown, no preamble, no code fences."""


def enrich_issues_with_ai(issues: list[dict]) -> list[dict]:
    if not issues:
        return issues

    prompt = f"""{SYSTEM_PROMPT}

These DFM issues were found in a CAD part.
For each issue, add a field "ai_suggestion" with a 2-sentence expert fix recommendation.
Return the same JSON array with ai_suggestion added to each object.

Issues:
{json.dumps(issues, indent=2)}"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        raw = response.text.strip()

        # strip code fences if Gemini adds them
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw.strip())

    except Exception as e:
        print(f"Gemini enrich error: {e}")
        for issue in issues:
            issue["ai_suggestion"] = f"Manual review required. Rule {issue['rule_id']} violated."
        return issues


def generate_summary(issues: list[dict], filename: str) -> str:
    critical = sum(1 for i in issues if i["severity"] == "critical")
    major    = sum(1 for i in issues if i["severity"] == "major")
    minor    = sum(1 for i in issues if i["severity"] == "minor")

    prompt = f"""You are a senior design engineer writing a formal validation report.

CAD part '{filename}' validation results:
- {critical} critical, {major} major, {minor} minor issues
- Top issues: {json.dumps([i['description'] for i in issues[:4]], indent=2)}

Write a 3-sentence executive summary. State compliance status first. Be direct."""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini summary error: {e}")
        return (
            f"Validation complete for '{filename}'. "
            f"Found {critical} critical, {major} major, and {minor} minor issues. "
            f"Immediate review recommended before proceeding to manufacturing."
        )