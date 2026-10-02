import asyncio, feedparser, httpx, re
from bs4 import BeautifulSoup
from trafilatura import extract
from app.models import Article
from app.utils import canonical_url, sha256

HEADERS = {"User-Agent": "ZeroDayIntelligence/1.0 (+security-research)"}

async def fetch(url):
    async with httpx.AsyncClient(timeout=20, follow_redirects=True, headers=HEADERS) as c:
        r = await c.get(url)
        r.raise_for_status()
        return r

async def collect_source(src):
    if src["type"] == "rss":
        r = await fetch(src["url"])
        feed = feedparser.parse(r.text)
        out = []
        for e in feed.entries[:50]:
            u = canonical_url(e.get("link",""))
            if not u: continue
            out.append(await article_from_url(src, u, e.get("title",""), e.get("published")))
        return [x for x in out if x]
    if src["type"] == "json":
        r = await fetch(src["url"])
        data = r.json()
        out = []
        for item in data.get("vulnerabilities", [])[:100]:
            u = canonical_url(item.get("url","") or src["url"])
            title = item.get("vulnerabilityName","")
            text = " ".join(str(v) for v in item.values())
            out.append(Article(source_id=src["id"], source_name=src["name"], tier=src["tier"],
                               url=u, title=title, text=text, content_hash=sha256(text)))
        return out
    return []

async def article_from_url(src, url, title="", published=None):
    try:
        r = await fetch(url)
        body = extract(r.text, include_comments=False, include_tables=True) or ""
        if not body:
            soup = BeautifulSoup(r.text, "html.parser")
            body = soup.get_text(" ", strip=True)
        body = body[:50000]
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            u = canonical_url(urljoin(url, a["href"]))
            if u and u not in links and len(links) < 50:
                links.append(u)
        if not title:
            title = soup.title.get_text(" ", strip=True) if soup.title else url
        return Article(source_id=src["id"], source_name=src["name"], tier=src["tier"],
                        url=url, title=title, published=published, text=body,
                        content_hash=sha256(body), links=links)
    except Exception:
        return None

from urllib.parse import urljoin
