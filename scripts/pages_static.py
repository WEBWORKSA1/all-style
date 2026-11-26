"""Bodies for lead-gen, community, company and legal pages. {{R}} is replaced with the relative root."""
import datetime as dt
import calendar

HP = '<input class="hp" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
EFFECTIVE = "November 26, 2026"


def _hero(eyebrow, h1, lead, extra=""):
    return (f'<section class="hero" style="padding-bottom:30px"><div class="wrap">{{{{CRUMBS}}}}<span class="eyebrow">{eyebrow}</span>'
            f'<h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div></section>')


def _consent(label="I agree to be contacted about this request and accept the <a href=\"{{R}}privacy/\">privacy policy</a>."):
    return f'<label class="check"><input type="checkbox" name="consent" value="yes" required> <span>{label}</span></label>'


def _done(title, text, links=""):
    return (f'<div class="success-panel" hidden id="{{ID}}"><div class="big">{title}</div><p class="lead" style="margin:0 auto 16px">{text}</p>'
            f'<div class="btn-row" style="justify-content:center">{links}</div></div>')


SERVICES = [
    ("personal-styling", "Personal styling", "Wardrobe, shopping, a new look"),
    ("color-analysis", "Colour analysis", "Find your seasonal palette"),
    ("wardrobe-edit", "Wardrobe edit & capsule", "Declutter and build a capsule"),
    ("interior-room", "Interior design: one room", "Living, bedroom, office…"),
    ("interior-home", "Interior design: full home", "Several rooms or a move"),
    ("hair-makeup", "Hair & makeup", "New cut, colour or event look"),
    ("wedding-styling", "Wedding styling & planning", "Look, palette, vendors"),
    ("event-styling", "Event outfit styling", "Gala, interview, party"),
]


def get_styled_body(c):
    E, S, P, PO = c["E"], c["STYLES"], c["PILLARS"], c["PORDER"]
    svc = "".join(f'<label class="choice"><input type="radio" name="service" value="{k}" required><span>{E(n)}<small>{E(d)}</small></span></label>' for k, n, d in SERVICES)
    chips = ""
    for i, p in enumerate(PO):
        chips += (f'<details{" open" if i == 0 else ""} style="margin-bottom:8px"><summary style="cursor:pointer;font-weight:600">{E(P[p]["name"])}</summary><div class="chips" style="margin-top:8px">' +
                  "".join(f'<label><input type="checkbox" name="styles" value="{s["s"]}"><span>{E(s["n"])}</span></label>' for s in S if s["p"] == p) + "</div></details>")
    done = _done("Request received.", "Thank you. We'll review your brief and reply by email, usually within two business days, with your matched professional(s).",
                 '<a class="btn" href="{{R}}quiz/">Take the Style DNA Quiz</a><a class="btn btn-ghost" href="{{R}}styles/">Explore the Atlas</a>').replace("{ID}", "gs-done")
    return _hero("Get Styled · free to request · no obligation", "Get matched with a pro who gets your style",
                 "Personal stylists, colour analysts, interior designers, hair &amp; makeup artists and wedding stylists. Tell us what you need in under two minutes; we'll match you by style, budget and location.",
                 '<div class="logo-strip" style="margin-top:14px"><span>✓ Free to request</span><span>✓ Matched to your style &amp; budget</span><span>✓ Online or in person</span><span>✓ Your details shared only with your matches</span></div>') + f"""
<div class="wrap layout"><div>
<form class="tool form" id="gs" data-form="Get Styled lead" data-steps data-prefill data-done="#gs-done" novalidate>
<div class="small muted" data-step-label>Step 1 of 4</div><div class="progress"><i></i></div>
<div class="step-panel"><span class="legend" style="font:500 1.4rem/1.2 var(--serif)">What do you need help with?</span><div class="choice-grid">{svc}</div>
<div class="btn-row"><button class="btn btn-accent" type="button" data-next>Continue</button></div></div>
<div class="step-panel"><span class="legend" style="font:500 1.4rem/1.2 var(--serif)">Your style, budget and timing</span>
<p class="note" data-quiz-note hidden></p>
<div class="field"><span class="legend">Styles you love <span class="muted small">(optional, pick any)</span></span>{chips}<a class="small" href="{{{{R}}}}quiz/">Not sure? Take the 2-minute quiz first →</a></div>
<div class="row2"><div class="field"><label for="gs-budget">Budget</label><select id="gs-budget" name="budget_range" required><option value="">Choose…</option><option>Under $250</option><option>$250–$1,000</option><option>$1,000–$5,000</option><option>$5,000–$15,000</option><option>$15,000–$50,000</option><option>$50,000+</option><option>Not sure yet</option></select></div>
<div class="field"><label for="gs-time">Timeline</label><select id="gs-time" name="timeline" required><option value="">Choose…</option><option>As soon as possible</option><option>Within a month</option><option>1–3 months</option><option>3–6 months</option><option>Just exploring</option></select></div></div>
<div class="row2"><div class="field"><label for="gs-format">Format</label><select id="gs-format" name="format"><option>Online or in person</option><option>Online only</option><option>In person only</option></select></div>
<div class="field"><label for="gs-loc">City &amp; country</label><input id="gs-loc" name="location" required placeholder="e.g. Toronto, Canada" autocomplete="address-level2"></div></div>
<div class="btn-row"><button class="btn btn-ghost" type="button" data-prev>Back</button><button class="btn btn-accent" type="button" data-next>Continue</button></div></div>
<div class="step-panel"><span class="legend" style="font:500 1.4rem/1.2 var(--serif)">How can your pro reach you?</span>
<div class="row2"><div class="field"><label for="gs-name">Your name</label><input id="gs-name" name="name" required autocomplete="name"></div><div class="field"><label for="gs-email">Email</label><input id="gs-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="row2"><div class="field"><label for="gs-phone">Phone / WhatsApp <span class="muted small">(optional)</span></label><input id="gs-phone" type="tel" name="phone" autocomplete="tel"></div><div class="field"><label for="gs-pref">Preferred contact</label><select id="gs-pref" name="contact_preference"><option>Email</option><option>Phone</option><option>WhatsApp</option></select></div></div>
<div class="field"><label for="gs-msg">Tell us about your project</label><textarea id="gs-msg" name="message" placeholder="e.g. Moving into a 2-bed condo, want a calm Japandi living room by spring; budget flexible for the sofa."></textarea></div>
<div class="btn-row"><button class="btn btn-ghost" type="button" data-prev>Back</button><button class="btn btn-accent" type="button" data-next>Continue</button></div></div>
<div class="step-panel"><span class="legend" style="font:500 1.4rem/1.2 var(--serif)">Last step</span>
<p>We'll match you with up to three professionals who work in your style and budget. You decide whether to go ahead; there's no cost or obligation to request.</p>
{_consent('I agree to be contacted about my request and to my details being shared with up to three matched professionals, as described in the <a href="{{R}}privacy/">privacy policy</a>.')}
<label class="check"><input type="checkbox" name="newsletter" value="yes"> <span>Also send me the Weekly Style Brief (optional).</span></label>
<input type="hidden" name="style_dna" value=""><input type="hidden" name="budget" value=""><input type="hidden" name="lead_source" value="get-styled">{HP}
<div class="btn-row"><button class="btn btn-ghost" type="button" data-prev>Back</button><button class="btn btn-accent" type="submit">Send my request</button></div></div>
</form>{done}</div>
<aside class="side"><div class="card"><h3>How it works</h3><ol class="steps"><li>Tell us what you need and the styles you love.</li><li>We match you with pros who specialise in that style, budget and location.</li><li>Compare, chat and choose. No pressure, no fees to request.</li></ol></div>
<div class="card"><h3>Typical requests</h3><ul class="ticks small"><li>A Japandi living room for a rental</li><li>Colour analysis before a wardrobe refresh</li><li>Capsule wardrobe for a new job</li><li>Boho wedding styling and palette</li><li>A low-maintenance haircut for curly hair</li></ul></div>
<div class="card"><h3>Are you a pro?</h3><p class="small muted">Stylists, designers and beauty pros can join the network.</p><a class="btn btn-sm" href="{{{{R}}}}pros/">Join the Pro Network</a></div></aside></div>"""


def pros_body(c):
    E = c["E"]
    done = _done("Application received.", "Thanks for applying to the All-Style Pro Network. We'll review your profile and reply by email.", '<a class="btn" href="{{R}}styles/">Explore the Atlas</a>').replace("{ID}", "pro-done")
    services = "".join(f'<label><input type="checkbox" name="services" value="{E(n)}"><span>{E(n)}</span></label>' for k, n, d in SERVICES)
    return _hero("Pro Network", "Get clients who already love your style",
                 "All-Style readers arrive knowing exactly which style they want. Join the network to receive matched requests from people looking for a stylist, designer or beauty pro in your speciality.") + f"""
<section class="section" style="padding-top:20px"><div class="wrap"><div class="grid g4">
<div class="card"><h3>Style-matched requests</h3><p class="muted small">Every request includes the client's chosen styles, budget, timeline and location.</p></div>
<div class="card"><h3>Pre-qualified intent</h3><p class="muted small">Requests come from quiz-takers and style-page readers who've already defined what they want.</p></div>
<div class="card"><h3>Visibility on style pages</h3><p class="muted small">Featured pros can be highlighted on the Atlas pages for their specialities.</p></div>
<div class="card"><h3>Fair, transparent plans</h3><p class="muted small">Start free. Upgrade to featured or exclusive-area plans only if it works for you.</p></div></div>
<h2 style="margin-top:46px">Plans</h2><div class="table-wrap"><table><thead><tr><th></th><th>Free listing</th><th>Featured</th><th>Exclusive area</th></tr></thead><tbody>
<tr><th>Matched requests</th><td>Standard</td><td>Priority</td><td>Exclusive in your city &amp; speciality</td></tr>
<tr><th>Feature on style pages</th><td>—</td><td>✓</td><td>✓</td></tr><tr><th>Contest &amp; newsletter features</th><td>—</td><td>Occasional</td><td>✓</td></tr>
<tr><th>Price</th><td>$0</td><td colspan="2">Shared on application, based on your market</td></tr></tbody></table></div></div></section>
<section class="section section-alt"><div class="wrap narrow"><h2>Apply to join</h2>
<form class="form" id="pro-form" data-form="Pro Network application" data-done="#pro-done" novalidate>
<div class="row2"><div class="field"><label for="p-biz">Business name</label><input id="p-biz" name="business" required></div><div class="field"><label for="p-name">Your name</label><input id="p-name" name="name" required autocomplete="name"></div></div>
<div class="row2"><div class="field"><label for="p-email">Email</label><input id="p-email" type="email" name="email" required autocomplete="email"></div><div class="field"><label for="p-phone">Phone <span class="muted small">(optional)</span></label><input id="p-phone" type="tel" name="phone"></div></div>
<div class="row2"><div class="field"><label for="p-prof">Profession</label><select id="p-prof" name="profession" required><option value="">Choose…</option><option>Personal stylist</option><option>Image consultant / colour analyst</option><option>Interior designer / decorator</option><option>Home stager</option><option>Hairstylist / barber</option><option>Makeup artist</option><option>Wedding planner / stylist</option><option>Photographer</option><option>Other</option></select></div>
<div class="field"><label for="p-web">Website or Instagram</label><input id="p-web" name="website" required placeholder="https://"></div></div>
<div class="field"><span class="legend">Services you offer</span><div class="chips">{services}</div></div>
<div class="row2"><div class="field"><label for="p-styles">Styles you specialise in</label><input id="p-styles" name="specialties" placeholder="e.g. Japandi, Modern Organic"></div><div class="field"><label for="p-area">Cities / regions served</label><input id="p-area" name="regions" required placeholder="e.g. Montréal + online"></div></div>
<div class="row2"><div class="field"><label for="p-years">Years of experience</label><select id="p-years" name="experience"><option>0–2</option><option>3–5</option><option>6–10</option><option>10+</option></select></div>
<div class="field"><label for="p-plan">Plan interest</label><select id="p-plan" name="plan"><option>Free listing</option><option>Featured</option><option>Exclusive area</option><option>Not sure yet</option></select></div></div>
<div class="field"><label for="p-msg">Anything else?</label><textarea id="p-msg" name="message"></textarea></div>
{_consent()}{HP}<button class="btn btn-accent" type="submit">Apply to join</button></form>{done}</div></section>"""


def support_body(c):
    links = c["SITE"].get("donate_links", {})
    pay = "".join(f'<a class="btn" href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in [("Donate with PayPal", links.get("paypal")), ("Buy us a coffee", links.get("buymeacoffee")), ("Card (Stripe)", links.get("stripe"))] if u)
    pay_block = f'<div class="btn-row" style="margin:18px 0">{pay}</div>' if pay else ""
    alloc = [("Operations & hosting", 30), ("Promotions & marketing", 25), ("Hiring writers & creators", 25), ("Contests & prizes", 20)]
    done = _done("Thank you!", "We've received your pledge. We'll email you a secure payment link and a receipt for your records.", '<a class="btn" href="{{R}}">Back to All-Style</a>').replace("{ID}", "don-done")
    return _hero("Support", "Keep All-Style free, independent and growing",
                 "All-Style is free to read and every tool is free to use. Supporter contributions pay for running the site, promoting it, hiring writers and creators, and funding contest prizes.") + f"""
<section class="section" style="padding-top:20px"><div class="wrap"><div class="grid g4">
<div class="card tier"><span class="chip">One-time</span><div class="price">$5</div><h3>Coffee</h3><p class="muted small">Covers a day of hosting and data refreshes.</p></div>
<div class="card tier"><span class="chip">Monthly</span><div class="price">$15</div><h3>Supporter</h3><p class="muted small">Funds a new Atlas entry every month.</p></div>
<div class="card tier"><span class="chip">Monthly</span><div class="price">$50</div><h3>Patron</h3><p class="muted small">Sponsors a contest prize and gets a thank-you in the Weekly Style Brief.</p></div>
<div class="card tier"><span class="chip">One-time</span><div class="price">$250+</div><h3>Founding Partner</h3><p class="muted small">Named on the About page (optional) and helps hire our next writer.</p></div></div>
<div class="grid g2" style="margin-top:40px;align-items:start"><div><h2>Where your money goes</h2><div class="alloc">{"".join(f'<div><span>{n}</span><div class="meter"><i style="width:{p}%"></i></div><strong>{p}%</strong></div>' for n, p in alloc)}</div>
<p class="small muted" style="margin-top:14px">Target allocation of general donations. You can direct your gift to one area in the form. All-Style is not a registered charity; donations are not tax-deductible.</p>{pay_block}</div>
<div class="card"><h2 style="font-size:1.5rem">Make a pledge</h2><p class="small muted">Choose an amount and we'll email you a secure payment link. No card details are collected on this page.</p>
<form class="form" data-form="Donation pledge" data-done="#don-done" novalidate>
<div class="row2"><div class="field"><label for="d-amt">Amount</label><input id="d-amt" type="number" name="amount" min="1" step="1" required value="15"></div><div class="field"><label for="d-cur">Currency</label><select id="d-cur" name="currency"><option>USD</option><option>CAD</option><option>EUR</option><option>GBP</option><option>INR</option><option>AUD</option></select></div></div>
<div class="row2"><div class="field"><label for="d-freq">Frequency</label><select id="d-freq" name="frequency"><option>One-time</option><option>Monthly</option></select></div><div class="field"><label for="d-alloc">Direct my gift to</label><select id="d-alloc" name="allocation"><option>Wherever it's needed most</option><option>Operations &amp; hosting</option><option>Promotions &amp; marketing</option><option>Hiring talent</option><option>Contests &amp; prizes</option></select></div></div>
<div class="row2"><div class="field"><label for="d-name">Name</label><input id="d-name" name="name" required autocomplete="name"></div><div class="field"><label for="d-email">Email</label><input id="d-email" type="email" name="email" required autocomplete="email"></div></div>
<label class="check"><input type="checkbox" name="public_thanks" value="yes"> <span>You may thank me publicly by first name.</span></label>
<div class="field"><label for="d-msg">Message <span class="muted small">(optional)</span></label><textarea id="d-msg" name="message" style="min-height:80px"></textarea></div>
{_consent()}{HP}<button class="btn btn-accent" type="submit">Send my pledge</button></form>{done}</div></div></div></section>"""


def contests_body(c):
    E, today, theme, themes = c["E"], c["today"], c["theme"], c["SITE"]["contest_themes"]
    last_day = calendar.monthrange(today.year, today.month)[1]
    close = today.replace(day=min(25, last_day))
    nxt = (today.replace(day=1) + dt.timedelta(days=32)).replace(day=5)
    past = [themes[(today.month - 1 - i) % 12] for i in range(1, 4)]
    upcoming = [themes[(today.month - 1 + i) % 12] for i in range(1, 3)]
    done = _done("You're in!", "Your entry has been received. Winners are announced on this page and in the Weekly Style Brief.", '<a class="btn" href="{{R}}styles/">Get inspired in the Atlas</a>').replace("{ID}", "ct-done")
    return _hero(f"Style Challenge · {today.strftime('%B %Y')}", E(theme),
                 f"Free to enter. Style it, share a link to your photo or post, and tell us how you did it. Entries close <strong>{close.strftime('%B %-d')}</strong>; winners are announced by <strong>{nxt.strftime('%B %-d')}</strong>.") + f"""
<section class="section" style="padding-top:20px"><div class="wrap"><div class="grid g3">
<div class="card"><h3>1. Create</h3><p class="muted small">Style an outfit, a room, a corner or a look that fits this month's theme. Use any budget.</p></div>
<div class="card"><h3>2. Share</h3><p class="muted small">Post it anywhere public (Instagram, TikTok, Pinterest, a blog or a cloud photo link).</p></div>
<div class="card"><h3>3. Enter</h3><p class="muted small">Submit the link below with a short note on your choices. One entry per person per month.</p></div></div>
<div class="grid g2" style="margin-top:40px;align-items:start"><div>
<h2>Prizes</h2><p>Winners are featured on the All-Style homepage, this page and the Weekly Style Brief. Monthly prize packages are funded by <a href="{{{{R}}}}partners/">sponsors</a> and <a href="{{{{R}}}}support/">supporters</a>; when a sponsor prize is confirmed it is listed here before entries close.</p>
<h2>Judging</h2><div class="alloc">{"".join(f'<div><span>{n}</span><div class="meter"><i style="width:{p * 2.5}%"></i></div><strong>{p}%</strong></div>' for n, p in [("Fit to theme & style coherence", 40), ("Creativity", 30), ("Practicality & budget", 20), ("Your story", 10)])}</div>
<h2 style="margin-top:28px">Coming up</h2><ul>{"".join(f"<li>{E(t)}</li>" for t in upcoming)}</ul>
<h2>Previous themes</h2><ul>{"".join(f"<li>{E(t)}</li>" for t in past)}</ul>
<div class="cta-card" style="margin-top:20px"><h3>Sponsor a prize</h3><p>Put your brand in front of an engaged, style-focused audience.</p><a class="btn" href="{{{{R}}}}partners/">Sponsor a contest</a></div></div>
<div class="card"><h2 style="font-size:1.5rem">Enter this month</h2>
<form class="form" data-form="Contest entry" data-done="#ct-done" novalidate><input type="hidden" name="contest" value="{E(theme)} ({today.strftime('%B %Y')})">
<div class="row2"><div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required autocomplete="name"></div><div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="row2"><div class="field"><label for="c-country">Country</label><input id="c-country" name="country" required autocomplete="country-name"></div><div class="field"><label for="c-cat">Category</label><select id="c-cat" name="category"><option>Wear</option><option>Home</option><option>Hair &amp; Beauty</option><option>Occasions</option></select></div></div>
<div class="field"><label for="c-link">Link to your photo or post</label><input id="c-link" type="url" name="entry_link" required placeholder="https://"></div>
<div class="field"><label for="c-title">Entry title</label><input id="c-title" name="entry_title" required maxlength="80"></div>
<div class="field"><label for="c-desc">How you styled it</label><textarea id="c-desc" name="description" required maxlength="800"></textarea></div>
<label class="check"><input type="checkbox" name="age_18" value="yes" required> <span>I am 18 or older and the entry is my own work.</span></label>
<label class="check"><input type="checkbox" name="rules" value="accepted" required> <span>I accept the official rules below and allow All-Style to feature my entry with credit.</span></label>{HP}
<button class="btn btn-accent" type="submit">Submit my entry</button></form>{done}</div></div>
<div class="prose" style="margin-top:46px"><h2>Official rules (summary)</h2><ol>
<li><strong>No purchase necessary.</strong> Entry is free. A purchase does not improve your chances.</li>
<li><strong>Eligibility:</strong> open to individuals aged 18+ where such contests are lawful. Void where prohibited. Employees of sponsors are not eligible for that sponsor's prize.</li>
<li><strong>Entry period:</strong> from the 1st of the month until 23:59 UTC on the closing date shown above. One entry per person per month.</li>
<li><strong>Judging:</strong> by the All-Style editors using the published criteria. Decisions are final.</li>
<li><strong>Your content:</strong> you keep ownership. You grant All-Style a non-exclusive licence to display your entry with credit on the site, newsletter and social channels. Entries must be your own work and must not infringe anyone's rights or include anyone under 18 without guardian consent.</li>
<li><strong>Prizes:</strong> as listed on this page before entries close; non-transferable; no cash alternative unless stated. Winners are contacted by email and must reply within 14 days. Winners are responsible for any taxes.</li>
<li><strong>Privacy:</strong> entry details are used only to run the contest, as described in our <a href="{{{{R}}}}privacy/">privacy policy</a>.</li></ol></div></div></section>"""


ROLES = [
    ("Contributing Style Editor", "Freelance · Remote", "Research and write new Atlas entries and guides in fashion and beauty. Strong, original writing and a sharp eye for detail."),
    ("Interior Style Writer", "Freelance · Remote", "Write and update interior style profiles, comparisons and room guides. Design background or deep interest required."),
    ("Short-form Video Creator", "Freelance · Remote", "Turn Atlas entries into 30–60 second videos for Shorts, Reels and TikTok. Editing and on-camera confidence a plus."),
    ("Community & Contest Moderator", "Part-time · Remote", "Run the monthly Style Challenge: review entries, coordinate judging and keep the community friendly."),
    ("Partnerships & Ad Sales", "Commission-based · Remote", "Bring in sponsors, brand partners and pro-network members. Experience selling to fashion, beauty or home brands preferred."),
    ("Style Ambassador", "Volunteer / perks · Anywhere", "Share All-Style with your community, test new tools and feature in our Ambassador spotlight."),
]


def careers_body(c):
    E = c["E"]
    roles = "".join(f'<div class="card"><span class="badge">{E(t)}</span><h3 style="margin-top:10px">{E(n)}</h3><p class="muted small">{E(d)}</p><a class="btn btn-sm btn-ghost" href="#apply" onclick="document.getElementById(\'job-role\').value=\'{E(n)}\'">Apply</a></div>' for n, t, d in ROLES)
    opts = "".join(f"<option>{E(n)}</option>" for n, t, d in ROLES)
    done = _done("Application received.", "Thank you for applying. If there's a fit, we'll be in touch by email.", '<a class="btn" href="{{R}}">Back to All-Style</a>').replace("{ID}", "job-done")
    return _hero("Careers", "Help decode every style",
                 "All-Style is growing. We work remotely with freelancers and part-timers who love style, write clearly and care about getting details right. Supporter donations help fund these roles.") + f"""
<section class="section" style="padding-top:20px"><div class="wrap"><div class="grid g3">{roles}</div>
<div class="grid g2" style="margin-top:46px;align-items:start"><div class="prose"><h2>How we work</h2><ul><li>Remote-first, asynchronous, outcome-focused.</li><li>Original work only: no copied text, no unlicensed images.</li><li>Fair, agreed rates per piece or per month, paid on time.</li><li>We credit our contributors by name.</li></ul>
<h2>Don't see your role?</h2><p>Send a general application. We're always interested in photographers, illustrators, developers and stylists.</p></div>
<div class="card" id="apply"><h2 style="font-size:1.5rem">Apply</h2><form class="form" data-form="Job application" data-done="#job-done" novalidate>
<div class="field"><label for="job-role">Role</label><select id="job-role" name="role" required>{opts}<option>General application</option></select></div>
<div class="row2"><div class="field"><label for="j-name">Name</label><input id="j-name" name="name" required autocomplete="name"></div><div class="field"><label for="j-email">Email</label><input id="j-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="row2"><div class="field"><label for="j-loc">Location / time zone</label><input id="j-loc" name="location" required></div><div class="field"><label for="j-avail">Availability</label><select id="j-avail" name="availability"><option>A few hours a week</option><option>10–20 hours a week</option><option>20+ hours a week</option><option>Project-based</option></select></div></div>
<div class="field"><label for="j-port">Portfolio, LinkedIn or samples</label><input id="j-port" type="url" name="portfolio" required placeholder="https://"></div>
<div class="field"><label for="j-msg">Why you, in a few lines</label><textarea id="j-msg" name="message" required></textarea></div>
{_consent()}{HP}<button class="btn btn-accent" type="submit">Send application</button></form>{done}</div></div></div></section>"""


def partners_body(c):
    pk = [("Sponsored style page", "Your brand presented on a relevant Atlas entry (clearly labelled as sponsored), with a link and a short brand story."),
          ("Tool sponsorship", "“Presented by” placement on a tool such as the Colour Season Finder or Makeover Budget Planner."),
          ("Weekly Style Brief", "Newsletter placements reaching readers who opted in to style content."),
          ("Contest sponsorship", "Fund a monthly Style Challenge prize; your brand features on the contest page, entries and winners' announcement."),
          ("Lead partnerships", "Receive style-matched consumer requests in your city and speciality (interiors, styling, beauty, weddings)."),
          ("Custom & affiliate", "Content partnerships, affiliate programmes and bespoke campaigns that fit our editorial standards.")]
    done = _done("Thanks, we'll be in touch.", "We've received your enquiry and will reply by email with options and availability.", '<a class="btn" href="{{R}}">Back to All-Style</a>').replace("{ID}", "pt-done")
    return _hero("Advertise &amp; partner", "Reach people at the moment they choose their style",
                 "All-Style readers are actively deciding what to wear, how to decorate and how to celebrate. Partner with us through clearly labelled sponsorships, tools, contests, newsletter placements and lead partnerships.") + f"""
<section class="section" style="padding-top:20px"><div class="wrap"><div class="grid g3">{"".join(f'<div class="card"><h3>{n}</h3><p class="muted small">{d}</p></div>' for n, d in pk)}</div>
<div class="grid g2" style="margin-top:46px;align-items:start"><div class="prose"><h2>Our standards</h2><ul><li>Sponsored content is always labelled.</li><li>We don't sell editorial verdicts; our style profiles stay independent.</li><li>No misleading claims, no prohibited products, Google publisher-policy compliant.</li></ul>
<h2>Acquisition &amp; strategic partnerships</h2><p>Interested in this website, the domain name or a strategic partnership? Use the contact link at the very top of any page, or select it in the form.</p></div>
<div class="card"><h2 style="font-size:1.5rem">Partnership enquiry</h2><form class="form" data-form="Partnership enquiry" data-done="#pt-done" novalidate>
<div class="row2"><div class="field"><label for="pt-co">Company</label><input id="pt-co" name="company" required></div><div class="field"><label for="pt-name">Your name</label><input id="pt-name" name="name" required autocomplete="name"></div></div>
<div class="row2"><div class="field"><label for="pt-email">Work email</label><input id="pt-email" type="email" name="email" required autocomplete="email"></div><div class="field"><label for="pt-web">Website</label><input id="pt-web" name="website" placeholder="https://"></div></div>
<div class="row2"><div class="field"><label for="pt-int">Interested in</label><select id="pt-int" name="interest" required><option value="">Choose…</option><option>Sponsored style page</option><option>Display advertising</option><option>Tool sponsorship</option><option>Newsletter placement</option><option>Contest sponsorship</option><option>Lead partnership</option><option>Affiliate / content partnership</option><option>Website / domain acquisition</option><option>Other</option></select></div>
<div class="field"><label for="pt-bud">Budget range</label><select id="pt-bud" name="budget"><option>To discuss</option><option>Under $1,000</option><option>$1,000–$5,000</option><option>$5,000–$20,000</option><option>$20,000+</option></select></div></div>
<div class="field"><label for="pt-msg">Goals and timing</label><textarea id="pt-msg" name="message" required></textarea></div>
{_consent()}{HP}<button class="btn btn-accent" type="submit">Send enquiry</button></form>{done}</div></div></div></section>"""


def contact_body(c):
    return _hero("Contact", "Talk to All-Style", "Questions, corrections, feedback or press: send us a message and we'll reply by email.") + f"""
<section class="section" style="padding-top:20px"><div class="wrap layout" style="padding-top:0"><div class="card">
<form class="form" data-form="Contact message" data-ok="Thank you! Your message has been received. We'll reply by email." novalidate>
<div class="row2"><div class="field"><label for="ct-name">Name</label><input id="ct-name" name="name" required autocomplete="name"></div><div class="field"><label for="ct-email">Email</label><input id="ct-email" type="email" name="email" required autocomplete="email"></div></div>
<div class="field"><label for="ct-topic">Topic</label><select id="ct-topic" name="topic"><option>General question</option><option>Feedback or idea</option><option>Correction</option><option>Press</option><option>Privacy request</option><option>Something else</option></select></div>
<div class="field"><label for="ct-msg">Message</label><textarea id="ct-msg" name="message" required></textarea></div>
{_consent()}{HP}<button class="btn btn-accent" type="submit">Send message</button></form></div>
<aside class="side"><div class="card"><h3>Looking for a pro?</h3><p class="small muted">Use Get Styled for a free match.</p><a class="btn btn-sm" href="{{{{R}}}}get-styled/">Get Styled</a></div>
<div class="card"><h3>Business enquiries</h3><p class="small muted">Advertising, sponsorship and partnerships.</p><a class="btn btn-sm" href="{{{{R}}}}partners/">Partner with us</a></div>
<div class="card"><h3>Join us</h3><p class="small muted">Writers, creators and moderators.</p><a class="btn btn-sm" href="{{{{R}}}}careers/">Careers</a></div></aside></div></section>"""


def _legal(title, lead, html_body):
    return (f'<section class="hero" style="padding-bottom:26px"><div class="wrap narrow">{{{{CRUMBS}}}}<h1>{title}</h1><p class="lead">{lead}</p>'
            f'<p class="small muted">Effective {EFFECTIVE}</p></div></section><section class="section" style="padding-top:20px"><div class="wrap narrow prose">{html_body}</div></section>')


def STATIC_PAGES(c):
    n = len(c["STYLES"])
    about = _legal("About All-Style", "The Style Atlas: every named style decoded, plus free tools to find yours.", f"""
<h2>What we do</h2><p>All-Style explains the styles people search for every day, from fashion aesthetics like Old Money and Dark Academia to interior styles like Japandi and Mid-Century Modern, haircuts like the wolf cut and dress codes from white tie to smart casual. Today the Atlas covers {n} styles, each with its palette (with hex codes), signature pieces, materials, do's and don'ts and a three-step way to start.</p>
<p>Alongside the Atlas we build free tools (a Style DNA Quiz, colour season finder, body and face shape calculators, size converter, capsule builder, outfit shuffler, dress code decoder, palette generator and budget planner) and long-form guides.</p>
<h2>Editorial policy</h2><ul><li><strong>Original writing.</strong> Every profile and guide is written for All-Style. We don't copy text from other publications.</li><li><strong>No stock or third-party photos.</strong> Style artwork on this site is generated from each style's palette, so we never publish images we don't have rights to.</li><li><strong>Independence.</strong> Sponsored content is labelled. Sponsors and advertisers never buy editorial verdicts.</li><li><strong>Corrections.</strong> Spot an error? <a href="{{{{R}}}}contact/">Tell us</a> and we'll fix it promptly.</li><li><strong>Automated sections.</strong> Trend Pulse headlines and the video library update automatically from public RSS feeds; headlines link to their original publishers and videos play from YouTube.</li></ul>
<h2>How All-Style is funded</h2><p>Advertising (Google AdSense), optional matching with professionals through <a href="{{{{R}}}}get-styled/">Get Styled</a>, clearly labelled <a href="{{{{R}}}}partners/">sponsorships</a> and reader <a href="{{{{R}}}}support/">support</a>. Reading and using tools is free.</p>
<h2>Contact</h2><p>Use the <a href="{{{{R}}}}contact/">contact form</a>. For website, domain, sponsorship, advertising or partnership interest, use the link at the top of every page.</p>""")
    privacy = _legal("Privacy Policy", "How All-Style collects, uses and protects information.", """
<h2>Who we are</h2><p>All-Style ("we", "us") operates this website. You can reach us through the <a href="{{R}}contact/">contact form</a>.</p>
<h2>Information we collect</h2><ul><li><strong>Information you submit</strong> in forms (for example name, email, phone, location, budget, style preferences, messages, contest entries and job applications).</li><li><strong>Information stored on your device</strong>: your theme, saved styles (My Board), quiz results, capsule checklist and wardrobe for the outfit shuffler are kept in your browser's local storage and are not sent to us unless you include them in a form.</li><li><strong>Automatically collected data</strong> by our advertising and hosting providers, such as IP address, device and browser information, and cookies (see below).</li></ul>
<h2>How we use information</h2><ul><li>To respond to messages and requests and, for Get Styled requests, to match you with up to three professionals and share your request details with them.</li><li>To review Pro Network, job and partnership applications, run contests and process donation pledges.</li><li>To send the Weekly Style Brief if you opt in (unsubscribe at any time).</li><li>To operate, secure and improve the site and show advertising.</li></ul>
<h2>Form processing</h2><p>Forms are delivered to our inbox through FormSubmit (formsubmit.co), a third-party form-forwarding service, which processes the submitted data to deliver it to us.</p>
<h2>Advertising and Google</h2><p>We use Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visits to this and/or other sites on the internet. You may opt out of personalised advertising by visiting <a href="https://adssettings.google.com/" rel="noopener" target="_blank">Google Ads Settings</a>, and you can opt out of some third-party vendors' use of cookies for personalised advertising at <a href="https://www.aboutads.info/choices/" rel="noopener" target="_blank">aboutads.info</a>. Learn more about <a href="https://policies.google.com/technologies/partner-sites" rel="noopener" target="_blank">how Google uses data from partner sites</a>. If you choose "Essential only" in our cookie banner, we request non-personalised ads.</p>
<h2>Embedded content</h2><p>Videos are embedded using YouTube's privacy-enhanced mode and load only when you click play. Fonts are served by Google Fonts. These providers may collect data according to their own policies.</p>
<h2>Sharing</h2><p>We do not sell your personal information. We share it only with the professionals you ask to be matched with, service providers that help us run the site (such as form delivery, hosting and advertising), or when required by law.</p>
<h2>Retention</h2><p>We keep form submissions only as long as needed for the purpose they were submitted for, and generally no longer than 24 months, unless the law requires longer.</p>
<h2>Your rights</h2><p>Depending on where you live (for example under GDPR, UK GDPR, PIPEDA or Quebec's Law 25, or California law), you may have rights to access, correct, delete or port your data and to object to or restrict certain processing. Send a request via the <a href="{{R}}contact/">contact form</a> with the topic "Privacy request".</p>
<h2>Children</h2><p>All-Style is intended for adults. We do not knowingly collect personal information from children under 16. Contest entries are limited to adults 18+.</p>
<h2>Security</h2><p>The site is served over HTTPS. No method of transmission is completely secure, so please don't submit sensitive information such as payment card numbers through our forms.</p>
<h2>Changes</h2><p>We may update this policy and will change the effective date above when we do.</p>""")
    cookies = _legal("Cookie Policy", "What cookies and similar technologies All-Style uses and how to control them.", """
<h2>Essential storage</h2><p>We use your browser's local storage (not tracking cookies) to remember your theme, cookie choice, saved styles, quiz results and tool progress. This stays on your device.</p>
<h2>Advertising cookies</h2><p>Google AdSense and its partners may set cookies to show and measure ads, including personalised ads if you consent. Choosing "Essential only" asks Google to serve non-personalised ads, which still use cookies for frequency capping, fraud prevention and aggregated reporting.</p>
<h2>Third-party embeds</h2><p>YouTube (privacy-enhanced mode, after you click play) and Google Fonts may set or read their own cookies or collect technical data.</p>
<h2>Managing cookies</h2><p>You can change your choice at any time by clearing this site's data in your browser, which shows the banner again. You can also block cookies in your browser settings and manage Google ad personalisation at <a href="https://adssettings.google.com/" target="_blank" rel="noopener">Google Ads Settings</a>.</p>""")
    terms = _legal("Terms of Use", "The rules for using All-Style.", """
<h2>Acceptance</h2><p>By using All-Style you agree to these terms. If you don't agree, please don't use the site.</p>
<h2>Content and tools</h2><p>All content and tools are provided for general information and inspiration. Results from calculators, quizzes and converters are estimates and may not suit every person, brand or situation.</p>
<h2>Get Styled and the Pro Network</h2><p>When you request a match, we introduce you to independent professionals. They are not our employees or agents. Any agreement, payment or service is between you and the professional; please check credentials, quotes and terms before hiring.</p>
<h2>Your submissions</h2><p>You're responsible for what you submit. Don't submit unlawful, infringing or harmful content. Contest entries are also governed by the official rules on the <a href="{{R}}contests/">contests page</a>.</p>
<h2>Intellectual property</h2><p>The All-Style text, design, generated artwork and code are protected by copyright. You may share links and short quotations with attribution. Third-party names and trademarks belong to their owners (see <a href="{{R}}trademark/">Trademark &amp; Copyright</a>).</p>
<h2>External links</h2><p>We link to third-party sites (for example news headlines and YouTube). We're not responsible for their content or practices.</p>
<h2>Disclaimer of warranties and liability</h2><p>The site is provided "as is". To the fullest extent permitted by law, we disclaim all warranties and are not liable for indirect or consequential losses arising from your use of the site or any professional you hire.</p>
<h2>Changes</h2><p>We may update these terms; the effective date above shows the latest version.</p>""")
    disclaimer = _legal("Disclaimer", "Important context for using All-Style's content and tools.", """
<h2>General information only</h2><p>Style, beauty and interior content on All-Style is general guidance, not professional advice for your specific situation. For hair treatments, skin concerns, structural home changes or electrical work, consult a qualified professional.</p>
<h2>Tools and estimates</h2><p>Size conversions are based on common standard tables; brands vary, so check each brand's own chart. Colour, body-shape and face-shape results are guides that depend on the accuracy of your inputs and lighting. Budget splits are planning starting points, not quotes.</p>
<h2>Advertising and sponsorship</h2><p>All-Style displays ads served by Google and may publish clearly labelled sponsored content. We may receive compensation when you are matched with a professional or use a partner's service. This never changes our editorial descriptions of styles.</p>
<h2>Automated content</h2><p>Headlines and videos in Trend Pulse and the Video Library are collected automatically from public feeds and belong to their publishers. Inclusion doesn't imply endorsement.</p>""")
    trademark = _legal("Trademark &amp; Copyright Disclosure", "Who owns what, and what All-Style is (and isn't) affiliated with.", """
<h2>Independent publication</h2><p><strong>All-Style</strong> is an independent style publication and directory. It is <strong>not affiliated with, endorsed by or sponsored by</strong> any company, brand or product that uses a similar name, including the "ALSTYLE" / "Alstyle Apparel &amp; Activewear" apparel marks owned by Gildan Activewear or its affiliates, or any business trading as "Allstyle", "All Style", "AllStyles", "All Styles" or similar. We use the descriptive phrase "all style" in its ordinary English meaning: content covering all styles.</p>
<h2>Third-party trademarks</h2><p>Brand, designer, publication, channel and product names mentioned on this site are trademarks of their respective owners and are used only to identify them (nominative use). Their mention does not imply any affiliation or endorsement.</p>
<h2>Copyright</h2><p>© All-Style. The text, generated artwork, design and code of this site are original works and may not be reproduced without permission, except for short quotations with attribution and links. Style names (for example "Japandi" or "Dark Academia") are common descriptive terms and are not claimed by All-Style.</p>
<h2>Images</h2><p>All-Style does not publish stock or third-party photographs. Style illustrations are generated from colour palettes. Video thumbnails and embeds are provided by YouTube and remain the property of their creators.</p>
<h2>Headlines</h2><p>Trend Pulse shows headline titles and links that point to the original publishers. We do not republish article text.</p>
<h2>Reporting concerns</h2><p>If you believe content on All-Style infringes your rights, please use the <a href="{{R}}contact/">contact form</a> with the topic "Something else" and include the page URL, the work concerned and your contact details. We review and respond promptly.</p>""")
    return [
        ("about/", "About All-Style", "About All-Style, our editorial policy and how the site is funded.", about),
        ("privacy/", "Privacy Policy", "How All-Style collects, uses and protects your information, including Google AdSense cookies.", privacy),
        ("cookies/", "Cookie Policy", "Cookies and local storage used by All-Style and how to control them.", cookies),
        ("terms/", "Terms of Use", "Terms for using All-Style, its tools and the Get Styled matching service.", terms),
        ("disclaimer/", "Disclaimer", "Disclaimer for All-Style content, tools, advertising and automated sections.", disclaimer),
        ("trademark/", "Trademark & Copyright Disclosure", "All-Style is an independent publication not affiliated with Alstyle apparel or any similarly named business. Trademark and copyright details.", trademark),
    ]
