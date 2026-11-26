# All-Style: The Style Atlas

Every style, decoded. A static, self-updating website that explains 65 named styles across **Wear**, **Interiors**, **Hair & Beauty** and **Occasions**, with free interactive tools, a Style DNA quiz, a pro-matching lead funnel, donations, contests, careers and partnership pages. Built for GitHub Pages (free plan, `main` branch, no build step on GitHub's side) and Google AdSense.

## Structure

| Path | What it is |
|---|---|
| `src/data/styles/*.json` | The Atlas: one entry per style (palette, pieces, materials, do/don't, steps, quiz traits) |
| `src/data/guides.json`, `quiz.json`, `site.json` | Guides, quiz questions, site settings (URL, AdSense ID, feeds, YouTube channels, contest themes, donation links, ad slots) |
| `scripts/build.py` | Renders every page into place (`index.html`, `styles/<slug>/`, `tools/<tool>/`, …) plus `sitemap.xml`, `feed.xml`, `robots.txt`, `data/*.json` |
| `scripts/update.py` | Pulls headlines (Trend Pulse), counts style mentions (Style Heat Index) and fetches the latest videos |
| `scripts/pages_tools.py`, `pages_static.py` | Tool copy/markup; lead-gen, community and legal page bodies |
| `assets/` | CSS, JS (`main.js` core, `tools.js` tools), favicon, social image |
| `.github/workflows/refresh.yml` | Runs update + build every 6 hours and on pushes, commits the result, asks Pages to rebuild |

## Run locally

```bash
python scripts/update.py   # optional: refresh headlines/videos (needs internet)
python scripts/build.py    # regenerate all pages
python -m http.server      # then open http://localhost:8000/
```

## Publishing (GitHub Pages)

Settings → Pages → Build and deployment → **Deploy from a branch** → `main` / `(root)` → Save. The site is served at `https://webworksa1.github.io/all-style/`.

**Custom domain:** add it under Settings → Pages → Custom domain, then change `"url"` in `src/data/site.json` to the new address so canonical links and the sitemap match. All internal links are relative, so the site works on a sub-path or a root domain.

## Forms

Every form (Get Styled, Pro Network, donations, contests, careers, partners, contact, newsletter) posts through FormSubmit's AJAX endpoint. The destination inbox is assembled at runtime in `assets/js/main.js` and never appears as text in the HTML. Subjects are prefixed `[All-Style]` with the form name. **The first submission triggers a one-time FormSubmit activation email; click it to start receiving submissions.**

## Monetisation settings (`src/data/site.json`)

- `adsense_client`: already set; the AdSense script is in the `<head>` of every page and `ads.txt` is in the root. Auto ads place units automatically.
- `ad_slots`: paste manual ad-unit slot IDs (`inarticle`, `display`) to add fixed units inside articles and tools.
- `donate_links`: add PayPal / Buy Me a Coffee / Stripe Payment Link URLs to show instant-pay buttons on `/support/` (pledge form works without them).
- In AdSense → Privacy & messaging, enable the certified consent message for EEA/UK visitors.

## Content rules

Original writing only; no stock or third-party photos (style art is generated from each palette). Trend Pulse shows headline titles linking to the original publishers. See `/trademark/` for the trademark and copyright disclosure.
