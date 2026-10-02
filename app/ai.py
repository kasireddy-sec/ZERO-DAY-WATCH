import os, json, re, httpx
from app.models import Analysis

PROMPT = open("prompts/zero_day_analysis.txt", encoding="utf-8").read()

def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)

async def analyze(article):
    if os.getenv("AI_ENABLED","false").lower() != "true":
        return None
    base = os.getenv("AI_BASE_URL","").rstrip("/")
    key = os.getenv("AI_API_KEY","")
    model = os.getenv("AI_MODEL","")
    if not (base and key and model):
        return None

    user = PROMPT + "\n\nARTICLE TITLE:\n" + article.title + "\n\nARTICLE URL:\n" + article.url + \
           "\n\nARTICLE TEXT:\n" + article.text[:30000]
    payload = {
        "model": model,
        "messages": [
            {"role":"system","content":"Return JSON only."},
            {"role":"user","content":user}
        ],
        "temperature": 0
    }
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(base + "/chat/completions",
                         headers={"Authorization":f"Bearer {key}"},
                         json=payload)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        return Analysis.model_validate(extract_json(content))
