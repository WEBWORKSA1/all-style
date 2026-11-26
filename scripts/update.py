#!/usr/bin/env python3
"""Refresh All-Style's automated data (run by GitHub Actions every 6 hours).

- data/trends.json : latest headlines per pillar from Google News RSS searches
- data/heat.json   : Style Heat Index (daily counts of style-name mentions in new headlines)
- data/videos.json : latest uploads from curated YouTube channels (handle -> channel RSS)
- data/channels.json : cache of resolved YouTube channel IDs

Every fetch is best-effort: failures are logged and previous data is kept, so the site never breaks.
Standard library only.
"""
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "Mozilla/5.0 (compatible; AllStyleBot/1.0; +https://github.com/webworksa1/all-style)"
NOW = dt.datetime.now(dt.timezone.utc)
TODAY = NOW.date().isoformat()
GENERIC = {"Classic", "Minimalist", "Contemporary", "Traditional", "Bob", "Rustic", "Coastal", "Industrial", "Western",
           "Transitional", "Bohemian", "Scandi Style", "Mediterranean", "Scandinavian", "Preppy", "Grunge", "Maximalist"}


def load(rel, default):
    p = ROOT / rel
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def save(rel, obj):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8", "Cookie": "CONSENT=YES+1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def log(*a):
    print("[update]", *a, file=sys.stderr)


SITE = load("src/data/site.json", {})
STYLES = []
for p in ["wear", "home", "hair", "occasion"]:
    STYLES += load(f"src/data/styles/{p}.json", [])


# ---------------- headlines ----------------
def fetch_news(query):
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": f"{query} when:3d", "hl": "en-US", "gl": "US", "ceid": "US:en"})
    root = ET.fromstring(get(url))
    out = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        src_el = it.find("source")
        source = (src_el.text or "").strip() if src_el is not None else ""
        if source and title.endswith(" - " + source):
            title = title[: -len(source) - 3].strip()
        pub = it.findtext("pubDate") or ""
        try:
            date = dt.datetime.strptime(pub, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=dt.timezone.utc).isoformat()
        except Exception:
            date = NOW.isoformat()
        if title and link.startswith("http"):
            out.append({"title": title[:180], "link": link, "source": source[:60], "date": date})
    return out


def update_trends():
    old = load("data/trends.json", {"pillars": {}})
    pillars = {}
    allnew = []
    for pillar, queries in SITE.get("feeds", {}).items():
        items, seen = [], set()
        for q in queries:
            try:
                for x in fetch_news(q):
                    key = x["title"].lower()
                    if key not in seen:
                        seen.add(key)
                        items.append(x)
                time.sleep(1)
            except Exception as e:
                log("news failed:", q, e)
        items.sort(key=lambda x: x["date"], reverse=True)
        pillars[pillar] = items[:14] if items else old.get("pillars", {}).get(pillar, [])
        allnew += items
    save("data/trends.json", {"updated": NOW.isoformat(), "pillars": pillars})
    log("trends:", {k: len(v) for k, v in pillars.items()})
    return allnew


def terms_for(st):
    t = [a for a in st.get("aka", []) if len(a) > 3]
    if st["n"] not in GENERIC:
        t.append(st["n"].split(" (")[0])
    return sorted(set(x.lower() for x in t), key=len, reverse=True)


def update_heat(headlines):
    heat = load("data/heat.json", {"seen": {}, "days": {}})
    seen, days = heat.get("seen", {}), heat.get("days", {})
    pats = {st["s"]: re.compile(r"\b(" + "|".join(re.escape(t) for t in terms_for(st)) + r")\b", re.I) for st in STYLES if terms_for(st)}
    new = 0
    for h in headlines:
        hid = hashlib.sha1(h["title"].lower().encode()).hexdigest()[:16]
        if hid in seen:
            continue
        seen[hid] = TODAY
        new += 1
        day = days.setdefault(TODAY, {})
        for slug, rx in pats.items():
            if rx.search(h["title"]):
                day[slug] = day.get(slug, 0) + 1
    cutoff_seen = (NOW.date() - dt.timedelta(days=30)).isoformat()
    cutoff_days = (NOW.date() - dt.timedelta(days=60)).isoformat()
    seen = {k: v for k, v in seen.items() if v >= cutoff_seen}
    days = {k: v for k, v in days.items() if k >= cutoff_days}
    save("data/heat.json", {"updated": NOW.isoformat(), "seen": seen, "days": days})
    log("heat: new headlines", new, "today counts", days.get(TODAY, {}))


# ---------------- videos ----------------
def resolve_channel(handle, cache):
    if handle in cache:
        return cache[handle]
    try:
        page = get("https://www.youtube.com/" + urllib.parse.quote(handle, safe="@")).decode("utf-8", "ignore")
        m = (re.search(r'<link rel="canonical" href="https://www\.youtube\.com/channel/(UC[\w-]{22})"', page)
             or re.search(r'"externalId":"(UC[\w-]{22})"', page) or re.search(r'"channelId":"(UC[\w-]{22})"', page))
        if m:
            cache[handle] = m.group(1)
            return m.group(1)
    except Exception as e:
        log("resolve failed:", handle, e)
    return None


def update_videos():
    cache = load("data/channels.json", {})
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}
    items = []
    for ch in SITE.get("channels", []):
        cid = resolve_channel(ch["handle"], cache)
        if not cid:
            continue
        try:
            root = ET.fromstring(get("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid))
            name = root.findtext("a:title", default=ch["handle"], namespaces=ns)
            for e in root.findall("a:entry", ns)[:6]:
                vid = e.findtext("yt:videoId", namespaces=ns)
                title = e.findtext("a:title", namespaces=ns) or ""
                link = e.find("a:link", ns)
                href = link.get("href", "") if link is not None else ""
                if not vid or "/shorts/" in href:
                    continue
                items.append({"id": vid, "title": title[:140], "channel": name, "pillar": ch["pillar"], "published": e.findtext("a:published", namespaces=ns) or ""})
            time.sleep(0.5)
        except Exception as e:
            log("feed failed:", ch["handle"], e)
    save("data/channels.json", cache)
    if items:
        items.sort(key=lambda x: x["published"], reverse=True)
        save("data/videos.json", {"updated": NOW.isoformat(), "items": items[:80]})
    log("videos:", len(items))


def main():
    headlines = update_trends()
    update_heat(headlines)
    update_videos()


if __name__ == "__main__":
    main()
