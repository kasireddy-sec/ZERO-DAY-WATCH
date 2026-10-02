import json
from pathlib import Path
from datetime import datetime, timezone

p = Path("data/vulnerabilities.json")
v = json.loads(p.read_text()) if p.exists() else {}
out = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "total_zero_day_records": len(v),
    "high_confidence": sum(1 for x in v.values() if float(x.get("Confidence",0)) >= .8),
    "active_exploitation": sum(1 for x in v.values() if x.get("Exploitation") in {"confirmed","reported"}),
    "records": list(v.values())
}
Path("data/daily_digest.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
