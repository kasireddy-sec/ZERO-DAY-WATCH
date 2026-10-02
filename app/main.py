import asyncio, yaml, os, re
from pathlib import Path
from datetime import datetime, timezone
from app.collectors import collect_source
from app.ai import analyze
from app.rules import qualifies_zero_day
from app.storage import load_all, save_all, now
from app.utils import internal_vuln_key, alert_key
from app.report import write_excel
from app.alerts import send_alert

def next_id(vulns):
    year = datetime.now(timezone.utc).year
    n = 1
    for k in vulns:
        m = re.search(r"ZD-\d{4}-(\d+)", k)
        if m: n = max(n, int(m.group(1))+1)
    return f"ZD-{year}-{n:05d}"

async def run(dry_run=False):
    cfg = yaml.safe_load(Path("config/sources.yaml").read_text())
    rules = yaml.safe_load(Path("config/rules.yaml").read_text())
    vulns, seen, alerts = load_all()
    candidates = []
    for src in cfg["sources"]:
        if not src.get("enabled", True): continue
        try:
            candidates.extend(await collect_source(src))
        except Exception as e:
            print(f"[SOURCE ERROR] {src['id']}: {e}")

    unique = {}
    for a in candidates:
        if not a.text: continue
        key = a.url + "|" + a.content_hash
        if key not in seen:
            unique[key] = a
            seen[key] = {"seen_at": now(), "source": a.source_id}
    print(f"Collected={len(candidates)} New={len(unique)}")

    for a in unique.values():
        try:
            analysis = await analyze(a)
        except Exception as e:
            print(f"[AI ERROR] {a.url}: {e}")
            analysis = None
        if not analysis:
            continue
        if not qualifies_zero_day(analysis, rules):
            continue

        vkey = internal_vuln_key(analysis)
        rid = next_id(vulns) if vkey not in vulns else vulns[vkey]["Record_ID"]
        record = vulns.get(vkey, {
            "Record_ID": rid, "First_Seen": now(), "Source_Count": 0,
            "Alert_Status": "NOT_SENT", "Last_Alert_UTC": ""
        })
        record.update({
            "Last_Seen": now(),
            "State": "ZERO_DAY_CANDIDATE",
            "Confidence": analysis.confidence,
            "Title": analysis.title or a.title,
            "Vendor": analysis.vendor or "",
            "Product": analysis.product or "",
            "Affected_Versions": ", ".join(analysis.affected_versions),
            "CVE": ", ".join(analysis.cve_ids),
            "Alternate_IDs": ", ".join(analysis.alternate_ids),
            "Exploitation": analysis.exploitation_status,
            "Patch_Status": "AVAILABLE" if analysis.patch_available else "NOT_AVAILABLE" if analysis.patch_available is False else "UNKNOWN",
            "Mitigation": analysis.mitigation,
            "Fixed_Versions": ", ".join(analysis.fixed_versions),
            "Impact": analysis.impact,
            "Recommended_Action": analysis.recommended_action,
            "Primary_Source": a.source_name,
            "Source_URL": a.url,
            "Source_Count": int(record.get("Source_Count",0)) + 1
        })
        if not dry_run:
            ak = alert_key(rid, record["State"], "ZERO_DAY")
            if ak not in alerts:
                ok = await send_alert(record)
                if ok:
                    alerts[ak] = {"sent_at": now(), "record_id": rid}
                    record["Alert_Status"] = "SENT"
                    record["Alert_Key"] = ak
                    record["Last_Alert_UTC"] = now()
        vulns[vkey] = record

    save_all(vulns, seen, alerts)
    write_excel(vulns)
    print(f"Zero-day records={len(vulns)}")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    asyncio.run(run(args.dry_run))
