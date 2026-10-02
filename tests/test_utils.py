from app.utils import canonical_url, internal_vuln_key
from app.models import Analysis

def test_canonical_url():
    assert canonical_url("HTTPS://Example.COM/a/?utm_source=x") == "https://example.com/a"

def test_key_uses_cve():
    a = Analysis(title="x", cve_ids=["CVE-2026-1234"])
    assert internal_vuln_key(a) == "ID:CVE-2026-1234"
