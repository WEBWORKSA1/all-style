#!/usr/bin/env python3
"""Render every All-Style page from src/data (+ auto-refreshed data/*.json) into static HTML.

Run:  python scripts/build.py
Output is written in place (index.html, styles/<slug>/index.html, ...) so GitHub Pages can
serve the repository root from the main branch with no build step on GitHub's side.
"""
import datetime as dt
import hashlib
import html
import json
import re
import shutil
from email.utils import format_datetime
from pathlib import Path

from pages_tools import TOOLS
from pages_static import STATIC_PAGES, get_styled_body, pros_body, support_body, contests_body, careers_body, partners_body, contact_body

ROOT = Path(__file__).resolve().parents[1]
E = html.escape


def load(rel, default=None):
    p = ROOT / rel
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


SITE = load("src/data/site.json")
PILLARS = SITE["pillars"]
PORDER = ["wear", "home", "hair", "occasion"]
STYLES = []
for _p in PORDER:
    STYLES += load(f"src/data/styles/{_p}.json")
BY = {s["s"]: s for s in STYLES}
GUIDES = load("src/data/guides.json")
QUIZ = load("src/data/quiz.json")
TRENDS = load("data/trends.json", {}) or {}
VIDEOS = load("data/videos.json", {}) or {}
HEAT = load("data/heat.json", {}) or {}
BASE = SITE["url"].rstrip("/")
NOW = dt.datetime.now(dt.timezone.utc)
TODAY = NOW.date()
LAUNCH = "2026-11-26"
SITEMAP = []  # (path, lastmod, priority)
PILLAR_PATH = {"wear": "wear/", "home": "home/", "hair": "hair-beauty/", "occasion": "occasions/"}
PRO_NOUN = {"wear": "a personal stylist", "home": "an interior designer", "hair": "a hair & makeup pro", "occasion": "a wedding or event stylist"}
SERVICE_BY_PILLAR = {"wear": "personal-styling", "home": "interior-room", "hair": "hair-makeup", "occasion": "wedding-styling"}

# ---------- validation ----------
for s in STYLES:
    s["pr"] = [x for x in s.get("pr", []) if x in BY and x != s["s"]]
assert len(BY) == len(STYLES), "duplicate style slug"


# ---------- helpers ----------
def seed(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


def art(st, w=480, h=300):
    """Deterministic generative artwork from a style's palette (no photos, no copyright risk)."""
    c = [x[1] for x in st["c"]]
    r = seed(st["s"])
    p = st["p"]
    lab = E(st["n"]) + " palette artwork"
    o = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{lab}" preserveAspectRatio="xMidYMid slice">',
         f'<rect width="{w}" height="{h}" fill="{c[0]}"/>']
    if p == "wear":
        x = 0
        widths = [40 + (r >> (i * 3)) % 70 for i in range(6)]
        for i, wd in enumerate(widths):
            o.append(f'<rect x="{x}" y="0" width="{wd}" height="{h}" fill="{c[(i % 4) + 1]}" opacity="{0.92 if i % 2 else 1}"/>')
            x += wd + 6
            if x > w:
                break
        cx = 120 + r % 240
        o.append(f'<path d="M0 {h*0.72} Q {w/2} {h*0.45} {w} {h*0.78} L {w} {h} L 0 {h} Z" fill="{c[0]}" opacity=".88"/>')
        o.append(f'<circle cx="{cx}" cy="{h*0.68:.0f}" r="26" fill="{c[2]}"/><circle cx="{cx}" cy="{h*0.68:.0f}" r="9" fill="{c[0]}"/>')
    elif p == "home":
        o.append(f'<rect y="{h*0.72:.0f}" width="{w}" height="{h*0.28:.0f}" fill="{c[1]}"/>')
        ax = 60 + r % 120
        o.append(f'<path d="M{ax} {h*0.72:.0f} V 95 a 70 70 0 0 1 140 0 V {h*0.72:.0f} Z" fill="{c[3]}"/>')
        o.append(f'<path d="M{ax+14} {h*0.72:.0f} V 100 a 56 56 0 0 1 112 0 V {h*0.72:.0f} Z" fill="{c[0]}" opacity=".55"/>')
        sx = ax + 170 if ax + 330 < w else 30
        o.append(f'<rect x="{sx}" y="{h*0.55:.0f}" width="190" height="62" rx="22" fill="{c[2]}"/><rect x="{sx+10}" y="{h*0.47:.0f}" width="170" height="40" rx="16" fill="{c[2]}" opacity=".85"/>')
        o.append(f'<circle cx="{w-50}" cy="70" r="24" fill="{c[4]}"/><rect x="{w-52}" y="94" width="4" height="{h*0.72-94:.0f}" fill="{c[4]}"/>')
    elif p == "hair":
        ox, oy = (w if r % 2 else 0), h
        for i in range(7):
            rr = 330 - i * 44
            o.append(f'<circle cx="{ox}" cy="{oy}" r="{rr}" fill="{c[(i % 4) + 1]}"/>')
        o.append(f'<path d="M0 {h*0.3:.0f} C {w*0.3:.0f} {h*0.1:.0f}, {w*0.6:.0f} {h*0.5:.0f}, {w} {h*0.25:.0f}" stroke="{c[0]}" stroke-width="10" fill="none" opacity=".7"/>')
    else:
        cx, cy = w / 2, h * 1.02
        n = 14
        import math
        for i in range(n):
            a1 = math.pi + i * math.pi / n
            a2 = math.pi + (i + 1) * math.pi / n
            x1, y1 = cx + 300 * math.cos(a1), cy + 300 * math.sin(a1)
            x2, y2 = cx + 300 * math.cos(a2), cy + 300 * math.sin(a2)
            o.append(f'<path d="M{cx:.0f} {cy:.0f} L{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f} Z" fill="{c[1] if i % 2 else c[2]}"/>')
        o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="90" fill="{c[3]}"/><circle cx="{cx:.0f}" cy="{cy:.0f}" r="60" fill="{c[0]}"/>')
        o.append(f'<path d="M{w-70} 40 l 26 26 l -26 26 l -26 -26 Z" fill="{c[4]}"/>')
    o.append("</svg>")
    return "".join(o)


def palette_html(st):
    return '<div class="palette">' + "".join(f'<span style="background:{h}" title="{E(n)} {h}"></span>' for n, h in st["c"]) + "</div>"


def card(st):
    k = " ".join([st["n"], st["t"], " ".join(st.get("aka", [])), " ".join(st["m"]), PILLARS[st["p"]]["name"]]).lower()
    return (f'<article class="style-card" data-p="{st["p"]}" data-k="{E(k)}"><div class="art">{art(st)}</div>'
            f'<div class="body"><span class="chip {st["p"]}">{E(PILLARS[st["p"]]["name"])}</span>'
            f'<h3><a href="{{{{R}}}}styles/{st["s"]}/">{E(st["n"])}</a></h3><p>{E(st["t"])}</p></div>'
            f'<button class="save-btn" type="button" data-save="{st["s"]}" aria-pressed="false" aria-label="Save to My Board"></button></article>')


def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{a}</p></details>" for q, a in faqs) + "</div>"


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faqs]}


def ad(kind="display"):
    slot = SITE.get("ad_slots", {}).get(kind)
    if not slot:
        return ""  # Auto ads handle placement until manual slots are configured
    return (f'<div class="ad-slot"><div class="ad-label">Advertisement</div><ins class="adsbygoogle" style="display:block" '
            f'data-ad-client="{SITE["adsense_client"]}" data-ad-slot="{slot}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
            f'<script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>')


def fmt_date(s):
    try:
        d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return d.strftime("%b %-d, %Y")
    except Exception:
        return ""


def ago(s):
    try:
        d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        h = (NOW - d).total_seconds() / 3600
        if h < 1:
            return "just now"
        if h < 24:
            return f"{int(h)}h ago"
        return f"{int(h // 24)}d ago"
    except Exception:
        return ""


def daily_style(date=None):
    d = (date or TODAY) - dt.date(1970, 1, 1)
    return STYLES[(d.days * 7919) % len(STYLES)]


def contest_theme(date=None):
    d = date or TODAY
    return SITE["contest_themes"][(d.month - 1) % len(SITE["contest_themes"])]


# ---------- auto data views ----------
def heat_rank(limit=10):
    days = HEAT.get("days", {})
    if not days:
        return []
    last7 = [(TODAY - dt.timedelta(days=i)).isoformat() for i in range(7)]
    prev7 = [(TODAY - dt.timedelta(days=i)).isoformat() for i in range(7, 14)]
    rows = []
    for st in STYLES:
        a = sum(days.get(d, {}).get(st["s"], 0) for d in last7)
        b = sum(days.get(d, {}).get(st["s"], 0) for d in prev7)
        if a or b:
            rows.append((st, a, b))
    rows.sort(key=lambda x: (-x[1], -x[2], x[0]["n"]))
    return rows[:limit]


def heat_html(limit=10):
    rows = heat_rank(limit)
    if not rows:
        return ('<div class="empty">The Style Heat Index is warming up. It counts how often each style is named in tracked fashion, '
                'interiors, beauty and wedding headlines, refreshed automatically every six hours.</div>')
    top = max(1, rows[0][1])
    out = []
    for i, (st, a, b) in enumerate(rows, 1):
        if b == 0 and a > 0:
            dl, cls = "new", "up"
        elif a == b:
            dl, cls = "=", ""
        else:
            pct = round((a - b) / max(b, 1) * 100)
            dl, cls = (f"+{pct}%" if pct > 0 else f"{pct}%"), ("up" if pct > 0 else "down")
        out.append(f'<div class="heat-row"><span class="n">{i:02d}</span><a href="{{{{R}}}}styles/{st["s"]}/">{E(st["n"])} <span class="chip {st["p"]}" style="margin-left:6px">{E(PILLARS[st["p"]]["name"])}</span></a>'
                   f'<div class="heat-bar"><i style="width:{max(6, round(a / top * 100))}%"></i></div><span class="delta {cls}">{dl}</span></div>')
    return "".join(out)


def news_html(pillar=None, limit=8):
    pil = TRENDS.get("pillars", {})
    items = []
    if pillar:
        items = pil.get(pillar, [])
    else:
        for p in PORDER:
            items += [dict(x, _p=p) for x in pil.get(p, [])[:3]]
        items.sort(key=lambda x: x.get("date", ""), reverse=True)
    items = items[:limit]
    if not items:
        return '<div class="empty">Fresh headlines from around the style world load here automatically on the next refresh.</div>'
    return '<ul class="news">' + "".join(
        f'<li><a href="{E(x["link"])}" target="_blank" rel="noopener nofollow">{E(x["title"])}</a>'
        f'<small>{E(x.get("source", ""))}{" · " + ago(x["date"]) if x.get("date") else ""}</small></li>' for x in items) + "</ul>"


def videos_for(pillar=None, limit=6, match=None):
    items = VIDEOS.get("items", [])
    if pillar:
        items = [v for v in items if v.get("pillar") == pillar]
    if match:
        terms = [t.lower() for t in match]
        hit = [v for v in items if any(t in v.get("title", "").lower() for t in terms)]
        items = hit
    return items[:limit]


def video_cards(items):
    return "".join(
        f'<div class="video-card"><div class="yt" data-id="{E(v["id"])}" data-title="{E(v["title"])}">'
        f'<img loading="lazy" src="https://i.ytimg.com/vi/{E(v["id"])}/hqdefault.jpg" alt="{E(v["title"])}" width="480" height="360"></div>'
        f'<h3>{E(v["title"])}</h3><small class="muted">{E(v.get("channel", ""))}{" · " + fmt_date(v["published"]) if v.get("published") else ""}</small></div>'
        for v in items)


def yt_search_links(terms):
    return '<div class="chips">' + "".join(
        f'<a class="btn btn-ghost btn-sm" target="_blank" rel="noopener" href="https://www.youtube.com/results?search_query={E(t.replace(" ", "+"))}">▶ {E(t)}</a>'
        for t in terms) + "</div>"


# ---------- layout ----------
NAV = [("styles/", "Style Atlas"), ("quiz/", "Style Quiz"), ("tools/", "Tools"), ("trends/", "Trends"), ("videos/", "Videos"), ("guides/", "Guides")]
ICON_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
ICON_MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
ICON_HEART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7.5-4.6-10-9.2C.3 8.6 2.2 4.5 6 4.5c2.1 0 3.4 1.1 4 2.2.6-1.1 1.9-2.2 4-2.2 3.8 0 5.7 4.1 4 7.3C19.5 16.4 12 21 12 21z"/></svg>'


def footer():
    tools = "".join(f'<li><a href="{{{{R}}}}tools/{t["slug"]}/">{E(t["name"])}</a></li>' for t in TOOLS[:7])
    return f"""<footer class="site-footer"><div class="wrap"><div class="foot-grid">
<div><a class="foot-logo" href="{{{{R}}}}">All-Style</a><p style="color:#B9B0A2;font-size:.92rem;max-width:34ch">{E(SITE["tagline"])} The Style Atlas for what you wear, where you live and how you celebrate.</p>
<form class="form" data-form="Newsletter signup" data-ok="You're on the list. Look out for the Weekly Style Brief." novalidate>
<label class="sr" for="nl-email">Email for the Weekly Style Brief</label><div class="foot-news"><input id="nl-email" type="email" name="email" placeholder="Your email" required><input type="hidden" name="list" value="Weekly Style Brief"><input class="hp" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="btn" type="submit">Join</button></div>
<small style="color:#A89F91">One email a week. Unsubscribe any time.</small></form></div>
<div><h4>Explore</h4><ul><li><a href="{{{{R}}}}styles/">Style Atlas</a></li><li><a href="{{{{R}}}}wear/">Wear</a></li><li><a href="{{{{R}}}}home/">Interiors</a></li><li><a href="{{{{R}}}}hair-beauty/">Hair &amp; Beauty</a></li><li><a href="{{{{R}}}}occasions/">Occasions</a></li><li><a href="{{{{R}}}}compare/">Compare styles</a></li><li><a href="{{{{R}}}}daily/">Style of the Day</a></li><li><a href="{{{{R}}}}board/">My Board</a></li></ul></div>
<div><h4>Tools</h4><ul><li><a href="{{{{R}}}}quiz/">Style DNA Quiz</a></li>{tools}<li><a href="{{{{R}}}}tools/">All tools</a></li></ul></div>
<div><h4>Get involved</h4><ul><li><a href="{{{{R}}}}get-styled/">Get Styled (free match)</a></li><li><a href="{{{{R}}}}pros/">For professionals</a></li><li><a href="{{{{R}}}}contests/">Contests &amp; prizes</a></li><li><a href="{{{{R}}}}careers/">Careers</a></li><li><a href="{{{{R}}}}support/">Support All-Style</a></li><li><a href="{{{{R}}}}partners/">Advertise &amp; partner</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="{{{{R}}}}about/">About &amp; editorial policy</a></li><li><a href="{{{{R}}}}contact/">Contact</a></li><li><a href="{{{{R}}}}privacy/">Privacy policy</a></li><li><a href="{{{{R}}}}cookies/">Cookie policy</a></li><li><a href="{{{{R}}}}terms/">Terms of use</a></li><li><a href="{{{{R}}}}disclaimer/">Disclaimer</a></li><li><a href="{{{{R}}}}trademark/">Trademark &amp; copyright</a></li></ul></div>
</div><div class="foot-legal"><span>© <span data-year>{TODAY.year}</span> All-Style. All rights reserved. Independent publication; not affiliated with any brand named "Alstyle", "Allstyle" or "All Style". <a href="{{{{R}}}}trademark/">Disclosure</a></span><span>Original writing &amp; generated artwork. No stock or third-party photos.</span></div></div></footer>"""


def layout(path, title, desc, body, *, crumbs=None, schema=None, ogtype="website", tools_js=False, sticky=None,
           noindex=False, absolute=False, priority="0.6", lastmod=None, h_title=None):
    if path == "404.html":
        depth = 0
    else:
        depth = path.count("/")
    R = (BASE + "/") if absolute else ("../" * depth if depth else "./")
    canonical = BASE + "/" + ("" if path == "index" else path)
    full_title = (title + " | All-Style") if title != "All-Style" else "All-Style: Every style, decoded"
    schemas = list(schema or [])
    if crumbs:
        schemas.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u} for i, (n, u) in enumerate([("Home", "")] + crumbs)]})
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    crumb_html = ""
    if crumbs:
        crumb_html = '<nav class="crumbs" aria-label="Breadcrumb"><a href="{{R}}">Home</a>' + "".join(
            (f' / <a href="{{{{R}}}}{u}">{E(n)}</a>' if i < len(crumbs) - 1 else f" / <span>{E(n)}</span>") for i, (n, u) in enumerate(crumbs)) + "</nav>"
    body = body.replace("{{CRUMBS}}", crumb_html)
    nav = "".join(f'<a href="{{{{R}}}}{u}"{" aria-current=\"page\"" if path.startswith(u) else ""}>{n}</a>' for u, n in NAV)
    sticky_html = ""
    if sticky:
        sticky_html = f'<div class="sticky-cta" id="sticky-cta" role="complementary" aria-label="Get styled"><span>{sticky[0]}</span><a class="btn btn-sm" href="{sticky[1]}">{sticky[2]}</a><button class="x" type="button" aria-label="Dismiss">×</button></div>'
    og_img = BASE + "/assets/img/og.png"
    page = f"""<!doctype html>
<html lang="en" data-root="{R}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canonical}">
{'<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'}
<meta property="og:site_name" content="All-Style"><meta property="og:type" content="{ogtype}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#1B1916">
<link rel="icon" href="{R}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{R}manifest.webmanifest">
<link rel="alternate" type="application/rss+xml" title="All-Style" href="{R}feed.xml">
<script>(function(){{try{{var d=document.documentElement,t=localStorage.getItem('as-theme');t=t?JSON.parse(t):(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');d.setAttribute('data-theme',t);if(JSON.parse(localStorage.getItem('as-consent')||'null')==='essential'){{(window.adsbygoogle=window.adsbygoogle||[]).requestNonPersonalizedAds=1}}}}catch(e){{}}}})();</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/css/main.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><a href="{SITE["contact_link"]}" target="_blank" rel="noopener">{E(SITE["contact_text"])}</a></div>
<header class="site-header"><div class="wrap hdr">
<a class="logo" href="{R}" aria-label="All-Style home"><span class="logo-mark" aria-hidden="true"></span><span>All<b>-</b>Style</span></a>
<nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn btn-accent btn-sm" style="margin-left:8px;color:#fff" href="{R}get-styled/">Get Styled</a></nav>
<div class="hdr-actions"><button class="icon-btn" type="button" data-search-open aria-label="Search (press /)">{ICON_SEARCH}</button><a class="icon-btn" href="{R}board/" aria-label="My Board" title="My Board">{ICON_HEART}</a><button class="icon-btn" id="theme-btn" type="button" aria-label="Toggle dark mode">{ICON_MOON}</button><button class="icon-btn menu-btn" id="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">{ICON_MENU}</button></div>
</div></header>
<main id="main">
{body}
</main>
{footer()}
<div class="search-ov" id="search-ov" role="dialog" aria-modal="true" aria-label="Search"><div class="search-box"><input id="search-input" type="search" placeholder="Search styles, tools and guides…" autocomplete="off" aria-label="Search"><div class="search-res" id="search-res"></div></div></div>
<div class="cookie" id="cookie" role="dialog" aria-label="Cookie preferences"><p>We use cookies for essential features and, with your consent, Google advertising cookies to show personalised ads. See our <a href="{R}cookies/">cookie policy</a>.</p><div class="btn-row"><button class="btn btn-sm" type="button" data-consent="all">Accept all</button><button class="btn btn-ghost btn-sm" type="button" data-consent="essential">Essential only</button></div></div>
{sticky_html}
<script src="{R}assets/js/main.js" defer></script>
{f'<script src="{R}assets/js/tools.js" defer></script>' if tools_js else ''}
</body>
</html>
"""
    page = page.replace("{{R}}", R)
    if path == "404.html":
        out = ROOT / "404.html"
    else:
        out = ROOT / (path if path != "index" else "") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    if not noindex and path != "404.html":
        SITEMAP.append(("" if path == "index" else path, lastmod or LAUNCH, priority))


def section(title, sub, inner, link=None, alt=False):
    lk = f'<a class="btn btn-ghost btn-sm" href="{link[0]}">{link[1]}</a>' if link else ""
    return (f'<section class="section{" section-alt" if alt else ""}"><div class="wrap"><div class="sec-head"><div><h2>{title}</h2>'
            f'{"<p>" + sub + "</p>" if sub else ""}</div>{lk}</div>{inner}</div></section>')


# ---------- pages ----------
def page_home():
    picks = [BY[s] for s in ["japandi", "old-money", "wolf-cut", "black-tie", "mid-century-modern", "dark-academia", "curtain-bangs", "boho-wedding"]]
    mosaic = "".join(f'<a href="{{{{R}}}}styles/{s["s"]}/">{art(s, 300, 400)}<span>{E(s["n"])}</span></a>' for s in picks)
    ds = daily_style()
    pillars = "".join(
        f'<a href="{{{{R}}}}{PILLAR_PATH[p]}"><span class="chip {p}">{E(PILLARS[p]["name"])}</span><b>{E(PILLARS[p]["long"])}</b><span>{sum(1 for s in STYLES if s["p"] == p)} styles decoded</span></a>' for p in PORDER)
    featured = "".join(card(BY[s]) for s in ["japandi", "old-money", "modern-organic", "clean-girl", "wabi-sabi", "taper-fade", "classic-elegant-wedding", "scandinavian-interior"])
    tools = "".join(f'<a class="card tool-card" href="{{{{R}}}}tools/{t["slug"]}/"><span class="ico">{t["ico"]}</span><h3>{E(t["name"])}</h3><p class="muted small">{E(t["short"])}</p></a>' for t in TOOLS[:8])
    vids = videos_for(limit=4)
    vid_html = f'<div class="grid g4">{video_cards(vids)}</div>' if vids else yt_search_links(["japandi living room", "old money outfits", "wolf cut tutorial", "black tie dress code"])
    guides = "".join(f'<a class="card" style="text-decoration:none" href="{{{{R}}}}guides/{g["slug"]}/"><span class="chip {g["pillar"]}">{E(PILLARS[g["pillar"]]["name"])}</span><h3 style="margin-top:10px">{E(g["title"])}</h3><p class="muted small">{E(g["desc"])}</p></a>' for g in GUIDES[:3])
    body = f"""
<section class="hero"><div class="wrap hero-grid"><div>
<span class="eyebrow">The Style Atlas</span>
<h1>Every style, <em>decoded.</em> Then made yours.</h1>
<p class="lead">From Old Money to Japandi, wolf cuts to white tie: {len(STYLES)} styles explained with palettes, signature pieces and how to start. Take the free quiz to find your mix, then get matched with a pro who works in it.</p>
<div class="hero-search"><button class="fake-input" type="button" data-search-open>Search a style, e.g. “Japandi” or “black tie”</button></div>
<div class="btn-row"><a class="btn btn-accent" href="{{{{R}}}}quiz/">Take the Style DNA Quiz</a><a class="btn btn-ghost" href="{{{{R}}}}styles/">Browse the Atlas</a></div>
<div class="stats"><div><b>{len(STYLES)}</b>styles decoded</div><div><b>{len(TOOLS) + 2}</b>free tools</div><div><b>4</b>areas of life</div><div><b>6h</b>auto-refresh</div></div>
</div><div class="hero-mosaic" aria-label="Featured styles">{mosaic}</div></div></section>
<section class="section"><div class="wrap"><div class="pillar-band">{pillars}</div></div></section>
{section("Featured in the Atlas", "Deep, practical profiles: what each style is, where it came from, its palette with hex codes and how to start this week.", '<div class="grid g4">' + featured + "</div>", ("{{R}}styles/", "See all " + str(len(STYLES)) + " styles"))}
<section class="section section-alt"><div class="wrap daily"><div>
<span class="eyebrow">Style of the Day · {TODAY.strftime("%B %-d")}</span>
<h2 data-daily-name>{E(ds["n"])}</h2><p class="lead" data-daily-tag>{E(ds["t"])}</p>
<div class="palette" data-daily-pal style="max-width:420px;margin:14px 0 18px">{"".join(f'<span style="background:{h}"></span>' for n, h in ds["c"])}</div>
<a class="btn" data-daily-link data-daily-auto="{ds["s"]}" href="{{{{R}}}}styles/{ds["s"]}/">Read today's style</a></div>
<div class="card"><h3>Style Heat Index</h3><p class="small muted">Most-mentioned styles in tracked headlines this week.</p>{heat_html(6)}<p style="margin:14px 0 0"><a href="{{{{R}}}}trends/">Full Trend Pulse →</a></p></div></div></section>
{section("Free style tools", "No sign-up, no paywall. Everything runs in your browser.", '<div class="grid g4">' + tools + "</div>", ("{{R}}tools/", "All tools"))}
<section class="section"><div class="wrap"><div class="cta-card" style="display:grid;grid-template-columns:1.3fr .7fr;gap:24px;align-items:center;padding:clamp(24px,4vw,44px)">
<div><span class="eyebrow" style="color:#F0A58E">Get Styled · free to request</span><h2 style="color:inherit">Love a style? Get a pro who works in it.</h2><p>Tell us what you need — a wardrobe, a room, a cut, a wedding — and we'll match you with a stylist or designer in your style and budget. No obligation.</p></div>
<div class="btn-row" style="justify-content:flex-end"><a class="btn" href="{{{{R}}}}get-styled/">Start my free match</a><a class="btn btn-ghost" style="color:inherit;border-color:rgba(255,255,255,.4)" href="{{{{R}}}}pros/">I'm a professional</a></div></div></div></section>
{section("Trend Pulse", "Latest style headlines from around the web, refreshed automatically.", news_html(limit=8), ("{{R}}trends/", "All trends"), alt=True)}
{section("Watch & learn", "Hand-picked style channels; the library updates itself.", vid_html, ("{{R}}videos/", "Video library"))}
{section("Guides", "Long-form, practical and original.", '<div class="grid g3">' + guides + "</div>", ("{{R}}guides/", "All guides"))}
<section class="section section-alt"><div class="wrap grid g3">
<div class="card"><h3>Contests &amp; prizes</h3><p class="muted">This month: <strong>{E(contest_theme())}</strong>. Enter free, get featured.</p><a class="btn btn-sm" href="{{{{R}}}}contests/">Enter the challenge</a></div>
<div class="card"><h3>Support independent style</h3><p class="muted">Donations fund operations, promotion, new writers and contest prizes.</p><a class="btn btn-sm" href="{{{{R}}}}support/">Support All-Style</a></div>
<div class="card"><h3>Write, film or style with us</h3><p class="muted">Freelance editors, video creators, ambassadors and moderators.</p><a class="btn btn-sm" href="{{{{R}}}}careers/">See open roles</a></div>
</div></section>"""
    schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": "All-Style", "url": BASE + "/",
               "potentialAction": {"@type": "SearchAction", "target": BASE + "/styles/?q={search_term_string}", "query-input": "required name=search_term_string"}},
              {"@context": "https://schema.org", "@type": "Organization", "name": "All-Style", "url": BASE + "/", "logo": BASE + "/assets/img/favicon.svg"}]
    layout("index", "All-Style", SITE["description"], body, schema=schema, priority="1.0", lastmod=TODAY.isoformat(),
           sticky=("Find your style mix in 2 minutes", "{{R}}quiz/", "Take the quiz"))


def page_atlas():
    tabs = '<button class="tab" type="button" data-pf="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="tab" type="button" data-pf="{p}" aria-pressed="false">{E(PILLARS[p]["name"])}</button>' for p in PORDER)
    cards = "".join(card(s) for s in sorted(STYLES, key=lambda x: x["n"]))
    body = f"""<section class="hero" style="padding-bottom:30px"><div class="wrap">{{{{CRUMBS}}}}<span class="eyebrow">The Style Atlas</span><h1>Every style, A to Z</h1>
<p class="lead">{len(STYLES)} named styles across fashion, interiors, hair &amp; beauty and occasions. Filter, search, save your favourites to My Board, or compare any two side by side.</p></div></section>
<section class="section" style="padding-top:30px"><div class="wrap"><div class="filter-bar"><div class="tabs" style="margin:0">{tabs}</div><label class="sr" for="atlas-q">Filter styles</label><input id="atlas-q" type="search" placeholder="Filter by name, mood or alias…"><span id="atlas-count" class="muted small"></span></div>
<div class="grid g4" id="atlas">{cards}</div>
<div class="btn-row" style="margin-top:30px"><a class="btn" href="{{{{R}}}}compare/">Compare two styles</a><a class="btn btn-ghost" href="{{{{R}}}}quiz/">Which styles are mine?</a></div></div></section>"""
    schema = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "The Style Atlas", "url": BASE + "/styles/",
               "hasPart": [{"@type": "Article", "name": s["n"], "url": f"{BASE}/styles/{s['s']}/"} for s in STYLES]}]
    layout("styles/", "The Style Atlas: Every Fashion, Interior, Hair & Occasion Style", f"Browse {len(STYLES)} styles decoded: fashion aesthetics, interior design styles, haircuts and dress codes, each with palette, key pieces and how to start.",
           body, crumbs=[("Style Atlas", "styles/")], schema=schema, priority="0.9")


def style_faqs(st):
    pn = PILLARS[st["p"]]["name"].lower()
    pairs = ", ".join(BY[x]["n"] for x in st["pr"][:3])
    return [
        [f"What is {st['n']}?", f"{st['d']}"],
        [f"What colours go with {st['n']}?", f"A typical {st['n']} palette uses " + ", ".join(f"{n.lower()} ({h})" for n, h in st["c"][:4]) + f" and {st['c'][4][0].lower()}."],
        [f"How do I start with {st['n']}?", " ".join(f"{i}. {x}." for i, x in enumerate(st["st"], 1))],
        [f"What styles go well with {st['n']}?", f"{st['n']} blends naturally with {pairs}." if pairs else f"{st['n']} works well with neutral, pared-back styles."],
        [f"Who suits {st['n']}?", st["w"]],
    ]


def page_style(st):
    p = st["p"]
    pn = PILLARS[p]["name"]
    pairs = "".join(card(BY[x]) for x in st["pr"][:4])
    same = [x for x in STYLES if x["p"] == p and x["s"] != st["s"] and x["s"] not in st["pr"]]
    more = "".join(f'<li><a href="{{{{R}}}}styles/{x["s"]}/">{E(x["n"])}</a></li>' for x in same[:8])
    cmp_links = "".join(f'<li><a href="{{{{R}}}}compare/?a={st["s"]}&amp;b={x}">{E(st["n"])} vs {E(BY[x]["n"])}</a></li>' for x in st["pr"][:3])
    pal_btns = "".join(f'<button type="button" data-copy="{h}"><i style="background:{h}"></i><b>{E(n)}</b><code>{h}</code></button>' for n, h in st["c"])
    svc = SERVICE_BY_PILLAR[p]
    cta_url = f"{{{{R}}}}get-styled/?service={svc}&amp;styles={st['s']}"
    vids = videos_for(p, 2, [st["n"]] + st.get("aka", []))
    vid_block = (f'<div class="block"><h2>Watch</h2><div class="grid g2">{video_cards(vids)}</div></div>' if vids else
                 f'<div class="block"><h2>Watch</h2><p class="muted">See {E(st["n"])} in motion on YouTube:</p>{yt_search_links([st["n"] + (" interior" if p == "home" else " tutorial" if p == "hair" else " outfit ideas" if p == "wear" else " ideas"), st["n"] + " guide"])}</div>')
    faqs = style_faqs(st)
    k_label = {"wear": "Signature pieces", "home": "Signature elements", "hair": "Defining features", "occasion": "What it includes"}[p]
    m_label = {"wear": "Fabrics & materials", "home": "Materials & finishes", "hair": "Tools & products", "occasion": "Fabrics & materials"}[p]
    body = f"""<section class="style-hero"><div class="wrap">{{{{CRUMBS}}}}<div class="style-hero-grid"><div>
<span class="chip {p}">{E(pn)}</span>
<h1 style="margin-top:12px">{E(st["n"])}</h1><p class="lead">{E(st["t"])}</p>
<div class="mood">{"".join(f"<span>{E(m)}</span>" for m in st["m"])}</div>
<div class="btn-row"><a class="btn btn-accent" href="{cta_url}">Get {E(PRO_NOUN[p])} for this style</a><button class="btn btn-ghost" type="button" data-save="{st["s"]}" aria-pressed="false" style="gap:8px">Save</button></div>
{('<p class="small muted" style="margin-top:12px">Also called: ' + E(", ".join(st["aka"][:4])) + "</p>") if st.get("aka") else ""}
</div><div class="art">{art(st, 640, 480)}</div></div></div></section>
<div class="wrap layout"><article>
<div class="block"><h2>What is {E(st["n"])}?</h2><p>{E(st["d"])}</p><p><strong>Origins.</strong> {E(st["o"])}</p></div>
<div class="block"><h2>The palette</h2><p class="muted small">Tap a colour to copy its hex code.</p>{palette_html(st)}<div class="pal-list">{pal_btns}</div></div>
{ad("inarticle")}
<div class="block two-col"><div><h2>{k_label}</h2><ul class="ticks">{"".join(f"<li>{E(x)}</li>" for x in st["k"])}</ul></div>
<div><h2>{m_label}</h2><ul class="ticks">{"".join(f"<li>{E(x)}</li>" for x in st["mat"])}</ul></div></div>
<div class="block two-col"><div><h2>Do</h2><ul class="ticks">{"".join(f"<li>{E(x)}</li>" for x in st["do"])}</ul></div>
<div><h2>Don't</h2><ul class="ticks crosses">{"".join(f"<li>{E(x)}</li>" for x in st["dont"])}</ul></div></div>
<div class="block"><h2>Start in three steps</h2><ol class="steps">{"".join(f"<li>{E(x)}</li>" for x in st["st"])}</ol></div>
<div class="block"><h2>Who it suits &amp; budget tip</h2><p>{E(st["w"])}</p><p class="note"><strong>Budget tip:</strong> {E(st["b"])}</p></div>
{vid_block}
<div class="block"><h2>Frequently asked questions</h2>{faq_html(faqs)}</div>
{('<div class="block"><h2>Works well with</h2><div class="grid g2">' + pairs + "</div></div>") if pairs else ""}
</article>
<aside class="side">
<div class="cta-card"><h3>Make it real</h3><p>Get matched with a pro who works in {E(st["n"])}. Free to request, no obligation.</p><a class="btn" href="{cta_url}">Start my free match</a></div>
<div class="card"><h3>At a glance</h3><dl class="kv"><dt>Area</dt><dd><a href="{{{{R}}}}{PILLAR_PATH[p]}">{E(pn)}</a></dd><dt>Mood</dt><dd>{E(", ".join(st["m"]))}</dd><dt>Key colour</dt><dd>{E(st["c"][1][0])} <code>{st["c"][1][1]}</code></dd><dt>Traits</dt><dd>{E(", ".join(st["q"]))}</dd></dl></div>
{('<div class="card"><h3>Compare</h3><ul style="padding-left:1.1em;margin:0">' + cmp_links + "</ul></div>") if cmp_links else ""}
<div class="card"><h3>More {E(pn)} styles</h3><ul style="padding-left:1.1em;margin:0">{more}</ul></div>
<div class="card"><h3>Is this you?</h3><p class="small muted">Take the {E(pn)} version of the Style DNA Quiz to see your match score.</p><a class="btn btn-sm" href="{{{{R}}}}quiz/?mode={ {'wear':'me','home':'home','hair':'hair','occasion':'event'}[p] }">Take the quiz</a></div>
</aside></div>"""
    schema = [{"@context": "https://schema.org", "@type": "Article", "headline": f"{st['n']}: {st['t']}", "description": st["d"],
               "about": st["n"], "author": {"@type": "Organization", "name": "All-Style"}, "publisher": {"@type": "Organization", "name": "All-Style"},
               "datePublished": LAUNCH, "dateModified": LAUNCH, "mainEntityOfPage": f"{BASE}/styles/{st['s']}/"}, faq_schema(faqs)]
    desc = f"{st['n']} explained: {st['t']} Palette with hex codes, signature pieces, materials, do's and don'ts and how to start."
    layout(f"styles/{st['s']}/", f"{st['n']} {'Interior Style' if p == 'home' else 'Style'} Guide: Palette, Key Pieces & How to Start", desc[:300], body,
           crumbs=[("Style Atlas", "styles/"), (pn, PILLAR_PATH[p]), (st["n"], f"styles/{st['s']}/")], schema=schema, ogtype="article",
           sticky=(f"Love {E(st['n'])}?", cta_url, "Get a free pro match"), priority="0.8")


def page_pillar(p):
    pn = PILLARS[p]["name"]
    items = [s for s in STYLES if s["p"] == p]
    tools = [t for t in TOOLS if t["pillar"] == p]
    guides = [g for g in GUIDES if g["pillar"] == p]
    vids = videos_for(p, 3)
    intro = {
        "wear": "Fashion aesthetics and personal style, decoded: from quiet luxury to streetwear, academia to techwear. Learn the codes, then build your own blend.",
        "home": "Interior design styles explained with palettes, materials and furniture, from Japandi and Mid-Century Modern to Wabi-Sabi and Art Deco.",
        "hair": "Haircuts and makeup looks worth knowing by name, who they suit and how to ask for them, so you leave the salon happy.",
        "occasion": "Dress codes from white tie to smart casual, plus wedding styles that make every vendor decision easier.",
    }[p]
    body = f"""<section class="hero" style="padding-bottom:30px"><div class="wrap">{{{{CRUMBS}}}}<span class="chip {p}">{E(pn)}</span><h1 style="margin-top:12px">{E(PILLARS[p]["long"])}</h1><p class="lead">{intro}</p>
<div class="btn-row"><a class="btn btn-accent" href="{{{{R}}}}get-styled/?service={SERVICE_BY_PILLAR[p]}">Get matched with a pro</a><a class="btn btn-ghost" href="{{{{R}}}}quiz/?mode={ {'wear':'me','home':'home','hair':'hair','occasion':'event'}[p] }">Find my {E(pn)} style</a></div></div></section>
{section(f"{len(items)} {pn} styles", "", '<div class="grid g4">' + "".join(card(s) for s in items) + "</div>")}
{section("Tools for this area", "", '<div class="grid g3">' + "".join(f'<a class="card tool-card" href="{{{{R}}}}tools/{t["slug"]}/"><span class="ico">{t["ico"]}</span><h3>{E(t["name"])}</h3><p class="muted small">{E(t["short"])}</p></a>' for t in tools) + "</div>", alt=True) if tools else ""}
{section("Guides", "", '<div class="grid g3">' + "".join(f'<a class="card" style="text-decoration:none" href="{{{{R}}}}guides/{g["slug"]}/"><h3>{E(g["title"])}</h3><p class="muted small">{E(g["desc"])}</p></a>' for g in guides) + "</div>") if guides else ""}
{section("Latest headlines", "", news_html(p, 6), ("{{R}}trends/", "Trend Pulse"), alt=True)}
{section("Watch", "", ('<div class="grid g3">' + video_cards(vids) + "</div>") if vids else yt_search_links([f"{pn} style ideas", items[0]["n"] + " guide"]))}"""
    layout(PILLAR_PATH[p], f"{PILLARS[p]['long']}: {len(items)} Styles Explained", f"{intro} Palettes, key pieces, tools and expert matching.", body,
           crumbs=[(pn, PILLAR_PATH[p])], priority="0.8", lastmod=TODAY.isoformat())


def page_compare():
    body = """<section class="hero" style="padding-bottom:30px"><div class="wrap">{{CRUMBS}}<span class="eyebrow">Compare</span><h1>Style vs style</h1><p class="lead">Put any two styles side by side: mood, palette, signature pieces, materials and who each suits. Great for settling “Japandi or Scandinavian?” once and for all.</p></div></section>
<section class="section" style="padding-top:30px"><div class="wrap"><div class="tool" data-tool="compare"><div class="row2" style="align-items:end"><div class="field"><label for="cmp-a">Style A</label><select id="cmp-a"></select></div><div class="field"><label for="cmp-b">Style B</label><select id="cmp-b"></select></div></div>
<p style="margin:12px 0"><button class="btn btn-ghost btn-sm" id="cmp-swap" type="button">⇄ Swap</button></p><div id="cmp-out" aria-live="polite"><p class="muted">Loading styles…</p></div></div>
<div class="prose" style="margin-top:34px"><h2>Popular comparisons</h2><ul>
<li><a href="?a=japandi&amp;b=scandinavian-interior">Japandi vs Scandinavian</a></li><li><a href="?a=modern-farmhouse&amp;b=rustic-interior">Modern Farmhouse vs Rustic</a></li><li><a href="?a=contemporary&amp;b=mid-century-modern">Contemporary vs Mid-Century Modern</a></li><li><a href="?a=old-money&amp;b=preppy">Old Money vs Preppy</a></li><li><a href="?a=dark-academia&amp;b=light-academia">Dark vs Light Academia</a></li><li><a href="?a=black-tie&amp;b=cocktail-attire">Black Tie vs Cocktail</a></li><li><a href="?a=wolf-cut&amp;b=shag">Wolf Cut vs Shag</a></li></ul>
<p>Want the written version? Read <a href="{{R}}guides/interior-styles-people-confuse/">Interior Design Styles People Confuse</a>.</p></div></div></section>"""
    layout("compare/", "Compare Styles Side by Side", "Compare any two fashion, interior, hair or occasion styles side by side: palette, pieces, materials, mood and who each suits.",
           body, crumbs=[("Compare", "compare/")], tools_js=True, priority="0.7")


def page_quiz():
    modes = "".join(f'<button class="choice" type="button" data-mode="{k}" style="border:0;background:none;padding:0;text-align:left"><span><b style="font-family:var(--serif);font-size:1.2rem">{E(v["label"])}</b><small>{ {"me": "Fashion & personal style", "home": "Interior design style", "hair": "Haircuts & makeup looks", "event": "Weddings, parties & dress codes"}[k] }</small></span></button>' for k, v in QUIZ["modes"].items())
    faqs = [["How does the Style DNA Quiz work?", "Each answer adds style traits (like minimal, cozy or bold) to your profile. We then compare your trait profile with every style's profile using cosine similarity and show your closest matches as a percentage."],
            ["Is the quiz free?", "Yes. No sign-up is needed. Your result is saved only in your browser so you can share it with a pro if you choose."],
            ["Can I take it for my home and my wardrobe?", "Yes. Pick a different mode each time; you'll also see your closest style in the other areas of life."]]
    body = f"""<section class="hero" style="padding-bottom:30px"><div class="wrap narrow">{{{{CRUMBS}}}}<span class="eyebrow">Style DNA Quiz · 2 minutes</span><h1>Which styles are yours?</h1><p class="lead">Nine quick, visual questions. You'll get your top three styles with a match score, and your closest style in every other area of life.</p></div></section>
<section class="section" style="padding-top:30px"><div class="wrap narrow"><div class="tool" data-tool="quiz">
<div id="quiz-modes"><h2 style="font-size:1.4rem">What are we styling?</h2><div class="choice-grid" style="margin-top:12px">{modes}</div></div>
<div id="quiz-run" hidden></div><div id="quiz-result" class="tool-result" aria-live="polite"></div></div>
<div class="prose" style="margin-top:34px"><h2>About the quiz</h2>{faq_html(faqs)}</div></div></section>"""
    layout("quiz/", "Style DNA Quiz: Find Your Fashion, Home & Hair Style", "Free 2-minute quiz that matches you to your top fashion, interior, hair or wedding styles with a match score. No sign-up.",
           body, crumbs=[("Style Quiz", "quiz/")], tools_js=True, schema=[faq_schema(faqs)], priority="0.9")


def page_board():
    body = """<section class="hero" style="padding-bottom:30px"><div class="wrap">{{CRUMBS}}<span class="eyebrow">My Board</span><h1>Your saved styles</h1><p class="lead">Styles you've hearted live here, on this device. Share your board with a friend, partner or your stylist.</p></div></section>
<section class="section" style="padding-top:30px"><div class="wrap"><div data-tool="board"><div id="board-out"><p class="muted">Loading…</p></div></div></div></section>"""
    layout("board/", "My Board", "Your saved All-Style styles.", body, crumbs=[("My Board", "board/")], tools_js=True, noindex=True)


def page_tools_index():
    cards = "".join(f'<a class="card tool-card" href="{{{{R}}}}tools/{t["slug"]}/"><span class="ico">{t["ico"]}</span><h3>{E(t["name"])}</h3><p class="muted small">{E(t["short"])}</p></a>' for t in TOOLS)
    extra = '<a class="card tool-card" href="{{R}}quiz/"><span class="ico">Dn</span><h3>Style DNA Quiz</h3><p class="muted small">Match your wardrobe, home, hair or event to named styles.</p></a><a class="card tool-card" href="{{R}}compare/"><span class="ico">Vs</span><h3>Style Compare</h3><p class="muted small">Any two styles, side by side.</p></a>'
    body = f"""<section class="hero" style="padding-bottom:30px"><div class="wrap">{{{{CRUMBS}}}}<span class="eyebrow">Free tools</span><h1>Style tools that do the maths</h1><p class="lead">No sign-up and no paywall. Every tool runs in your browser and nothing you enter is uploaded.</p></div></section>
<section class="section" style="padding-top:30px"><div class="wrap"><div class="grid g3">{extra}{cards}</div></div></section>"""
    layout("tools/", "Free Style Tools: Colour Season, Body Shape, Size Converter & More", "Free, private style tools: colour season finder, body and face shape calculators, size converter, capsule builder, outfit shuffler, dress code decoder and more.",
           body, crumbs=[("Tools", "tools/")], priority="0.9")


def page_tool(t):
    related = [s for s in STYLES if s["p"] == t["pillar"]][:4]
    body = f"""<section class="hero" style="padding-bottom:26px"><div class="wrap narrow">{{{{CRUMBS}}}}<span class="eyebrow">Free tool</span><h1>{E(t["name"])}</h1><p class="lead">{E(t["intro"])}</p></div></section>
<section class="section" style="padding-top:26px"><div class="wrap narrow"><div class="tool" data-tool="{t["slug"]}">{t["ui"]}</div>
<div class="prose" style="margin-top:34px"><h2>How it works</h2>{t["how"]}{ad("inarticle")}<h2>FAQ</h2>{faq_html(t["faqs"])}</div>
<h2 style="margin-top:34px">Related styles</h2><div class="grid g2">{"".join(card(s) for s in related)}</div></div></section>"""
    schema = [{"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "applicationCategory": "LifestyleApplication", "operatingSystem": "Any",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": f"{BASE}/tools/{t['slug']}/", "description": t["short"]}, faq_schema(t["faqs"])]
    layout(f"tools/{t['slug']}/", f"{t['name']} (Free, No Sign-up)", t["short"] + " Free, private and instant.", body,
           crumbs=[("Tools", "tools/"), (t["name"], f"tools/{t['slug']}/")], tools_js=True, schema=schema, priority="0.8",
           sticky=("Want a pro to do this for you?", "{{R}}get-styled/", "Get a free match"))


def page_trends():
    sections = "".join(f'<div class="card"><h3><span class="chip {p}">{E(PILLARS[p]["name"])}</span></h3>{news_html(p, 8)}</div>' for p in PORDER)
    upd = TRENDS.get("updated")
    body = f"""<section class="hero" style="padding-bottom:30px"><div class="wrap">{{{{CRUMBS}}}}<span class="eyebrow">Trend Pulse · auto-updated</span><h1>What the style world is talking about</h1>
<p class="lead">Headlines across fashion, interiors, beauty and weddings, plus the <strong>Style Heat Index</strong>: which named styles are mentioned most this week and how that's changing.</p>
<p class="small muted">{"Last refreshed " + fmt_date(upd) + " (" + ago(upd) + ")." if upd else "Refreshes automatically every six hours."} Headlines link to their original publishers.</p></div></section>
<section class="section" style="padding-top:30px"><div class="wrap layout" style="padding-top:0"><div><h2>Latest headlines</h2><div class="grid g2">{sections}</div></div>
<aside class="side"><div class="card"><h3>Style Heat Index</h3><p class="small muted">Mentions in tracked headlines, last 7 days vs the 7 before.</p>{heat_html(15)}</div>
<div class="card"><h3>How the index works</h3><p class="small">Every six hours we scan new headlines for the names and aliases of all {len(STYLES)} styles in the Atlas. Each headline counts once. It's a measure of media attention, not sales.</p></div></aside></div></section>"""
    layout("trends/", "Trend Pulse & Style Heat Index", "Auto-updated fashion, interior, beauty and wedding headlines plus the Style Heat Index ranking the most-mentioned styles this week.",
           body, crumbs=[("Trends", "trends/")], priority="0.8", lastmod=TODAY.isoformat())


def page_videos():
    blocks = ""
    for p in PORDER:
        v = videos_for(p, 9)
        inner = ('<div class="grid g3">' + video_cards(v) + "</div>") if v else yt_search_links([f"{PILLARS[p]['name']} style ideas", f"{PILLARS[p]['long']}"])
        blocks += section(E(PILLARS[p]["name"]), "", inner, alt=(p in ("home", "occasion")))
    upd = VIDEOS.get("updated")
    body = f"""<section class="hero" style="padding-bottom:30px"><div class="wrap">{{{{CRUMBS}}}}<span class="eyebrow">Video library · auto-updated</span><h1>Watch &amp; learn</h1><p class="lead">The latest uploads from respected fashion, interiors, hair and wedding channels, collected automatically. Videos play from YouTube's privacy-enhanced player only when you click.</p>
<p class="small muted">{"Last refreshed " + fmt_date(upd) + "." if upd else "Refreshes automatically every six hours."}</p></div></section>{blocks}"""
    layout("videos/", "Style Video Library", "Latest fashion, interior design, hair and wedding videos from top YouTube channels, updated automatically.", body,
           crumbs=[("Videos", "videos/")], priority="0.7", lastmod=TODAY.isoformat())


def page_daily():
    ds = daily_style()
    past = [daily_style(TODAY - dt.timedelta(days=i)) for i in range(1, 8)]
    body = f"""<section class="style-hero"><div class="wrap">{{{{CRUMBS}}}}<div class="style-hero-grid"><div><span class="eyebrow">Style of the Day · {TODAY.strftime("%A, %B %-d, %Y")}</span>
<h1 data-daily-name>{E(ds["n"])}</h1><p class="lead" data-daily-tag>{E(ds["t"])}</p><div class="palette" data-daily-pal style="margin:16px 0">{"".join(f'<span style="background:{h}"></span>' for n, h in ds["c"])}</div>
<div class="btn-row"><a class="btn btn-accent" data-daily-link data-daily-auto="{ds["s"]}" href="{{{{R}}}}styles/{ds["s"]}/">Read the full profile</a><a class="btn btn-ghost" href="{{{{R}}}}quiz/">Is it my style?</a></div></div><div class="art">{art(ds, 640, 480)}</div></div></div></section>
<section class="section"><div class="wrap"><h2>Today's three-step challenge</h2><ol class="steps">{"".join(f"<li>{E(x)}</li>" for x in ds["st"])}</ol>
<h2 style="margin-top:40px">This week's styles</h2><div class="grid g4">{"".join(card(s) for s in past[:4])}</div></div></section>"""
    layout("daily/", "Style of the Day", f"Today's featured style: {ds['n']}. A new style from the Atlas every day with a three-step challenge.", body,
           crumbs=[("Style of the Day", "daily/")], priority="0.6", lastmod=TODAY.isoformat())


def page_guides():
    cards = "".join(f'<a class="card" style="text-decoration:none" href="{{{{R}}}}guides/{g["slug"]}/"><span class="chip {g["pillar"]}">{E(PILLARS[g["pillar"]]["name"])}</span><h3 style="margin-top:10px">{E(g["title"])}</h3><p class="muted small">{E(g["desc"])}</p><span class="small muted">{g["minutes"]} min read</span></a>' for g in GUIDES)
    body = f"""<section class="hero" style="padding-bottom:30px"><div class="wrap">{{{{CRUMBS}}}}<span class="eyebrow">Guides</span><h1>Practical style guides</h1><p class="lead">Original, long-form and linked to the tools that put them into practice.</p></div></section>
<section class="section" style="padding-top:30px"><div class="wrap"><div class="grid g3">{cards}</div></div></section>"""
    layout("guides/", "Style Guides", "Practical guides to personal style, colour seasons, interior styles, capsule wardrobes, dress codes, face shapes and wedding style.",
           body, crumbs=[("Guides", "guides/")], priority="0.8")


def page_guide(g):
    toc = "".join(f'<li><a href="#s{i}">{E(s["h"])}</a></li>' for i, s in enumerate(g["sections"]))
    secs = ""
    for i, s in enumerate(g["sections"]):
        secs += f'<h2 id="s{i}">{E(s["h"])}</h2>{s["b"]}'
        if i == 2:
            secs += ad("inarticle")
    others = [x for x in GUIDES if x["slug"] != g["slug"]][:3]
    svc = SERVICE_BY_PILLAR[g["pillar"]]
    body = f"""<section class="hero" style="padding-bottom:26px"><div class="wrap narrow">{{{{CRUMBS}}}}<span class="chip {g["pillar"]}">{E(PILLARS[g["pillar"]]["name"])}</span><h1 style="margin-top:12px">{E(g["title"])}</h1><p class="lead">{E(g["desc"])}</p><p class="small muted">By the All-Style editors · {g["minutes"]} min read · Updated {dt.date.fromisoformat(LAUNCH).strftime("%B %-d, %Y")}</p></div></section>
<div class="wrap layout"><article class="prose"><nav class="card" aria-label="Contents"><strong>In this guide</strong><ol style="margin:.5em 0 0">{toc}</ol></nav>{secs}<h2>FAQ</h2>{faq_html(g["faqs"])}</article>
<aside class="side"><div class="cta-card"><h3>Prefer expert help?</h3><p>Get matched with a pro for exactly this. Free to request.</p><a class="btn" href="{{{{R}}}}get-styled/?service={svc}">Start my free match</a></div>
<div class="card"><h3>More guides</h3><ul style="padding-left:1.1em;margin:0">{"".join(f'<li><a href="{{{{R}}}}guides/{o["slug"]}/">{E(o["title"])}</a></li>' for o in others)}</ul></div></aside></div>"""
    schema = [{"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"], "author": {"@type": "Organization", "name": "All-Style"},
               "publisher": {"@type": "Organization", "name": "All-Style"}, "datePublished": LAUNCH, "dateModified": LAUNCH, "mainEntityOfPage": f"{BASE}/guides/{g['slug']}/"}, faq_schema(g["faqs"])]
    layout(f"guides/{g['slug']}/", g["title"], g["desc"], body, crumbs=[("Guides", "guides/"), (g["title"], f"guides/{g['slug']}/")], schema=schema, ogtype="article",
           sticky=("Want a pro's help with this?", f"{{{{R}}}}get-styled/?service={svc}", "Get a free match"), priority="0.8")


def page_simple(path, title, desc, body, crumbs, **kw):
    layout(path, title, desc, body, crumbs=crumbs, **kw)


def page_404():
    body = """<section class="hero"><div class="wrap narrow"><span class="eyebrow">404</span><h1>This page has gone out of style.</h1><p class="lead">The page you're looking for doesn't exist or has moved. Try search, or start from one of these:</p>
<div class="btn-row"><a class="btn" href="{{R}}">Home</a><a class="btn btn-ghost" href="{{R}}styles/">Style Atlas</a><a class="btn btn-ghost" href="{{R}}quiz/">Style Quiz</a><button class="btn btn-ghost" type="button" data-search-open>Search</button></div></div></section>"""
    layout("404.html", "Page not found", "Page not found.", body, noindex=True, absolute=True)


# ---------- non-HTML outputs ----------
def write_data():
    (ROOT / "data").mkdir(exist_ok=True)
    slim = [{k: s[k] for k in ("s", "n", "p", "t", "m", "c", "k", "mat", "st", "w", "q", "aka")} for s in STYLES]
    (ROOT / "data/styles.json").write_text(json.dumps(slim, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (ROOT / "data/quiz.json").write_text(json.dumps(QUIZ, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    idx = [{"t": s["n"], "u": f"styles/{s['s']}/", "c": PILLARS[s["p"]]["name"] + " style", "k": " ".join(s.get("aka", []) + s["m"] + [s["t"]])} for s in STYLES]
    idx += [{"t": t["name"], "u": f"tools/{t['slug']}/", "c": "Tool", "k": t["short"]} for t in TOOLS]
    idx += [{"t": g["title"], "u": f"guides/{g['slug']}/", "c": "Guide", "k": g["desc"]} for g in GUIDES]
    idx += [{"t": n, "u": u, "c": c, "k": k} for n, u, c, k in [
        ("Style DNA Quiz", "quiz/", "Tool", "quiz find my style personality"), ("Compare styles", "compare/", "Tool", "versus vs difference"),
        ("Get Styled: free pro match", "get-styled/", "Service", "stylist designer interior hire help"), ("Trend Pulse", "trends/", "Trends", "news heat index headlines"),
        ("Video library", "videos/", "Videos", "youtube watch"), ("Contests & prizes", "contests/", "Community", "win challenge enter"),
        ("Careers", "careers/", "Company", "jobs hiring write freelance"), ("Support All-Style", "support/", "Company", "donate donation"),
        ("Advertise & partner", "partners/", "Company", "sponsor advertising partnership"), ("For professionals", "pros/", "Service", "stylist designer join list business"),
        ("Contact", "contact/", "Company", "email message"), ("Style of the Day", "daily/", "Daily", "today")]]
    for p in PORDER:
        idx.append({"t": PILLARS[p]["long"], "u": PILLAR_PATH[p], "c": PILLARS[p]["name"], "k": PILLARS[p]["name"]})
    (ROOT / "data/search.json").write_text(json.dumps(idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def write_sitemap():
    seen = set()
    rows = []
    for path, lastmod, pr in SITEMAP:
        if path in seen:
            continue
        seen.add(path)
        rows.append(f"<url><loc>{BASE}/{path}</loc><lastmod>{lastmod}</lastmod><priority>{pr}</priority></url>")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /board/\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")


def write_feed():
    pub = format_datetime(dt.datetime.fromisoformat(LAUNCH + "T09:00:00+00:00"))
    items = [(g["title"], f"{BASE}/guides/{g['slug']}/", g["desc"]) for g in GUIDES] + [(f"{s['n']}: {s['t']}", f"{BASE}/styles/{s['s']}/", s["d"]) for s in STYLES]
    ds = daily_style()
    items.insert(0, (f"Style of the Day: {ds['n']}", f"{BASE}/styles/{ds['s']}/", ds["t"]))
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0"><channel>', "<title>All-Style</title>", f"<link>{BASE}/</link>",
           f"<description>{E(SITE['description'])}</description>", f"<lastBuildDate>{format_datetime(NOW)}</lastBuildDate>"]
    for t, u, d in items:
        xml.append(f"<item><title>{E(t)}</title><link>{u}</link><guid>{u}</guid><description>{E(d)}</description><pubDate>{pub}</pubDate></item>")
    xml.append("</channel></rss>")
    (ROOT / "feed.xml").write_text("\n".join(xml), encoding="utf-8")


def main():
    page_home()
    page_atlas()
    for s in STYLES:
        page_style(s)
    for p in PORDER:
        page_pillar(p)
    page_compare()
    page_quiz()
    page_board()
    page_tools_index()
    for t in TOOLS:
        page_tool(t)
    page_trends()
    page_videos()
    page_daily()
    page_guides()
    for g in GUIDES:
        page_guide(g)
    ctx = {"STYLES": STYLES, "PILLARS": PILLARS, "PORDER": PORDER, "SITE": SITE, "E": E, "theme": contest_theme(), "today": TODAY, "BY": BY}
    page_simple("get-styled/", "Get Styled: Free Match with a Stylist or Designer", "Tell us what you need and get matched with a personal stylist, colour analyst, interior designer, hair & makeup artist or wedding stylist. Free, no obligation.",
                get_styled_body(ctx), [("Get Styled", "get-styled/")], priority="0.9")
    page_simple("pros/", "For Stylists, Designers & Beauty Pros: Join the Network", "Join the All-Style Pro Network to receive matched client requests from people who love your style.",
                pros_body(ctx), [("For professionals", "pros/")], priority="0.7")
    page_simple("support/", "Support All-Style", "Help keep All-Style free and independent. Donations fund operations, promotion, new writers and contest prizes.",
                support_body(ctx), [("Support", "support/")], priority="0.6")
    page_simple("contests/", "Style Challenge: Monthly Contest & Prizes", f"This month's Style Challenge: {ctx['theme']}. Free to enter, open to adults 18+.",
                contests_body(ctx), [("Contests", "contests/")], priority="0.7", lastmod=TODAY.replace(day=1).isoformat())
    page_simple("careers/", "Careers at All-Style", "Freelance and part-time roles at All-Style: editors, interior writers, video creators, moderators, partnerships and ambassadors.",
                careers_body(ctx), [("Careers", "careers/")], priority="0.6")
    page_simple("partners/", "Advertise, Sponsor & Partner with All-Style", "Sponsorships, advertising, tool and contest sponsorship, newsletter placements and lead partnerships with All-Style.",
                partners_body(ctx), [("Partners", "partners/")], priority="0.6")
    page_simple("contact/", "Contact All-Style", "Send a message to the All-Style team.", contact_body(ctx), [("Contact", "contact/")], priority="0.5")
    for path, title, desc, body in STATIC_PAGES(ctx):
        page_simple(path, title, desc, body, [(title.split(" |")[0], path)], priority="0.3")
    page_404()
    write_data()
    write_sitemap()
    write_feed()
    print(f"Built {len(SITEMAP)} indexable pages, {len(STYLES)} styles, {len(TOOLS)} tools, {len(GUIDES)} guides.")


if __name__ == "__main__":
    main()
