/* All-Style interactive tools. Loaded only on tool, quiz, compare and board pages. */
(function () {
  "use strict";
  var AS = window.AS, $ = AS.$, $$ = AS.$$, esc = AS.esc, R = AS.root, LS = AS.LS;
  var host = $("[data-tool]"); if (!host) return;
  var tool = host.getAttribute("data-tool");
  var PNAME = { wear: "Wear", home: "Interiors", hair: "Hair & Beauty", occasion: "Occasions" };
  var PRO = { wear: "a personal stylist", home: "an interior designer", hair: "a hair & makeup pro", occasion: "a wedding or event stylist" };
  function pal(c) { return c.map(function (x) { return '<span style="background:' + x[1] + '"></span>'; }).join(""); }
  function show(el, html) { el.innerHTML = html; el.classList.add("show"); el.scrollIntoView({ behavior: "smooth", block: "nearest" }); }
  function num(id) { var v = parseFloat(($("#" + id) || {}).value); return isNaN(v) ? null : v; }
  function ctaLink(service, styles) { return R + "get-styled/?service=" + service + (styles && styles.length ? "&styles=" + styles.join(",") : ""); }

  /* ================= STYLE DNA QUIZ ================= */
  var TOOLS = {};
  TOOLS.quiz = function () {
    Promise.all([AS.data("quiz"), AS.data("styles")]).then(function (r) {
      var Q = r[0], S = r[1], modes = $("#quiz-modes"), run = $("#quiz-run"), res = $("#quiz-result");
      var start = new URLSearchParams(location.search).get("mode");
      function begin(mode) {
        var qs = Q.shared.concat(Q[mode]), i = 0, vec = {};
        modes.hidden = true; run.hidden = false; res.classList.remove("show");
        function draw() {
          var q = qs[i];
          run.innerHTML = '<div class="small muted">' + esc(Q.modes[mode].label) + " · Question " + (i + 1) + " of " + qs.length + '</div><div class="progress"><i style="width:' + ((i) / qs.length * 100) + '%"></i></div>' +
            '<h2 style="margin-top:6px">' + esc(q.q) + '</h2><div class="quiz-opts">' + q.a.map(function (a, k) {
              return '<button type="button" data-k="' + k + '">' + (a[2] ? '<span class="sw">' + a[2].map(function (h) { return '<i style="background:' + h + '"></i>'; }).join("") + "</span>" : "") + esc(a[0]) + "</button>";
            }).join("") + '</div>' + (i ? '<p style="margin-top:14px"><button type="button" class="btn btn-ghost btn-sm" data-back>← Back</button></p>' : "");
          $$("[data-k]", run).forEach(function (b) {
            b.addEventListener("click", function () {
              q._pick = +b.getAttribute("data-k");
              i++; if (i < qs.length) draw(); else finish();
            });
          });
          var back = $("[data-back]", run); if (back) back.addEventListener("click", function () { i--; draw(); });
        }
        function finish() {
          vec = {}; qs.forEach(function (q) { (q.a[q._pick][1] || []).forEach(function (t) { vec[t] = (vec[t] || 0) + 1; }); });
          var norm = Math.sqrt(Object.keys(vec).reduce(function (s, k) { return s + vec[k] * vec[k]; }, 0)) || 1;
          function cos(st) { var dot = 0; st.q.forEach(function (t) { dot += vec[t] || 0; }); return dot / (norm * Math.sqrt(st.q.length)); }
          var scored = S.map(function (st) { return { st: st, sc: cos(st) }; });
          var pillar = Q.modes[mode].pillar;
          var mine = scored.filter(function (x) { return x.st.p === pillar; }).sort(function (a, b) { return b.sc - a.sc; }).slice(0, 3);
          var others = ["wear", "home", "hair", "occasion"].filter(function (p) { return p !== pillar; }).map(function (p) {
            return scored.filter(function (x) { return x.st.p === p; }).sort(function (a, b) { return b.sc - a.sc; })[0];
          });
          var top = mine.map(function (x) { return { s: x.st.s, n: x.st.n, p: Math.round(x.sc * 100) }; });
          LS.set("as-quiz", { mode: mode, top: top, t: Date.now() });
          run.hidden = true;
          var traits = Object.keys(vec).sort(function (a, b) { return vec[b] - vec[a]; }).slice(0, 3);
          show(res, '<p class="eyebrow">Your Style DNA</p><h2 class="result-title">' + esc(mine[0].st.n) + ' leads your mix</h2><p class="muted">Top traits: <strong>' + traits.join(" · ") + "</strong>. Match scores compare your answers with each style's trait profile.</p>" +
            '<div class="grid" style="gap:10px;margin:16px 0">' + mine.map(function (x) {
              return '<a class="match" href="' + R + "styles/" + x.st.s + '/"><div class="mini">' + pal(x.st.c) + "</div><div><b>" + esc(x.st.n) + '</b><div class="small muted">' + esc(x.st.t) + '</div></div><div class="pct">' + Math.round(x.sc * 100) + "%</div></a>";
            }).join("") + "</div>" +
            '<div class="cta-card" style="margin:20px 0"><h3>Turn this into a real plan</h3><p>Get matched with ' + esc(PRO[pillar]) + " who works in " + esc(mine[0].st.n) + " and " + esc(mine[1].st.n) + '. Free to request, no obligation.</p><a class="btn" href="' + ctaLink(Q.modes[mode].service, top.map(function (t) { return t.s; })) + '">Get matched with a pro</a></div>' +
            '<h3>Your style in other areas</h3><div class="grid g3" style="margin-top:10px">' + others.map(function (x) {
              return '<a class="match" style="grid-template-columns:60px 1fr" href="' + R + "styles/" + x.st.s + '/"><div class="mini">' + pal(x.st.c) + '</div><div><span class="small muted">' + PNAME[x.st.p] + "</span><br><b>" + esc(x.st.n) + "</b></div></a>";
            }).join("") + '</div><p style="margin-top:18px" class="btn-row"><button class="btn btn-ghost" type="button" data-restart>Retake quiz</button><a class="btn btn-ghost" href="' + R + "compare/?a=" + mine[0].st.s + "&b=" + mine[1].st.s + '">Compare my top two</a><button class="btn btn-ghost" type="button" data-save-top="' + top.map(function (t) { return t.s; }).join(",") + '">Save top 3 to My Board</button></p>');
          $("[data-restart]", res).addEventListener("click", function () { res.classList.remove("show"); modes.hidden = false; });
          $("[data-save-top]", res).addEventListener("click", function (e) {
            var b = AS.board(); e.target.getAttribute("data-save-top").split(",").forEach(function (s) { if (b.indexOf(s) < 0) b.push(s); });
            LS.set("as-board", b); AS.toast("Saved to My Board");
          });
        }
        draw();
      }
      $$("[data-mode]", modes).forEach(function (b) { b.addEventListener("click", function () { begin(b.getAttribute("data-mode")); }); });
      if (start && Q.modes[start]) begin(start);
    });
  };

  /* ================= COMPARE ================= */
  TOOLS.compare = function () {
    AS.data("styles").then(function (S) {
      var a = $("#cmp-a"), b = $("#cmp-b"), out = $("#cmp-out"), qs = new URLSearchParams(location.search);
      var opts = ["wear", "home", "hair", "occasion"].map(function (p) {
        return '<optgroup label="' + PNAME[p] + '">' + S.filter(function (s) { return s.p === p; }).map(function (s) { return '<option value="' + s.s + '">' + esc(s.n) + "</option>"; }).join("") + "</optgroup>";
      }).join("");
      a.innerHTML = opts; b.innerHTML = opts;
      a.value = qs.get("a") || "japandi"; b.value = qs.get("b") || "scandinavian-interior";
      function by(s) { return S.filter(function (x) { return x.s === s; })[0]; }
      function li(arr) { return "<ul style='margin:0;padding-left:1.1em'>" + arr.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>"; }
      function draw() {
        var x = by(a.value), y = by(b.value); if (!x || !y) return;
        var shared = x.q.filter(function (t) { return y.q.indexOf(t) > -1; });
        var rows = [["Pillar", PNAME[x.p], PNAME[y.p]], ["In one line", esc(x.t), esc(y.t)], ["Mood", x.m.join(", "), y.m.join(", ")],
          ["Palette", '<div class="palette">' + pal(x.c) + "</div>", '<div class="palette">' + pal(y.c) + "</div>"],
          ["Signature elements", li(x.k), li(y.k)], ["Materials", x.mat.join(", "), y.mat.join(", ")], ["Best for", esc(x.w), esc(y.w)], ["Start with", li(x.st), li(y.st)]];
        out.innerHTML = '<p class="note">Shared traits: <strong>' + (shared.length ? shared.join(", ") : "none — these two contrast strongly, which can work as a deliberate mix") + "</strong>.</p>" +
          '<div class="table-wrap" style="margin-top:14px"><table><thead><tr><th style="width:150px"></th><th><a href="' + R + "styles/" + x.s + '/">' + esc(x.n) + '</a></th><th><a href="' + R + "styles/" + y.s + '/">' + esc(y.n) + "</a></th></tr></thead><tbody>" +
          rows.map(function (r) { return "<tr><th>" + r[0] + "</th><td>" + r[1] + "</td><td>" + r[2] + "</td></tr>"; }).join("") + "</tbody></table></div>";
        history.replaceState(null, "", "?a=" + x.s + "&b=" + y.s);
      }
      a.addEventListener("change", draw); b.addEventListener("change", draw);
      $("#cmp-swap").addEventListener("click", function () { var t = a.value; a.value = b.value; b.value = t; draw(); });
      draw();
    });
  };

  /* ================= MY BOARD ================= */
  TOOLS.board = function () {
    AS.data("styles").then(function (S) {
      var out = $("#board-out"), shared = new URLSearchParams(location.search).get("s");
      AS.renderBoard = function () {
        var list = shared ? shared.split(",") : AS.board();
        var items = list.map(function (s) { return S.filter(function (x) { return x.s === s; })[0]; }).filter(Boolean);
        if (!items.length) { out.innerHTML = '<div class="empty">Your board is empty. Tap the heart on any style to save it here. Try the <a href="' + R + 'styles/">Style Atlas</a> or the <a href="' + R + 'quiz/">Style DNA Quiz</a>.</div>'; return; }
        var svc = items.some(function (i) { return i.p === "home"; }) ? "interior-room" : "personal-styling";
        out.innerHTML = (shared ? '<p class="note">You are viewing a shared board. <button class="btn btn-sm" type="button" id="board-import">Save all to my board</button></p>' : "") +
          '<div class="grid g3" style="margin-top:14px">' + items.map(function (i) {
            return '<a class="style-card" href="' + R + "styles/" + i.s + '/"><div class="palette" style="height:90px;border-radius:0">' + pal(i.c) + '</div><div class="body"><span class="chip ' + i.p + '">' + PNAME[i.p] + "</span><h3>" + esc(i.n) + "</h3><p>" + esc(i.t) + '</p></div><button class="save-btn" data-save="' + i.s + '"></button></a>';
          }).join("") + '</div><div class="btn-row" style="margin-top:20px"><a class="btn btn-accent" href="' + ctaLink(svc, items.map(function (i) { return i.s; })) + '">Get a pro to style my board</a>' +
          (shared ? "" : '<button class="btn btn-ghost" type="button" id="board-share">Copy share link</button><button class="btn btn-ghost" type="button" id="board-clear">Clear board</button>') + "</div>";
        $$("[data-save]", out).forEach(function (el) { el.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 21s-7.5-4.6-10-9.2C.3 8.6 2.2 4.5 6 4.5c2.1 0 3.4 1.1 4 2.2.6-1.1 1.9-2.2 4-2.2 3.8 0 5.7 4.1 4 7.3C19.5 16.4 12 21 12 21z"/></svg>'; el.setAttribute("aria-pressed", AS.board().indexOf(el.getAttribute("data-save")) > -1 ? "true" : "false"); });
        var sh = $("#board-share"); if (sh) sh.addEventListener("click", function () { var u = location.origin + location.pathname + "?s=" + AS.board().join(","); if (navigator.clipboard) navigator.clipboard.writeText(u); AS.toast("Share link copied"); });
        var cl = $("#board-clear"); if (cl) cl.addEventListener("click", function () { LS.set("as-board", []); AS.renderBoard(); });
        var im = $("#board-import"); if (im) im.addEventListener("click", function () { var b = AS.board(); items.forEach(function (i) { if (b.indexOf(i.s) < 0) b.push(i.s); }); LS.set("as-board", b); AS.toast("Saved to your board"); });
      };
      AS.renderBoard();
    });
  };

  /* ================= COLOUR SEASON ================= */
  var SEASONS = {
    "Light Spring": { d: "Light, warm and clear. Your best colours are fresh and delicate with a golden base.", c: ["#F7C59F", "#FFD8A8", "#A8E6CF", "#7FD1D1", "#F4978E", "#FBE7A1", "#C3B1E1", "#E8D5B7"], n: ["Ivory", "Light camel", "Warm grey"], x: "Black, heavy charcoal and dusty muted tones" },
    "Warm Spring": { d: "Warm and bright with golden undertones. Choose sunny, saturated warm colours.", c: ["#FF7F50", "#FFB347", "#F9D56E", "#8BC34A", "#2EC4B6", "#E07A5F", "#F28482", "#C68B59"], n: ["Cream", "Camel", "Warm beige"], x: "Icy pastels and cool blue-greys" },
    "Bright Spring": { d: "Clear, vivid and warm-leaning. High-energy colours bring your colouring alive.", c: ["#FF5E5B", "#FFBE0B", "#00BBF9", "#00F5D4", "#F15BB5", "#9BDE7E", "#FF8C42", "#3A86FF"], n: ["Bright white", "Warm navy", "Light grey"], x: "Dusty, greyed and muddy shades" },
    "Light Summer": { d: "Light, cool and soft. Powdery pastels look effortless on you.", c: ["#B8D8F2", "#D7C1E0", "#F6C6D0", "#A8DADC", "#CDE7BE", "#E3D9F2", "#9FB7D8", "#F2D0D9"], n: ["Soft white", "Light grey", "Rose beige"], x: "Black, orange and strong warm browns" },
    "Cool Summer": { d: "Cool and gentle with blue-pink undertones. Mid-tone cool colours flatter most.", c: ["#7B9ACC", "#C77DA0", "#6A8EAE", "#9AA9C4", "#B5838D", "#86A8A3", "#5D7298", "#D8A7B1"], n: ["Soft white", "Blue-grey", "Cool taupe"], x: "Orange, mustard and golden tones" },
    "Soft Summer": { d: "Muted and cool-neutral. Smoky, blended colours are your strength.", c: ["#8E9AAF", "#A3B4A2", "#B09398", "#7D8BA6", "#C6B2BE", "#8FA9A6", "#9C8AA5", "#B7A99A"], n: ["Pewter", "Mushroom", "Soft charcoal"], x: "Neon brights and pure black" },
    "Soft Autumn": { d: "Muted and warm-neutral. Earthy, softened colours look natural on you.", c: ["#B5A88F", "#A3A380", "#C9A88C", "#8B9A7A", "#D1A38A", "#9C8166", "#B7B39B", "#C08B6E"], n: ["Mushroom", "Soft camel", "Oatmeal"], x: "Icy colours, pure white and black" },
    "Warm Autumn": { d: "Rich, warm and golden. Spice and earth tones are your signature.", c: ["#C1440E", "#E09F3E", "#6B8E23", "#8C5E3C", "#D4A017", "#A0522D", "#556B2F", "#CC7722"], n: ["Camel", "Chocolate", "Olive"], x: "Cool pinks, icy blues and grey" },
    "Deep Autumn": { d: "Deep, warm and rich. Dark earth and jewel-like warm tones suit you.", c: ["#7B3F00", "#8B0000", "#2F4F2F", "#B8860B", "#5C4033", "#A0522D", "#004D40", "#6D2E46"], n: ["Espresso", "Dark olive", "Warm charcoal"], x: "Pastels and light, cool colours" },
    "Deep Winter": { d: "Deep, cool and high-contrast. Dark, crisp colours and jewel tones are ideal.", c: ["#0B132B", "#6A0572", "#003F5C", "#7A0019", "#006D5B", "#2E1A47", "#1B263B", "#B5179E"], n: ["Black", "Charcoal", "Pure white"], x: "Muted earthy tones and golden beige" },
    "Cool Winter": { d: "Cool and clear. Icy shades and true jewel tones flatter you.", c: ["#1E3A8A", "#C2185B", "#00838F", "#6A1B9A", "#B3E5FC", "#E1BEE7", "#0D47A1", "#AD1457"], n: ["Pure white", "Black", "Cool grey"], x: "Orange, rust and camel" },
    "Bright Winter": { d: "Vivid, cool and high-contrast. Bold, saturated colours were made for you.", c: ["#E4007C", "#0047AB", "#00A86B", "#FF0038", "#7F00FF", "#00CED1", "#FFD300", "#111111"], n: ["Pure white", "Black", "Charcoal"], x: "Dusty, muted and soft earth tones" }
  };
  TOOLS["color-season"] = function () {
    $("#cs-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var f = new FormData(e.target), W = 0, Dp = 0, C = 0;
      ["vein", "metal", "white"].forEach(function (k) { W += +(f.get(k) || 0); });
      Dp += +(f.get("hair") || 0) + +(f.get("eyes") || 0);
      C += +(f.get("contrast") || 0) + +(f.get("eyesclear") || 0);
      var warm = W > 0 || (W === 0 && f.get("metal") === "1");
      var aW = Math.abs(W) / 3, aD = Math.abs(Dp) / 4, aC = Math.abs(C) / 3, name;
      if (aD >= aW && aD >= aC) name = Dp < 0 ? (warm ? "Light Spring" : "Light Summer") : (warm ? "Deep Autumn" : "Deep Winter");
      else if (aC >= aW) name = C > 0 ? (warm ? "Bright Spring" : "Bright Winter") : (warm ? "Soft Autumn" : "Soft Summer");
      else name = warm ? (Dp <= 0 && C >= 0 ? "Warm Spring" : "Warm Autumn") : (Dp <= 0 || C < 0 ? "Cool Summer" : "Cool Winter");
      var s = SEASONS[name];
      show($("#cs-result"), '<p class="eyebrow">Your colour season</p><h2 class="result-title">' + name + '</h2><p>' + s.d + '</p><div class="swatch-row">' +
        s.c.map(function (h) { return '<button class="sw" type="button" data-copy="' + h + '" style="border:0;background:none;padding:0;cursor:pointer"><i style="background:' + h + '"></i><small>' + h + "</small></button>"; }).join("") +
        "</div><p style='margin-top:14px'><strong>Best neutrals:</strong> " + s.n.join(", ") + "<br><strong>Use sparingly near the face:</strong> " + s.x + '.</p><p class="small muted">Tap a swatch to copy its hex code. Results are a guide; lighting and makeup affect perception.</p><div class="btn-row no-print"><button type="button" class="btn btn-ghost" onclick="window.print()">Print my palette</button><a class="btn btn-accent" href="' + R + 'get-styled/?service=color-analysis">Book a professional colour analysis</a></div>');
      LS.set("as-season", name);
    });
  };

  /* ================= BODY SHAPE ================= */
  var BODY = {
    "Hourglass": "Bust and hips are balanced with a clearly defined waist. Emphasise the waist: wrap dresses, belted coats, high-rise trousers and tailored fits.",
    "Pear (Triangle)": "Hips are wider than bust and shoulders. Draw the eye up and balance the shoulders: boat necks, structured shoulders, A-line skirts, darker bottoms.",
    "Inverted Triangle": "Shoulders or bust are wider than hips. Add volume below: wide-leg trousers, A-line and full skirts; keep tops simple with V-necks.",
    "Rectangle": "Bust, waist and hips are similar. Create curves or play with lines: peplums, belts, layering, cropped jackets and textured fabrics.",
    "Apple (Round)": "Fuller through the middle with slimmer legs. Choose long vertical lines: open layers, empire waists, V-necks, straight-leg trousers and great shoes.",
    "Trapezoid": "Shoulders and chest slightly wider than the waist: the most balanced male shape. Most cuts work; slim-fit shirts and tailored jackets highlight it.",
    "Triangle": "Wider through the hips and waist than the chest. Build the shoulders: structured blazers, horizontal stripes up top, straight darker trousers.",
    "Oval": "Fuller through the midsection. Choose vertical lines and structure: single-breasted jackets, darker tones, open collars and fitted (not tight) shirts."
  };
  TOOLS["body-shape"] = function () {
    var sex = $("#bs-type");
    function lab() { var m = sex.value === "m"; $("#bs-l1").textContent = m ? "Chest" : "Bust"; $("#bs-l3").textContent = "Hips"; }
    sex.addEventListener("change", lab); lab();
    $("#bs-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var b = num("bs-1"), w = num("bs-2"), h = num("bs-3"); if (!b || !w || !h) return AS.toast("Enter all three measurements");
      var name;
      if (sex.value === "m") {
        if (w >= b * 1.02) name = "Oval"; else if (h > b * 1.05) name = "Triangle"; else if (b / w >= 1.25) name = "Inverted Triangle"; else if (b / w >= 1.1) name = "Trapezoid"; else name = "Rectangle";
      } else {
        if (w >= b * 0.9 && w >= h * 0.85) name = "Apple (Round)";
        else if (Math.abs(b - h) / h <= 0.05 && w / b <= 0.75 && w / h <= 0.75) name = "Hourglass";
        else if (h / b >= 1.05) name = "Pear (Triangle)";
        else if (b / h >= 1.05) name = "Inverted Triangle";
        else name = "Rectangle";
      }
      var txt = BODY[name];
      if (name === "Inverted Triangle" && sex.value === "m") txt = "Broad shoulders and chest with a narrow waist: the athletic V. Balance with straight or slightly relaxed trousers and avoid heavy shoulder padding.";
      if (name === "Rectangle" && sex.value === "m") txt = "Shoulders, chest and waist are similar. Add shape with structured jackets, layering and slightly tapered trousers.";
      show($("#bs-result"), '<p class="eyebrow">Your body shape</p><h2 class="result-title">' + name + "</h2><p>" + txt + '</p><p class="small muted">Ratios used: ' + (sex.value === "m" ? "chest" : "bust") + "/waist " + (b / w).toFixed(2) + ", hips/" + (sex.value === "m" ? "chest" : "bust") + " " + (h / b).toFixed(2) + '. Shapes describe proportions, not size, and every shape can wear any style.</p><a class="btn btn-accent" href="' + R + 'get-styled/?service=personal-styling">Get a stylist who dresses your shape</a>');
    });
  };

  /* ================= FACE SHAPE ================= */
  var FACE = {
    Oval: ["Balanced proportions; length about one and a half times the width.", ["bob", "curtain-bangs", "textured-crop"], "Most frame shapes work; try bold square or geometric frames."],
    Round: ["Similar length and width with a soft jaw.", ["textured-crop", "taper-fade", "butterfly-cut"], "Angular, rectangular frames add definition."],
    Square: ["Strong, angular jaw with similar widths.", ["curtain-bangs", "shag", "wolf-cut"], "Round or oval frames soften angles."],
    Oblong: ["Face is clearly longer than it is wide.", ["curtain-bangs", "bob", "shag"], "Tall, oversized frames balance length."],
    Heart: ["Wider forehead tapering to a narrower chin.", ["pixie-cut", "curtain-bangs", "bob"], "Bottom-heavy or rimless frames balance the forehead."],
    Diamond: ["Wide cheekbones with a narrower forehead and jaw.", ["wolf-cut", "shag", "curtain-bangs"], "Oval or cat-eye frames highlight cheekbones."]
  };
  TOOLS["face-shape"] = function () {
    $("#fs-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var fh = num("fs-fh"), cb = num("fs-cb"), jw = num("fs-jw"), L = num("fs-len"), jaw = $("#fs-jaw").value;
      if (!fh || !cb || !jw || !L) return AS.toast("Enter all four measurements");
      var ratio = L / cb, name;
      if (cb > fh * 1.08 && cb > jw * 1.1 && jaw === "pointed") name = "Diamond";
      else if (fh >= cb * 0.97 && fh > jw * 1.15 && jaw === "pointed") name = "Heart";
      else if (ratio >= 1.55) name = jaw === "square" || ratio > 1.7 ? "Oblong" : "Oval";
      else if (ratio < 1.3) name = jaw === "square" ? "Square" : "Round";
      else name = jaw === "square" && Math.abs(fh - jw) / jw < 0.12 ? "Square" : "Oval";
      var F = FACE[name];
      AS.data("styles").then(function (S) {
        var cuts = F[1].map(function (s) { return S.filter(function (x) { return x.s === s; })[0]; }).filter(Boolean);
        show($("#fs-result"), '<p class="eyebrow">Your face shape</p><h2 class="result-title">' + name + "</h2><p>" + F[0] + ' (length-to-cheekbone ratio ' + ratio.toFixed(2) + ').</p><h3>Cuts to try</h3><div class="grid g3" style="margin:10px 0 16px">' + cuts.map(function (c) {
          return '<a class="match" style="grid-template-columns:50px 1fr" href="' + R + "styles/" + c.s + '/"><div class="mini">' + pal(c.c) + "</div><div><b>" + esc(c.n) + "</b></div></a>";
        }).join("") + "</div><p><strong>Glasses:</strong> " + F[2] + '</p><a class="btn btn-accent" href="' + R + 'get-styled/?service=hair-makeup">Find a stylist for my face shape</a>');
      });
    });
  };

  /* ================= SIZE CONVERTER ================= */
  var SIZES = {
    "Women's clothing": { cols: ["US", "UK", "EU", "AU", "JP", "Letter"], rows: [["0", "4", "32", "4", "3", "XXS"], ["2", "6", "34", "6", "5", "XS"], ["4", "8", "36", "8", "7", "S"], ["6", "10", "38", "10", "9", "S"], ["8", "12", "40", "12", "11", "M"], ["10", "14", "42", "14", "13", "M"], ["12", "16", "44", "16", "15", "L"], ["14", "18", "46", "18", "17", "L"], ["16", "20", "48", "20", "19", "XL"], ["18", "22", "50", "22", "21", "XXL"], ["20", "24", "52", "24", "23", "XXL"]] },
    "Men's suits & jackets": { cols: ["US/UK chest (in)", "EU", "Letter"], rows: [["34", "44", "XS"], ["36", "46", "S"], ["38", "48", "M"], ["40", "50", "M"], ["42", "52", "L"], ["44", "54", "L"], ["46", "56", "XL"], ["48", "58", "XXL"], ["50", "60", "XXL"]] },
    "Men's shirts (collar)": { cols: ["US/UK (in)", "EU (cm)", "Letter"], rows: [["14", "36", "S"], ["14.5", "37", "S"], ["15", "38", "M"], ["15.5", "39", "M"], ["16", "41", "L"], ["16.5", "42", "L"], ["17", "43", "XL"], ["17.5", "44", "XL"], ["18", "46", "XXL"]] },
    "Women's shoes": { cols: ["US", "UK", "EU", "Foot length (cm)"], rows: [["5", "3", "35.5", "22.0"], ["5.5", "3.5", "36", "22.5"], ["6", "4", "36.5", "22.9"], ["6.5", "4.5", "37", "23.3"], ["7", "5", "37.5", "23.7"], ["7.5", "5.5", "38", "24.1"], ["8", "6", "38.5", "24.5"], ["8.5", "6.5", "39", "25.0"], ["9", "7", "40", "25.4"], ["9.5", "7.5", "40.5", "25.8"], ["10", "8", "41", "26.2"], ["11", "9", "42", "27.1"]] },
    "Men's shoes": { cols: ["US", "UK", "EU", "Foot length (cm)"], rows: [["7", "6", "40", "25.0"], ["7.5", "6.5", "40.5", "25.4"], ["8", "7", "41", "25.8"], ["8.5", "7.5", "42", "26.2"], ["9", "8", "42.5", "26.7"], ["9.5", "8.5", "43", "27.1"], ["10", "9", "44", "27.5"], ["10.5", "9.5", "44.5", "27.9"], ["11", "10", "45", "28.3"], ["12", "11", "46", "29.2"], ["13", "12", "47", "30.0"]] }
  };
  TOOLS["size-converter"] = function () {
    var cat = $("#sz-cat"), sys = $("#sz-sys"), val = $("#sz-val"), out = $("#sz-out");
    cat.innerHTML = Object.keys(SIZES).map(function (k) { return "<option>" + k + "</option>"; }).join("");
    function fillSys() { var t = SIZES[cat.value]; sys.innerHTML = t.cols.map(function (c, i) { return '<option value="' + i + '">' + c + "</option>"; }).join(""); fillVal(); }
    function fillVal() { var t = SIZES[cat.value], i = +sys.value; var seen = {}; val.innerHTML = t.rows.map(function (r, k) { if (seen[r[i]]) return ""; seen[r[i]] = 1; return '<option value="' + k + '">' + r[i] + "</option>"; }).join(""); draw(); }
    function draw() {
      var t = SIZES[cat.value], k = +val.value;
      out.innerHTML = '<div class="grid g4" style="margin:6px 0 18px">' + t.cols.map(function (c, i) { return '<div class="card" style="padding:14px"><div class="small muted">' + c + '</div><div class="result-title" style="font-size:1.6rem">' + t.rows[k][i] + "</div></div>"; }).join("") +
        '</div><div class="table-wrap"><table><thead><tr>' + t.cols.map(function (c) { return "<th>" + c + "</th>"; }).join("") + "</tr></thead><tbody>" +
        t.rows.map(function (r, i) { return "<tr" + (i === k ? ' style="background:var(--accent-soft)"' : "") + ">" + r.map(function (x) { return "<td>" + x + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody></table></div>";
    }
    cat.addEventListener("change", fillSys); sys.addEventListener("change", fillVal); val.addEventListener("change", draw); fillSys();
  };

  /* ================= CAPSULE BUILDER ================= */
  var CAP = {
    tops: { office: ["Crisp white shirt", "Silk or satin blouse", "Fine-gauge knit", "Striped shirt", "Fitted tee", "Turtleneck", "Shell top", "Polo knit", "Light blue shirt", "Printed blouse"], casual: ["White tee", "Striped Breton top", "Grey sweatshirt", "Chunky knit", "Linen shirt", "Black tee", "Tank top", "Denim shirt", "Long-sleeve tee", "Hoodie"], creative: ["Boxy tee", "Oversized shirt", "Statement knit", "Graphic tee", "Silk camisole", "Turtleneck", "Cropped cardigan", "Mesh or texture top", "Vest", "Printed shirt"], travel: ["Merino tee", "Packable shirt", "Lightweight knit", "Tank top", "Long-sleeve tee", "Button-down", "Wrinkle-free blouse", "Hoodie", "Polo", "Camisole"] },
    bottoms: { office: ["Tailored trousers (base)", "Tailored trousers (neutral 2)", "Pencil or midi skirt", "Dark straight jeans", "Wide-leg trousers", "Chinos"], casual: ["Straight jeans", "Wide-leg jeans", "Chinos", "Midi skirt", "Shorts (season)", "Joggers"], creative: ["Wide-leg trousers", "Cargo pants", "Barrel or vintage jeans", "Slip skirt", "Pleated trousers", "Shorts or culottes"], travel: ["Stretch trousers", "Dark jeans", "Packable skirt", "Shorts (season)", "Joggers", "Linen trousers"] },
    layers: ["Blazer", "Cardigan or knit layer", "Trench or rain jacket", "Wool coat (cold) / denim jacket (warm)"],
    shoes: { office: ["Loafers", "Block heels or derbies", "Clean leather sneakers", "Ankle boots (cold) / sandals (warm)"], casual: ["White sneakers", "Loafers", "Boots (cold) / sandals (warm)", "Ballet flats or slides"], creative: ["Chunky loafers", "Statement sneakers", "Boots", "Mary Janes or mules"], travel: ["Walking sneakers", "Packable flats", "Sandals or boots", "Smart shoe"] },
    extras: ["Leather bag", "Tote", "Belt", "Scarf", "Sunglasses", "Statement jewellery"]
  };
  TOOLS.capsule = function () {
    var out = $("#cap-out"), state = LS.get("as-capsule-ticks", {});
    $("#cap-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var f = new FormData(e.target), life = f.get("life"), size = +f.get("size"), base = f.get("base"), acc = f.get("accent"), season = f.get("season");
      if (life === "mixed") life = "office";
      var ratio = size === 15 ? [5, 3, 2, 3, 2] : size === 25 ? [8, 5, 4, 4, 4] : [10, 6, 4, 4, 6];
      var groups = [["Tops", CAP.tops[life].slice(0, ratio[0])], ["Bottoms", CAP.bottoms[life].slice(0, ratio[1])], ["Layers", CAP.layers.slice(0, ratio[2])], ["Shoes", CAP.shoes[life].slice(0, ratio[3])], ["Bags & accessories", CAP.extras.slice(0, ratio[4])]];
      if (season === "warm") groups.forEach(function (g) { g[1] = g[1].map(function (x) { return x.replace(/ \(cold\) \/ ([^,]+) \(warm\)/, " → $1").replace(/Wool coat \(cold\) \/ /, ""); }); });
      if (season === "cold") groups.forEach(function (g) { g[1] = g[1].map(function (x) { return x.replace(/ \(cold\) \/ [^,]+ \(warm\)/, "").replace(/Shorts \(season\)/, "Corduroy trousers"); }); });
      var total = groups.reduce(function (s, g) { return s + g[1].length; }, 0);
      var combos = groups[0][1].length * groups[1][1].length * Math.max(1, groups[2][1].length) * Math.max(1, groups[3][1].length);
      show(out, '<p class="eyebrow">Your capsule</p><h2 class="result-title">' + total + "-piece " + life + " capsule</h2><p>Palette: <strong>" + base + "</strong> base + cream/white + denim neutrals, with <span style=\"display:inline-block;width:14px;height:14px;border-radius:4px;vertical-align:-2px;background:" + acc + '"></span> accent. That is roughly <strong>' + combos.toLocaleString() + "</strong> top-bottom-layer-shoe combinations.</p>" +
        groups.map(function (g) { return "<h3 style='margin-top:18px'>" + g[0] + ' <span class="small muted">(' + g[1].length + ')</span></h3><ul class="checklist">' + g[1].map(function (it) { var id = (g[0] + it).replace(/\W/g, ""); return '<li><label class="check"><input type="checkbox" data-tick="' + id + '"' + (state[id] ? " checked" : "") + "> " + esc(it) + "</label></li>"; }).join("") + "</ul>"; }).join("") +
        '<div class="btn-row no-print" style="margin-top:18px"><button type="button" class="btn btn-ghost" onclick="window.print()">Print checklist</button><a class="btn btn-accent" href="' + R + 'get-styled/?service=wardrobe-edit">Book a wardrobe edit</a></div>');
      $$("[data-tick]", out).forEach(function (c) { c.addEventListener("change", function () { state[c.getAttribute("data-tick")] = c.checked; LS.set("as-capsule-ticks", state); }); });
    });
  };

  /* ================= OUTFIT SHUFFLER ================= */
  var STARTER = [["White tee", "top", "#F5F5F2"], ["Navy knit", "top", "#22304A"], ["Striped shirt", "top", "#DDE3EC"], ["Black turtleneck", "top", "#161616"], ["Camel blouse", "top", "#C19A6B"], ["Dark jeans", "bottom", "#2E3B55"], ["Black trousers", "bottom", "#1A1A1A"], ["Stone chinos", "bottom", "#CFC5B4"], ["Olive skirt", "bottom", "#6B6B3A"], ["White sneakers", "shoes", "#FAFAFA"], ["Brown loafers", "shoes", "#6B4429"], ["Black boots", "shoes", "#151515"], ["Navy blazer", "layer", "#1F2A44"], ["Trench coat", "layer", "#C8B48A"], ["Grey cardigan", "layer", "#9A9A9A"], ["Gold hoops", "accessory", "#C9A24D"], ["Silk scarf", "accessory", "#A3262A"], ["Leather tote", "accessory", "#7A5532"]];
  function isNeutral(hex) {
    var r = parseInt(hex.substr(1, 2), 16) / 255, g = parseInt(hex.substr(3, 2), 16) / 255, b = parseInt(hex.substr(5, 2), 16) / 255;
    var mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, s = mx === mn ? 0 : (l > .5 ? (mx - mn) / (2 - mx - mn) : (mx - mn) / (mx + mn));
    return s < 0.28 || l < 0.18 || l > 0.9 || (r > g && g > b && s < 0.45 && l > 0.3 && l < 0.8); // greys, black, white, browns/tans
  }
  TOOLS["outfit-shuffle"] = function () {
    var wd = LS.get("as-wardrobe", null) || STARTER.slice(), locks = {}, current = {}, cats = ["top", "bottom", "shoes", "layer", "accessory"];
    var grid = $("#os-grid"), list = $("#os-list"), note = $("#os-note");
    function save() { LS.set("as-wardrobe", wd); }
    function pick(c) { var opts = wd.filter(function (x) { return x[1] === c; }); return opts.length ? opts[Math.floor(Math.random() * opts.length)] : null; }
    function shuffle() {
      for (var tries = 0; tries < 40; tries++) {
        var o = {}; cats.forEach(function (c) { o[c] = locks[c] ? current[c] : pick(c); });
        var colours = cats.map(function (c) { return o[c] && o[c][2]; }).filter(Boolean).filter(function (h) { return !isNeutral(h); });
        if (colours.length <= 2 || tries === 39) { current = o; break; }
      }
      grid.innerHTML = cats.map(function (c) {
        var it = current[c];
        return '<div class="piece"><button type="button" class="lock" data-lock="' + c + '" aria-pressed="' + (locks[c] ? "true" : "false") + '">' + (locks[c] ? "Locked" : "Lock") + '</button><div class="dot" style="background:' + (it ? it[2] : "transparent") + '"></div><div class="small muted" style="text-transform:capitalize">' + c + "</div><strong>" + (it ? esc(it[0]) : "—") + "</strong></div>";
      }).join("");
      $$("[data-lock]", grid).forEach(function (b) { b.addEventListener("click", function () { var c = b.getAttribute("data-lock"); locks[c] = !locks[c]; b.setAttribute("aria-pressed", locks[c] ? "true" : "false"); b.textContent = locks[c] ? "Locked" : "Lock"; }); });
      var counts = cats.map(function (c) { return Math.max(1, wd.filter(function (x) { return x[1] === c; }).length); });
      note.textContent = "Your wardrobe can make about " + counts.reduce(function (a, b) { return a * b; }, 1).toLocaleString() + " outfits (one item per category). Shuffles keep to two or fewer non-neutral colours.";
    }
    function drawList() {
      list.innerHTML = cats.map(function (c) {
        return "<div><strong style='text-transform:capitalize'>" + c + "</strong><div class='chips' style='margin-top:6px'>" + wd.map(function (x, i) { return x[1] !== c ? "" : '<span class="badge" style="display:inline-flex;gap:6px;align-items:center"><i style="width:12px;height:12px;border-radius:50%;background:' + x[2] + ';display:inline-block;box-shadow:inset 0 0 0 1px rgba(0,0,0,.15)"></i>' + esc(x[0]) + ' <button type="button" data-del="' + i + '" style="border:0;background:none;cursor:pointer;color:var(--muted)" aria-label="Remove">×</button></span>'; }).join("") + "</div></div>";
      }).join("");
      $$("[data-del]", list).forEach(function (b) { b.addEventListener("click", function () { wd.splice(+b.getAttribute("data-del"), 1); save(); drawList(); }); });
    }
    $("#os-add").addEventListener("submit", function (e) {
      e.preventDefault(); var n = $("#os-name").value.trim(); if (!n) return;
      wd.push([n, $("#os-cat").value, $("#os-col").value]); save(); drawList(); e.target.reset(); AS.toast("Added " + n);
    });
    $("#os-shuffle").addEventListener("click", shuffle);
    $("#os-reset").addEventListener("click", function () { wd = STARTER.slice(); save(); drawList(); shuffle(); });
    drawList(); shuffle();
  };

  /* ================= DRESS CODE DECODER ================= */
  var CODES = [
    ["White Tie", 10, "white-tie", ["Black tailcoat, white piqué waistcoat and bow tie, wing-collar shirt, patent shoes", "Floor-length evening gown, long gloves optional, fine jewellery", "The most formal evening wear available; hire specialist pieces if needed"], ["Tuxedos", "Short or cocktail dresses", "Day suits"]],
    ["Black Tie", 9, "black-tie", ["Tuxedo with black bow tie, white dress shirt, black patent or polished shoes", "Floor-length gown or a very elegant formal cocktail dress", "Formal evening wear in rich fabrics: velvet, satin, silk"], ["Business suits", "Casual fabrics like cotton jersey", "Sneakers"]],
    ["Black Tie Optional", 8, "black-tie", ["Tuxedo, or a dark well-tailored suit with tie", "Gown, formal cocktail dress or elegant evening separates", "Formal evening wear; dark colours are safest"], ["Light-coloured casual suits", "Day dresses", "Open-toe casual sandals"]],
    ["Cocktail / Semi-formal", 6, "cocktail-attire", ["Dark suit; tie often optional", "Knee-to-midi dress, dressy jumpsuit or elegant separates", "Polished, festive outfit with some personality"], ["Jeans", "Floor-length gowns (usually)", "Sneakers"]],
    ["Festive Attire", 6, "festive-attire", ["Suit in a seasonal colour or velvet jacket", "Sequins, velvet or jewel-tone dress", "Cocktail outfit plus sparkle or seasonal colour"], ["Novelty sweaters unless invited", "Head-to-toe glitter at a dinner"]],
    ["Business Formal", 7, "business-formal-dress", ["Dark matching suit, dress shirt, conservative tie, leather shoes", "Tailored suit, sheath dress or skirt suit, closed shoes", "Dark, matching, tailored and conservative"], ["Loud patterns", "Casual shoes", "Bare shoulders in conservative settings"]],
    ["Business Casual", 5, "business-casual", ["Chinos or trousers with a shirt or knit, optional blazer", "Trousers or skirt with blouse or knit, smart flats or heels", "Tailored but tie-free; neutral palette"], ["Athletic wear", "Ripped jeans", "Slogans and logos"]],
    ["Smart Casual", 4, "smart-casual-dress", ["Dark jeans or chinos, blazer or overshirt, loafers or clean leather sneakers", "Dark jeans or trousers with a nice top, midi skirt, loafers or ankle boots", "One smart piece plus one casual piece"], ["Gym wear", "Flip-flops", "Full suit and tie (too formal)"]],
    ["Garden Party", 5, "cocktail-attire", ["Light suit (linen or cotton), open collar or light tie, loafers", "Floral or pastel midi dress, block heels or wedges", "Light fabrics and colours; shoes that cope with grass"], ["Stilettos", "Heavy dark wool", "Very casual shorts"]],
    ["Beach Formal", 5, "smart-casual-dress", ["Linen suit or trousers with a dress shirt, no tie, loafers or dressy sandals", "Flowing maxi or midi dress, flat sandals", "Breathable, elegant, sand-friendly"], ["Stilettos", "Heavy suits", "Swimwear"]],
    ["Casual", 2, "smart-casual-dress", ["Clean jeans, tee or polo, sneakers", "Jeans or casual dress, sneakers or sandals", "Comfortable but clean and intentional"], ["Anything stained or torn", "Pyjama-style loungewear (unless stated)"]]
  ];
  TOOLS["dress-code"] = function () {
    var sel = $("#dc-sel"), out = $("#dc-out");
    sel.innerHTML = CODES.map(function (c, i) { return '<option value="' + i + '">' + c[0] + "</option>"; }).join("");
    var q = new URLSearchParams(location.search).get("code"); if (q) CODES.forEach(function (c, i) { if (c[0].toLowerCase().indexOf(q.toLowerCase()) === 0) sel.value = i; });
    function draw() {
      var c = CODES[+sel.value];
      show(out, '<p class="eyebrow">Formality ' + c[1] + '/10</p><h2 class="result-title">' + c[0] + '</h2><div class="meter" style="margin:8px 0 18px"><i style="width:' + c[1] * 10 + '%"></i></div><div class="grid g3"><div class="card"><h3>Suits &amp; menswear</h3><p>' + c[3][0] + '</p></div><div class="card"><h3>Dresses &amp; womenswear</h3><p>' + c[3][1] + '</p></div><div class="card"><h3>Any outfit</h3><p>' + c[3][2] + '</p></div></div><h3 style="margin-top:18px">Avoid</h3><ul class="ticks crosses">' + c[4].map(function (x) { return "<li>" + x + "</li>"; }).join("") + '</ul><p class="btn-row" style="margin-top:16px"><a class="btn btn-ghost" href="' + R + "styles/" + c[2] + '/">Read the full guide</a><a class="btn btn-accent" href="' + R + 'get-styled/?service=event-styling">Get help styling my event</a></p>');
    }
    sel.addEventListener("change", draw); draw();
  };

  /* ================= PALETTE GENERATOR ================= */
  function hexToHsl(h) { var r = parseInt(h.substr(1, 2), 16) / 255, g = parseInt(h.substr(3, 2), 16) / 255, b = parseInt(h.substr(5, 2), 16) / 255, mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, s = 0, hu = 0; if (mx !== mn) { var d = mx - mn; s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn); hu = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; hu *= 60; } return [hu, s, l]; }
  function hslToHex(h, s, l) { h = ((h % 360) + 360) % 360; s = Math.max(0, Math.min(1, s)); l = Math.max(0, Math.min(1, l)); var c = (1 - Math.abs(2 * l - 1)) * s, x = c * (1 - Math.abs((h / 60) % 2 - 1)), m = l - c / 2, r = 0, g = 0, b = 0; if (h < 60) { r = c; g = x; } else if (h < 120) { r = x; g = c; } else if (h < 180) { g = c; b = x; } else if (h < 240) { g = x; b = c; } else if (h < 300) { r = x; b = c; } else { r = c; b = x; } return "#" + [r, g, b].map(function (v) { return ("0" + Math.round((v + m) * 255).toString(16)).slice(-2); }).join("").toUpperCase(); }
  TOOLS.palette = function () {
    var base = $("#pg-base"), sch = $("#pg-scheme"), out = $("#pg-out");
    function draw() {
      var hsl = hexToHsl(base.value), h = hsl[0], s = hsl[1], l = hsl[2], cols;
      var neutral = hslToHex(h, Math.min(s, .12), .93), deep = hslToHex(h, Math.min(s, .35), .18);
      if (sch.value === "analogous") cols = [neutral, base.value, hslToHex(h + 30, s, l), hslToHex(h - 30, s * .9, Math.min(.85, l + .12)), deep];
      else if (sch.value === "complementary") cols = [neutral, base.value, hslToHex(h + 180, s * .85, l), hslToHex(h, s * .5, Math.min(.88, l + .25)), deep];
      else if (sch.value === "triadic") cols = [neutral, base.value, hslToHex(h + 120, s * .8, l), hslToHex(h + 240, s * .8, l), deep];
      else cols = [neutral, hslToHex(h, s * .55, Math.min(.85, l + .2)), base.value, hslToHex(h, s, Math.max(.12, l - .2)), deep];
      var roles = ["60% · walls, large surfaces or main garment", "30% · upholstery, rugs or second garment", "10% · accent: cushions, art, shoes", "Accent 2 · small doses", "Anchor · trims, frames, text"];
      show(out, '<div class="palette" style="height:110px">' + cols.map(function (c, i) { return '<span style="background:' + c + ";flex:" + [6, 3, 1, 1, 1][i] + '"></span>'; }).join("") + '</div><div class="pal-list">' + cols.map(function (c, i) { return '<button type="button" data-copy="' + c + '"><i style="background:' + c + '"></i><b>' + c + "</b><code>" + roles[i] + "</code></button>"; }).join("") + '</div><p class="small muted" style="margin-top:10px">Tap a colour to copy. The top bar shows the classic 60-30-10 proportion.</p>');
    }
    base.addEventListener("input", draw); sch.addEventListener("change", draw); draw();
  };

  /* ================= MAKEOVER BUDGET PLANNER ================= */
  var SPLITS = {
    living: [["Seating (sofa, chairs)", 35], ["Tables & storage", 15], ["Lighting", 10], ["Rug", 10], ["Window treatments", 7], ["Art & decor", 8], ["Paint & small fixes", 5], ["Contingency", 10]],
    bedroom: [["Bed frame & mattress", 40], ["Bedding & textiles", 12], ["Storage & dressers", 13], ["Lighting", 8], ["Rug", 7], ["Window treatments", 5], ["Paint & decor", 5], ["Contingency", 10]],
    dining: [["Table", 30], ["Chairs", 25], ["Lighting (statement pendant)", 12], ["Rug", 8], ["Storage / sideboard", 10], ["Art & decor", 5], ["Contingency", 10]],
    office: [["Desk", 22], ["Ergonomic chair", 25], ["Storage & shelving", 15], ["Lighting", 10], ["Tech & cable management", 8], ["Decor & plants", 10], ["Contingency", 10]],
    kitchen: [["Paint or cabinet refinish", 25], ["Hardware & fixtures", 15], ["Lighting", 15], ["Backsplash or wall finish", 20], ["Textiles & accessories", 5], ["Small appliances & storage", 10], ["Contingency", 10]]
  };
  TOOLS.budget = function () {
    $("#bp-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var total = num("bp-total"), cur = $("#bp-cur").value, room = $("#bp-room").value, fee = num("bp-fee") || 0;
      if (!total || total <= 0) return AS.toast("Enter your total budget");
      var design = total * fee / 100, rest = total - design, sp = SPLITS[room];
      var fmt = function (v) { return cur + Math.round(v).toLocaleString(); };
      show($("#bp-out"), '<p class="eyebrow">Your plan</p><h2 class="result-title">' + fmt(total) + " " + $("#bp-room").selectedOptions[0].text.toLowerCase() + " makeover</h2>" + (fee ? "<p>Design fee set aside (" + fee + "%): <strong>" + fmt(design) + "</strong>. Remaining for the room: <strong>" + fmt(rest) + "</strong>.</p>" : "") +
        '<div class="alloc" style="margin:14px 0">' + sp.map(function (x) { return "<div><span>" + x[0] + '</span><div class="meter"><i style="width:' + x[1] * 2.5 + '%"></i></div><strong>' + fmt(rest * x[1] / 100) + "</strong></div>"; }).join("") +
        '</div><p class="small muted">Splits are a planning starting point based on where each room\'s money typically goes (big anchor pieces first, 10% contingency). Adjust to your priorities.</p><a class="btn btn-accent" href="' + R + "get-styled/?service=interior-room&budget=" + encodeURIComponent(fmt(total)) + '">Get a designer to plan this budget</a>');
    });
  };

  if (TOOLS[tool]) TOOLS[tool]();
})();
