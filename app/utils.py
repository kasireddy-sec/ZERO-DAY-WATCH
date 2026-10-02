import hashlib, re
from urllib.parse import urljoin, urlparse, urldefrag

TRACKING = {"utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid","fbclid"}

def canonical_url(url: str) -> str:
    url, _ = urldefrag(url.strip())
    p = urlparse(url)
    if p.scheme not in {"http","https"}:
        return ""
    q = []
    for item in p.query.split("&") if p.query else []:
        if not item:
            continue
        k = item.split("=",1)[0].lower()
        if k not in TRACKING:
            q.append(item)
    path = re.sub(r"/+$", "", p.path or "/")
    return f"{p.scheme.lower()}://{p.netloc.lower()}{path}" + (("?" + "&".join(q)) if q else "")

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "ignore")).hexdigest()

def internal_vuln_key(a) -> str:
    ids = [x.upper() for x in (a.cve_ids + a.alternate_ids) if x]
    if ids:
        return "ID:" + "|".join(sorted(set(ids)))
    vendor = (a.vendor or "").lower().strip()
    product = (a.product or "").lower().strip()
    title = re.sub(r"\W+", " ", a.title.lower()).strip()
    return "FP:" + sha256(f"{vendor}|{product}|{title}")[:24]

def alert_key(record_id: str, state: str, alert_type: str) -> str:
    return sha256(f"{record_id}|{state}|{alert_type}")[:32]
