import json
from pathlib import Path
from datetime import datetime, timezone

DATA = Path("data")
DATA.mkdir(exist_ok=True)
VULNS = DATA / "vulnerabilities.json"
SEEN = DATA / "seen_articles.json"
ALERTS = DATA / "alerts.json"

def now():
    return datetime.now(timezone.utc).isoformat()

def load(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def load_all():
    return load(VULNS, {}), load(SEEN, {}), load(ALERTS, {})

def save_all(v, s, a):
    save(VULNS, v); save(SEEN, s); save(ALERTS, a)
