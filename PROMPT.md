# All-Style — Phase-wise Build Prompt

**Domain:** All-Style ("All Style") · **Repo:** `webworksa1/all-style` · **Host:** GitHub Pages (free plan, `main` branch, static)
**AdSense publisher:** `ca-pub-6620975821265271`

---

## 0. The winning idea (why this concept)

**All-Style = "The Style Atlas": every named style — fashion, interiors, hair & beauty, occasions — decoded in one place, plus free tools that tell each visitor which styles are theirs, then match them to a paid pro.**

Reasoning from the market research (40 sites read, see §9):

| Signal | Evidence | Decision |
|---|---|---|
| "What style is this / what's my style?" is a huge evergreen query class | Aesthetics Wiki, Dictionary.com, Who What Wear, Apartment Therapy, Houzz, Homedit, HGTV, Wayfair all publish style glossaries | Programmatic **Style Atlas** (one deep page per style) = long-tail SEO engine |
| Home out-earns fashion per click | Google Ads benchmarks: Home & Home Improvement ≈ $7.85 avg CPC vs Apparel/Fashion ≈ $4.31; Furniture cost-per-lead ≈ $121 | **Home pillar gets the most depth**; fashion is the traffic pillar |
| Quizzes convert to leads | Havenly, Stitch Fix, The Knot all run quiz → match → pro. The Knot reported +10.3% lead submissions from style-matched picks + a visible match score | **Style DNA quiz with a visible match %** feeding the lead form |
| Free, no-signup tools win traffic | discoverfashions.com runs 15+ free style tools with ads + affiliate | 10 free tools, no login, in-browser |
| Pros pay for clients | Thumbtack stylist listings ($297–$397 packages), StyleSeat, Houzz, WeddingWire premium listings | **Pro Network** form (B2B lead + future listing fees) |
| Trend rankings get press & return visits | Lyst Index (quarterly), Pinterest Predicts | **Style Heat Index** computed automatically from headline mentions |

Revenue stack: AdSense (Auto ads) → lead gen (consumer "Get Styled" + pro network) → sponsorships (tool/page/contest/newsletter) → donations → affiliate later.

---

## Phase 1 — Foundation & compliance (build first)

1. Static site, no framework, works from a sub-path (`/all-style/`) **and** a custom domain root → every internal link is relative; one `SITE_URL` setting for canonicals.
2. Generator: `scripts/build.py` renders every page from `src/data/*.json` (single source of truth). `.nojekyll`, `404.html`, `robots.txt`, `sitemap.xml`, `feed.xml`, `ads.txt` (`google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`), `manifest.webmanifest`, SVG favicon.
3. `<head>` of every page: AdSense script exactly as supplied, canonical, meta description, Open Graph/Twitter, JSON-LD (WebSite + SearchAction, Organization, BreadcrumbList; Article/FAQPage where relevant).
4. **Top bar on every page:** "Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership" → links to the owner's contact page; the destination URL is never printed as visible text.
5. **One inbox, never exposed:** every form posts through FormSubmit's AJAX endpoint; the address is assembled in JavaScript from an encoded array, never present as plain text in HTML. Subject lines prefixed `[All-Style]` + form name.
6. Legal set for AdSense approval: About (with editorial policy), Contact (form), Privacy (Google/DoubleClick cookies, third-party vendors, opt-out links, FormSubmit, YouTube, localStorage), Terms, Cookies, Disclaimer, **Trademark & Copyright disclosure** (independent publication; not affiliated with Gildan's Alstyle® apparel marks or any "Allstyle/All Style" business; all trademarks belong to their owners; no third-party photos).
7. Cookie banner (accept / necessary-only → `requestNonPersonalizedAds`), prepared for Google's certified CMP in AdSense "Privacy & messaging".

## Phase 2 — Design system

- Editorial look: warm paper background, ink text, terracotta accent; serif display (Fraunces) + sans body (Inter); light/dark mode.
- **No stock or scraped photos.** Every style gets a generated swatch card (its 5-colour palette rendered as a layered SVG/CSS composition) → unique visuals, zero copyright risk.
- Mobile-first grid, sticky header, search overlay (`/` shortcut), focus states, skip link, reduced-motion support, Lighthouse-friendly (no frameworks, lazy video).

## Phase 3 — Core content: the Style Atlas

- 60+ entries across 4 pillars: **Wear** (Old Money, Japandi-adjacent minimalism, Dark Academia, Streetwear, Gorpcore…), **Home** (Japandi, Mid-Century Modern, Modern Farmhouse, Wabi-Sabi, Art Deco…), **Hair & Beauty** (Wolf Cut, Curtain Bangs, Taper Fade…), **Occasions** (White Tie, Black Tie, Cocktail, wedding styles…).
- Fixed template per style (borrowed from Aesthetics Wiki + Houzz + Apartment Therapy patterns): tagline, what it is, origins, mood, palette with hex codes, signature elements, materials, do/don't, "works well with", start-in-3-steps, budget tip, who it suits, FAQ (FAQPage schema), related styles, compare links, **pro CTA prefilled with the style**.
- Atlas index with pillar filters + live search; **Compare tool** (any style vs any style); **My Board** (save styles locally).
- Long-form original guides (find your style, colour seasons, interior styles that get confused, capsule formula, dress codes, face shapes, wedding style).

## Phase 4 — Interactive tools (traffic engine)

Style DNA Quiz (4 modes: me / my home / my hair / my event; cosine-similarity match %), Colour Season Finder (12 seasons), Body Shape Calculator (women + men, cm/in), Face Shape Finder, Size Converter (clothing + shoes), Capsule Wardrobe Builder (printable checklist), Outfit Shuffler ("dress me" with locks), Dress Code Decoder, Room Palette Generator (60-30-10, analogous, complementary, triadic), Makeover Budget Planner (allocates the user's own budget). Every tool page carries explanatory copy so it is never a thin page.

## Phase 5 — Lead generation (money engine)

- `/get-styled/`: 4-step form with progress bar — service (personal styling, colour analysis, wardrobe edit, interior design room / full home, hair & makeup, wedding/event styling) → styles + budget + timeline + online/in-person + location → contact → consent. Prefills from quiz/style pages via URL params; shows the visitor's match summary.
- Sticky CTA on every style page and tool result ("Love Japandi? Get a free plan from a matched designer").
- `/pros/`: Pro Network application for stylists, interior designers, salons, makeup artists, wedding planners (services, regions, plan interest: free listing / featured / exclusive leads).
- Newsletter ("Weekly Style Brief") in footer of every page.

## Phase 6 — Community & money pages

- `/support/`: donation tiers + allocation (operations, promotions & marketing, hiring talent, contests & prizes) + pledge form; optional PayPal / Buy Me a Coffee / Stripe links switch on from one config file.
- `/contests/`: monthly Style Challenge (theme rotates automatically), official rules (no purchase necessary, 18+, judging criteria), entry form, "sponsor a prize" CTA.
- `/careers/`: freelance editors, interior writer, video creator, community moderator, partnerships (commission), ambassadors; application form.
- `/partners/`: sponsored style page, tool sponsorship, newsletter, contest sponsorship, regional lead partnerships, domain/website acquisition inquiries; inquiry form.

## Phase 7 — Self-updating automation

- `scripts/update.py` (GitHub Actions, every 6 h): pulls Google News RSS per pillar → **Trend Pulse** headlines; resolves curated YouTube channel handles → channel RSS → **Video Library**; counts style-name mentions → **Style Heat Index** (7-day rolling, change vs prior week).
- `scripts/build.py` re-renders every page (Style of the Day rotates daily, contest theme monthly, sitemap `lastmod`, RSS feed), then the workflow commits to `main` and requests a Pages build.
- Every data feed degrades gracefully (empty state + YouTube search links) so a failed fetch never breaks a page.

## Phase 8 — QA, launch, AdSense submission

1. Link check (no broken internal links), HTML sanity, mobile screenshots, dark mode check.
2. Grep the build: the inbox address must not appear in plain text anywhere; the owner's contact URL appears only inside link `href`s, never as visible text.
3. Push to `main`, publish GitHub Pages (Settings → Pages → Deploy from branch → `main` / root).
4. Submit the first form yourself to activate FormSubmit.
5. AdSense → Sites → add the domain → paste-verified script already present → ads.txt live → request review. Enable Auto ads + certified CMP.

## Phase 9 — Research log (sites read for this build)

Who What Wear · Fashion Gone Rogue · Aesthetics Wiki · Dictionary.com (Gen Z aesthetics) · Havenly · Houzz · Apartment Therapy · Homedit · The VOU · DiscoverFashions · Une Femme · The Right Hairstyles · MensHairCuts · Man of Many · Real Men Real Style · Gentleman's Gazette · He Spoke Style · Suits Expert · Art of Manliness · The Knot (+ marketplace, + The Knot Worldwide tech blog) · WeddingWire · Stitch Fix · Stylist (UK) / Whering · Archute · Thumbtack · The Zoe Report · Woman & Home · Sterling Style Academy · Curbly · Lyst (The Lyst Index) · The Business of Fashion · Pinterest Predicts · HGTV · Wayfair Ideas & Advice · StyleCraze · Latest-Hairstyles · StyleSeat · Primer · House Digest · Joss & Main.

What was taken from them: structured per-style templates (Aesthetics Wiki, Houzz "works well with", Apartment Therapy "X vs Y"), quiz → match → pro funnels (Havenly, Stitch Fix, The Knot), no-signup tool suites (DiscoverFashions), ranking indexes (Lyst, Pinterest Predicts), pro marketplaces (Thumbtack, StyleSeat, WeddingWire), job boards (BoF Careers), sweepstakes/contests (HGTV, Pinterest), newsletter-everywhere (every publisher), affiliate & advertiser disclosures (Who What Wear, Man of Many, Primer).
