"""Tool page definitions: copy, FAQs and form markup. Logic lives in assets/js/tools.js."""

TOOLS = [
{
"slug": "color-season", "name": "Colour Season Finder", "ico": "Cs", "pillar": "wear",
"short": "Find which of the 12 colour seasons suits your skin, hair and eyes.",
"intro": "Answer seven quick questions about your natural colouring and get your seasonal colour palette: the shades that make your skin look clearer and your eyes brighter, plus your best neutrals.",
"ui": """
<form id="cs-form" class="form">
  <div class="field"><span class="legend">1. The veins on your inner wrist look mostly…</span>
    <div class="choice-grid">
      <label class="choice"><input type="radio" name="vein" value="-1" required><span>Blue or purple</span></label>
      <label class="choice"><input type="radio" name="vein" value="1"><span>Green or olive</span></label>
      <label class="choice"><input type="radio" name="vein" value="0"><span>Hard to tell / both</span></label>
    </div></div>
  <div class="field"><span class="legend">2. Which jewellery flatters you more?</span>
    <div class="choice-grid">
      <label class="choice"><input type="radio" name="metal" value="-1" required><span>Silver / platinum</span></label>
      <label class="choice"><input type="radio" name="metal" value="1"><span>Gold / brass</span></label>
      <label class="choice"><input type="radio" name="metal" value="0"><span>Both equally</span></label>
    </div></div>
  <div class="field"><span class="legend">3. Next to your face, which looks better?</span>
    <div class="choice-grid">
      <label class="choice"><input type="radio" name="white" value="-1" required><span>Pure, bright white</span></label>
      <label class="choice"><input type="radio" name="white" value="1"><span>Cream / ivory</span></label>
      <label class="choice"><input type="radio" name="white" value="0"><span>No real difference</span></label>
    </div></div>
  <div class="field"><span class="legend">4. Your natural hair colour (before greying or dye)</span>
    <div class="choice-grid">
      <label class="choice"><input type="radio" name="hair" value="-2" required><span>Light blonde</span></label>
      <label class="choice"><input type="radio" name="hair" value="-1"><span>Dark blonde / light brown</span></label>
      <label class="choice"><input type="radio" name="hair" value="0"><span>Medium brown / auburn</span></label>
      <label class="choice"><input type="radio" name="hair" value="2"><span>Dark brown / black</span></label>
    </div></div>
  <div class="field"><span class="legend">5. Your eye colour depth</span>
    <div class="choice-grid">
      <label class="choice"><input type="radio" name="eyes" value="-2" required><span>Light (pale blue, grey, light green)</span></label>
      <label class="choice"><input type="radio" name="eyes" value="0"><span>Medium (hazel, green-brown, blue-green)</span></label>
      <label class="choice"><input type="radio" name="eyes" value="2"><span>Dark (deep brown, black-brown)</span></label>
    </div></div>
  <div class="field"><span class="legend">6. Contrast between your hair, skin and eyes</span>
    <div class="choice-grid">
      <label class="choice"><input type="radio" name="contrast" value="-2" required><span>Low: everything blends</span></label>
      <label class="choice"><input type="radio" name="contrast" value="0"><span>Medium</span></label>
      <label class="choice"><input type="radio" name="contrast" value="2"><span>High: striking contrast</span></label>
    </div></div>
  <div class="field"><span class="legend">7. Do your eyes look…</span>
    <div class="choice-grid">
      <label class="choice"><input type="radio" name="eyesclear" value="1" required><span>Clear and sparkling</span></label>
      <label class="choice"><input type="radio" name="eyesclear" value="-1"><span>Soft, smoky or blended</span></label>
    </div></div>
  <button class="btn btn-accent" type="submit">Find my season</button>
</form>
<div id="cs-result" class="tool-result" aria-live="polite"></div>""",
"how": "<p>Seasonal colour analysis scores three dimensions: <strong>undertone</strong> (questions 1–3), <strong>depth</strong> (questions 4–5) and <strong>clarity</strong> (questions 6–7). Your strongest dimension decides your sub-season (for example Light, Deep, Bright, Soft, Warm or Cool), and your undertone decides the family (Spring, Summer, Autumn or Winter). Read the full <a href=\"{{R}}guides/seasonal-color-analysis/\">guide to the 12 seasons</a>.</p>",
"faqs": [["How accurate is an online colour analysis?", "It's a reliable starting point when you answer in daylight without makeup. A professional draping session is more precise because it compares fabrics against your face in person."], ["Should I wear only my season's colours?", "No. Use them near your face (tops, scarves, glasses, makeup). Trousers, shoes and bags can be anything you like."], ["Does hair dye change my season?", "Dye changes your overall contrast, so some colours may flatter you more or less, but your skin's undertone stays the same."]]
},
{
"slug": "body-shape", "name": "Body Shape Calculator", "ico": "Bs", "pillar": "wear",
"short": "Enter three measurements to get your body shape and what flatters it.",
"intro": "Use bust or chest, waist and hip measurements to find your body shape, with practical styling tips. Works in centimetres or inches: just use the same unit for all three.",
"ui": """
<form id="bs-form" class="form">
  <div class="row2">
    <div class="field"><label for="bs-type">Calculate for</label><select id="bs-type"><option value="f">Women's proportions</option><option value="m">Men's proportions</option></select></div>
    <div class="field"><label for="bs-unit">Unit</label><select id="bs-unit"><option>cm</option><option>in</option></select></div>
  </div>
  <div class="row2">
    <div class="field"><label for="bs-1" id="bs-l1">Bust</label><input id="bs-1" type="number" step="0.1" min="20" max="300" required inputmode="decimal"><span class="hint">Around the fullest part.</span></div>
    <div class="field"><label for="bs-2">Waist</label><input id="bs-2" type="number" step="0.1" min="20" max="300" required inputmode="decimal"><span class="hint">Around the narrowest part.</span></div>
  </div>
  <div class="field"><label for="bs-3" id="bs-l3">Hips</label><input id="bs-3" type="number" step="0.1" min="20" max="300" required inputmode="decimal"><span class="hint">Around the widest part of hips and seat.</span></div>
  <button class="btn btn-accent" type="submit">Calculate my shape</button>
</form>
<div id="bs-result" class="tool-result" aria-live="polite"></div>""",
"how": "<p>The calculator compares ratios between your measurements rather than absolute sizes. For example, a pear shape has hips at least about 5% wider than the bust, while an hourglass has a balanced bust and hips with a waist at least 25% smaller. Shapes describe <strong>proportions, not size</strong>, and every shape can wear every style; the tips simply show how to create balance.</p>",
"faqs": [["What if I'm between two shapes?", "Most people are. Read the tips for both and keep the ones that match how you like to look."], ["Do I need a tape measure?", "Yes, a soft tailor's tape gives the best results. Measure over light clothing and keep the tape level."], ["Is my data stored?", "No. Calculations happen in your browser and nothing is sent anywhere."]]
},
{
"slug": "face-shape", "name": "Face Shape Finder", "ico": "Fs", "pillar": "hair",
"short": "Measure four points to find your face shape and the haircuts that balance it.",
"intro": "Measure your forehead, cheekbones, jaw and face length to identify your face shape, then see haircuts and glasses that create balance.",
"ui": """
<form id="fs-form" class="form">
  <div class="row2">
    <div class="field"><label for="fs-fh">Forehead width</label><input id="fs-fh" type="number" step="0.1" min="5" max="40" required inputmode="decimal"><span class="hint">Across the widest part, hairline to hairline.</span></div>
    <div class="field"><label for="fs-cb">Cheekbone width</label><input id="fs-cb" type="number" step="0.1" min="5" max="40" required inputmode="decimal"><span class="hint">Across the highest points of the cheekbones.</span></div>
  </div>
  <div class="row2">
    <div class="field"><label for="fs-jw">Jaw width</label><input id="fs-jw" type="number" step="0.1" min="5" max="40" required inputmode="decimal"><span class="hint">Below the ear to the chin, times two.</span></div>
    <div class="field"><label for="fs-len">Face length</label><input id="fs-len" type="number" step="0.1" min="5" max="40" required inputmode="decimal"><span class="hint">Centre of hairline to tip of chin.</span></div>
  </div>
  <div class="field"><label for="fs-jaw">Jawline shape</label><select id="fs-jaw"><option value="rounded">Rounded / soft</option><option value="square">Square / angular</option><option value="pointed">Pointed / narrow chin</option></select></div>
  <p class="small muted">Use the same unit (cm or in) for every measurement.</p>
  <button class="btn btn-accent" type="submit">Find my face shape</button>
</form>
<div id="fs-result" class="tool-result" aria-live="polite"></div>""",
"how": "<p>The finder compares your face length with your cheekbone width and checks which of the three widths dominates. Long faces (ratio above about 1.55) are oval or oblong; short ratios (below about 1.3) are round or square; a wide forehead with a pointed chin suggests heart, and dominant cheekbones with a narrow forehead and jaw suggest diamond. See the full <a href=\"{{R}}guides/face-shapes-and-haircuts/\">face shapes and haircuts guide</a>.</p>",
"faqs": [["Can I use a photo instead of a tape?", "Yes. Take a straight-on photo with your hair pulled back and measure on screen; ratios matter, not absolute numbers."], ["Does face shape matter for men's haircuts?", "Yes. Men adjust with the height of the top, the fade height and beard shape to balance the face."], ["What matters more, face shape or hair texture?", "Both. A cut that suits your face but fights your texture won't last; mention both to your stylist."]]
},
{
"slug": "size-converter", "name": "Clothing & Shoe Size Converter", "ico": "Sz", "pillar": "wear",
"short": "Convert clothing and shoe sizes between US, UK, EU, AU and JP.",
"intro": "Shopping internationally? Convert women's and men's clothing and shoe sizes between US, UK, EU, Australian and Japanese systems in one click.",
"ui": """
<div class="form">
  <div class="row2">
    <div class="field"><label for="sz-cat">Category</label><select id="sz-cat"></select></div>
    <div class="field"><label for="sz-sys">Size system</label><select id="sz-sys"></select></div>
  </div>
  <div class="field"><label for="sz-val">Your size</label><select id="sz-val"></select></div>
</div>
<div id="sz-out" class="tool-result show" aria-live="polite"></div>""",
"how": "<p>The converter uses widely published standard conversion tables. Brands cut differently, so always check the specific brand's size chart and, for shoes, compare your foot length in centimetres, which is the most reliable measure.</p>",
"faqs": [["Why do my sizes differ between brands?", "There is no binding international standard; each brand grades its own patterns. Treat conversions as a starting point."], ["Are EU and French sizes the same?", "French and Spanish women's sizes are often one size larger than standard EU (for example EU 38 ≈ FR 40). Italian sizes differ again."], ["How do I measure foot length?", "Stand on paper, mark the heel and longest toe, and measure the distance in centimetres. Do it in the evening when feet are largest."]]
},
{
"slug": "capsule", "name": "Capsule Wardrobe Builder", "ico": "Cw", "pillar": "wear",
"short": "Build a printable 15, 25 or 33-piece capsule wardrobe checklist.",
"intro": "Tell us how you live, choose a palette and a capsule size, and get a tailored checklist you can tick off as you shop. Your progress is saved on this device.",
"ui": """
<form id="cap-form" class="form">
  <div class="row2">
    <div class="field"><label for="cap-life">Your week is mostly…</label><select id="cap-life" name="life"><option value="office">Office / client-facing</option><option value="casual">Casual / at home</option><option value="creative">Creative workplace</option><option value="travel">Travelling</option><option value="mixed">A bit of everything</option></select></div>
    <div class="field"><label for="cap-season">Season</label><select id="cap-season" name="season"><option value="all">All-year</option><option value="warm">Spring / summer</option><option value="cold">Autumn / winter</option></select></div>
  </div>
  <div class="row2">
    <div class="field"><label for="cap-size">Capsule size</label><select id="cap-size" name="size"><option value="15">15 pieces (minimal)</option><option value="25" selected>25 pieces</option><option value="33">33 pieces (Project 333 style)</option></select></div>
    <div class="field"><label for="cap-base">Base neutral</label><select id="cap-base" name="base"><option>Navy</option><option>Black</option><option>Camel</option><option>Charcoal</option><option>Olive</option></select></div>
  </div>
  <div class="field"><label for="cap-acc">Accent colour</label><input id="cap-acc" name="accent" type="color" value="#B8492F" style="height:48px;padding:4px"></div>
  <button class="btn btn-accent" type="submit">Build my capsule</button>
</form>
<div id="cap-out" class="tool-result" aria-live="polite"></div>""",
"how": "<p>The builder balances categories using a proven ratio (roughly 10 tops : 6 bottoms : 4 layers : 4 shoes : accessories for a 30-piece capsule) and picks items for your lifestyle and season. Read the <a href=\"{{R}}guides/capsule-wardrobe-formula/\">capsule wardrobe formula</a> for the reasoning.</p>",
"faqs": [["Do underwear and sportswear count?", "No. Most capsule methods exclude underwear, sleepwear, gym kit and special-occasion wear."], ["Can I add colour?", "Yes. Pick an accent colour and repeat it in a few tops and accessories so they all combine."], ["Where is my checklist saved?", "In your browser's local storage on this device only. Clearing site data resets it."]]
},
{
"slug": "outfit-shuffle", "name": "Outfit Shuffler", "ico": "Os", "pillar": "wear",
"short": "Shuffle your own wardrobe into colour-balanced outfits. Lock what you love.",
"intro": "Add the clothes you own (or start with our sample wardrobe), then shuffle for instant outfit ideas. Lock any piece to build around it. The shuffler keeps outfits to two or fewer non-neutral colours.",
"ui": """
<div class="btn-row"><button type="button" class="btn btn-accent" id="os-shuffle">Shuffle outfit</button><button type="button" class="btn btn-ghost" id="os-reset">Reset to sample wardrobe</button></div>
<div id="os-grid" class="shuffle-grid" aria-live="polite"></div>
<p id="os-note" class="small muted" style="margin-top:12px"></p>
<hr>
<h3>Your wardrobe</h3>
<form id="os-add" class="add-row">
  <div class="field"><label for="os-name">Item</label><input id="os-name" maxlength="40" placeholder="e.g. Green cardigan"></div>
  <div class="field"><label for="os-cat">Category</label><select id="os-cat"><option value="top">Top</option><option value="bottom">Bottom</option><option value="shoes">Shoes</option><option value="layer">Layer</option><option value="accessory">Accessory</option></select></div>
  <div class="field"><label for="os-col">Colour</label><input id="os-col" type="color" value="#2F4A3A" style="height:48px;padding:4px"></div>
  <button class="btn" type="submit">Add</button>
</form>
<div id="os-list" class="grid" style="gap:14px;margin-top:16px"></div>""",
"how": "<p>Each shuffle picks one item per category and checks the colours: greys, black, white, navy-leaning darks, tans and browns count as neutrals, and outfits are re-rolled until no more than two non-neutral colours appear together. Your wardrobe is stored only in your browser.</p>",
"faqs": [["How many outfits can my wardrobe make?", "The tool multiplies the number of items in each category. Even 5 tops, 4 bottoms and 3 shoes make 60 base outfits."], ["Is my wardrobe uploaded anywhere?", "No. Everything stays in your browser's local storage."], ["Why two colours?", "It's a simple rule that keeps outfits cohesive. Break it deliberately when you want a bolder look."]]
},
{
"slug": "dress-code", "name": "Dress Code Decoder", "ico": "Dc", "pillar": "occasion",
"short": "What to wear for white tie, black tie, cocktail, business casual and more.",
"intro": "Choose the dress code on your invitation and get a clear outfit formula, a formality rating and the mistakes to avoid.",
"ui": """
<div class="form"><div class="field"><label for="dc-sel">The invitation says…</label><select id="dc-sel"></select></div></div>
<div id="dc-out" class="tool-result" aria-live="polite"></div>""",
"how": "<p>Dress codes form a ladder of formality. The decoder rates each code from 1 to 10 and gives outfit formulas for suits, dresses and any outfit, so it works whatever you wear. See <a href=\"{{R}}guides/dress-codes-decoded/\">Dress Codes Decoded</a> for how to read an invitation.</p>",
"faqs": [["What if there's no dress code?", "Look at the venue and time: evening and formal venues suggest cocktail; daytime and casual venues suggest smart casual. Asking the host is always fine."], ["Can I wear a jumpsuit to a formal event?", "An elegant jumpsuit in a luxurious fabric works for cocktail and often black tie optional."], ["Is it worse to be over- or under-dressed?", "Generally under-dressed feels worse. Aim slightly above the code with simple accessories."]]
},
{
"slug": "palette", "name": "Palette Generator", "ico": "Pg", "pillar": "home",
"short": "Turn one colour into a 60-30-10 palette for a room, outfit or wedding.",
"intro": "Pick a colour you love and a harmony rule. The generator builds a five-colour palette with a 60-30-10 split, ready to copy as hex codes for paint, fabrics, outfits or wedding stationery.",
"ui": """
<div class="form"><div class="row2">
  <div class="field"><label for="pg-base">Start colour</label><input id="pg-base" type="color" value="#B8492F" style="height:52px;padding:4px"></div>
  <div class="field"><label for="pg-scheme">Harmony</label><select id="pg-scheme"><option value="mono">Tonal (monochrome)</option><option value="analogous">Analogous (neighbours)</option><option value="complementary">Complementary (opposites)</option><option value="triadic">Triadic (three-way)</option></select></div>
</div></div>
<div id="pg-out" class="tool-result" aria-live="polite"></div>""",
"how": "<p>The generator converts your colour to hue, saturation and lightness, then rotates the hue (30° for analogous, 180° for complementary, 120° for triadic) and adds a soft neutral and a deep anchor in the same hue family. The <strong>60-30-10 rule</strong> assigns 60% to a dominant colour, 30% to a secondary and 10% to accents, a reliable balance in interiors and outfits.</p>",
"faqs": [["Will paint match the hex code exactly?", "Screens and paints differ. Use the hex code to find the closest paint chip, then test a sample in your room's light."], ["Which harmony is safest?", "Tonal and analogous schemes are the easiest to live with; complementary and triadic are bolder."], ["Can I use this for a wedding?", "Yes. Use the soft neutral as the base, the start colour as the main colour and one accent sparingly."]]
},
{
"slug": "budget", "name": "Makeover Budget Planner", "ico": "Bp", "pillar": "home",
"short": "Split your room makeover budget across furniture, lighting, textiles and more.",
"intro": "Enter the budget you have and the room you're tackling. The planner allocates it across categories, sets aside a 10% contingency and, if you plan to hire help, reserves a design fee you choose.",
"ui": """
<form id="bp-form" class="form">
  <div class="row2">
    <div class="field"><label for="bp-total">Total budget</label><input id="bp-total" type="number" min="1" step="1" required inputmode="numeric" placeholder="e.g. 5000"></div>
    <div class="field"><label for="bp-cur">Currency</label><select id="bp-cur"><option value="$">$ (USD/CAD/AUD)</option><option value="£">£ (GBP)</option><option value="€">€ (EUR)</option><option value="₹">₹ (INR)</option></select></div>
  </div>
  <div class="row2">
    <div class="field"><label for="bp-room">Room</label><select id="bp-room"><option value="living">Living room</option><option value="bedroom">Bedroom</option><option value="dining">Dining room</option><option value="office">Home office</option><option value="kitchen">Kitchen refresh (no remodel)</option></select></div>
    <div class="field"><label for="bp-fee">Design fee to reserve (%)</label><input id="bp-fee" type="number" min="0" max="50" step="1" value="0" inputmode="numeric"><span class="hint">0 if DIY. Use the fee your designer quotes.</span></div>
  </div>
  <button class="btn btn-accent" type="submit">Plan my budget</button>
</form>
<div id="bp-out" class="tool-result" aria-live="polite"></div>""",
"how": "<p>The planner applies a room-specific split that puts most of the money into anchor pieces (sofa, bed, table, chair) that you'll use daily and keep longest, then lighting and rugs, which change a room the most per dollar, and keeps 10% back for surprises like delivery fees or a lamp that doesn't work out.</p>",
"faqs": [["Should I spend most on the sofa?", "Usually, yes. It's the most-used and hardest-to-replace piece in a living room. Accessories are easy to upgrade later."], ["What's a contingency for?", "Delivery charges, assembly, a returned item or a price change. Ten percent is a sensible minimum."], ["Can a designer save money?", "Often, by avoiding costly mistakes and accessing trade pricing, but compare their fee against your budget."]]
}
]
