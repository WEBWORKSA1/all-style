/* All-Style core script: theme, nav, search, forms, consent, video, board, sticky CTA. No dependencies. */
(function () {
  "use strict";
  var D = document, W = window, R = D.documentElement.getAttribute("data-root") || "./";
  var LS = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  W.AS = W.AS || {};
  AS.root = R; AS.LS = LS;
  var $ = function (s, c) { return (c || D).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || D).querySelectorAll(s)); };
  AS.$ = $; AS.$$ = $$;
  AS.esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };

  /* ---------- Toast ---------- */
  var toastEl;
  AS.toast = function (msg) {
    if (!toastEl) { toastEl = D.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); D.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove("show"); }, 2600);
  };

  /* ---------- Theme ---------- */
  var themeBtn = $("#theme-btn");
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var t = D.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    D.documentElement.setAttribute("data-theme", t); LS.set("as-theme", t);
  });

  /* ---------- Mobile nav ---------- */
  var menuBtn = $("#menu-btn"), nav = $("#nav");
  if (menuBtn && nav) menuBtn.addEventListener("click", function () {
    var open = nav.classList.toggle("open"); menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  });

  /* ---------- Data loader (cached) ---------- */
  var cache = {};
  AS.data = function (name) {
    if (!cache[name]) cache[name] = fetch(R + "data/" + name + ".json", { cache: "no-cache" }).then(function (r) { if (!r.ok) throw 0; return r.json(); });
    return cache[name];
  };

  /* ---------- Search ---------- */
  var ov = $("#search-ov"), sInput = $("#search-input"), sRes = $("#search-res"), idx = null, sel = -1;
  function openSearch() {
    if (!ov) return; ov.classList.add("open"); sInput.value = ""; sRes.innerHTML = ""; sInput.focus();
    if (!idx) AS.data("search").then(function (d) { idx = d; render(""); }).catch(function () { sRes.innerHTML = '<p class="muted" style="padding:12px">Search is loading. Try again in a moment.</p>'; });
    else render("");
  }
  function closeSearch() { if (ov) ov.classList.remove("open"); }
  function score(item, q) {
    var t = item.t.toLowerCase(), k = (item.k || "").toLowerCase();
    if (!q) return 1; if (t === q) return 100; if (t.indexOf(q) === 0) return 60; if (t.indexOf(q) > -1) return 40;
    var parts = q.split(/\s+/), s = 0;
    for (var i = 0; i < parts.length; i++) { if (!parts[i]) continue; if (t.indexOf(parts[i]) > -1) s += 12; else if (k.indexOf(parts[i]) > -1) s += 6; else return 0; }
    return s;
  }
  function render(q) {
    if (!idx) return; q = q.trim().toLowerCase();
    var list = idx.map(function (it) { return [score(it, q), it]; }).filter(function (x) { return x[0] > 0; })
      .sort(function (a, b) { return b[0] - a[0]; }).slice(0, q ? 12 : 8);
    sel = -1;
    sRes.innerHTML = list.length ? list.map(function (x) { return '<a href="' + R + x[1].u + '"><span>' + AS.esc(x[1].t) + '</span><small>' + AS.esc(x[1].c) + "</small></a>"; }).join("")
      : '<p class="muted" style="padding:12px">No match. Try "japandi", "black tie" or "colour".</p>';
  }
  $$("[data-search-open]").forEach(function (b) { b.addEventListener("click", openSearch); });
  if (ov) {
    ov.addEventListener("click", function (e) { if (e.target === ov) closeSearch(); });
    sInput.addEventListener("input", function () { render(sInput.value); });
    sInput.addEventListener("keydown", function (e) {
      var links = $$("a", sRes);
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault(); sel = Math.max(0, Math.min(links.length - 1, sel + (e.key === "ArrowDown" ? 1 : -1)));
        links.forEach(function (l, i) { l.classList.toggle("sel", i === sel); });
      } else if (e.key === "Enter" && links.length) { (links[sel] || links[0]).click(); }
    });
  }
  D.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeSearch();
    if (e.key === "/" && !/input|textarea|select/i.test((D.activeElement || {}).tagName || "")) { e.preventDefault(); openSearch(); }
  });

  /* ---------- Consent ---------- */
  var cookie = $("#cookie");
  if (cookie && !LS.get("as-consent", null)) cookie.classList.add("show");
  $$("[data-consent]").forEach(function (b) {
    b.addEventListener("click", function () {
      LS.set("as-consent", b.getAttribute("data-consent"));
      if (cookie) cookie.classList.remove("show");
      if (b.getAttribute("data-consent") === "essential") { (W.adsbygoogle = W.adsbygoogle || []).requestNonPersonalizedAds = 1; }
      AS.toast("Preferences saved");
    });
  });

  /* ---------- Forms (FormSubmit AJAX; inbox assembled at runtime, never in markup) ---------- */
  var K = [116, 118, 106, 53, 115, 112, 104, 116, 110, 71, 56, 104, 122, 114, 121, 118, 126, 105, 108, 126];
  function inbox() { return String.fromCharCode.apply(null, K.slice().reverse().map(function (n) { return n - 7; })); }
  function collect(form) {
    var data = {}, fd = new FormData(form);
    fd.forEach(function (v, k) {
      if (k === "_hp") return;
      if (data[k] !== undefined) data[k] = data[k] + ", " + v; else data[k] = v;
    });
    return data;
  }
  function msg(form, cls, text) {
    var m = $(".form-msg", form) || (function () { var x = D.createElement("div"); x.className = "form-msg"; x.setAttribute("role", "status"); form.appendChild(x); return x; })();
    m.className = "form-msg " + cls; m.textContent = text;
  }
  AS.send = function (form, extra) {
    var hp = form.querySelector('[name="_hp"]');
    if (hp && hp.value) return Promise.resolve(true); // bot
    var data = collect(form), name = form.getAttribute("data-form") || "Form";
    Object.keys(extra || {}).forEach(function (k) { data[k] = extra[k]; });
    data._subject = "[All-Style] " + name + (data.name ? " — " + data.name : "");
    data._template = "table"; data._captcha = "false";
    data["Website"] = "All-Style"; data["Page"] = location.href; data["Submitted (UTC)"] = new Date().toISOString();
    if (data.email) data._replyto = data.email;
    return fetch("https://formsubmit.co/ajax/" + inbox(), {
      method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data)
    }).then(function (r) { return r.ok; }).catch(function () { return false; });
  };
  function validate(form, scope) {
    var ok = true;
    $$("input,select,textarea", scope || form).forEach(function (el) {
      if (el.closest(".step-panel") && !el.closest(".step-panel").classList.contains("active") && scope) return;
      if (!el.checkValidity()) { ok = false; }
    });
    if (!ok) { var bad = $$(":invalid", scope || form).filter(function (el) { return el.tagName !== "FORM" && el.tagName !== "FIELDSET"; })[0]; if (bad) { bad.reportValidity(); bad.focus(); } }
    // grouped checkbox requirement
    $$("[data-require-one]", scope || form).forEach(function (g) {
      if (ok && !$$("input:checked", g).length) { ok = false; AS.toast(g.getAttribute("data-require-one")); }
    });
    return ok;
  }
  $$("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validate(form)) return;
      var btn = form.querySelector('[type="submit"]'); if (btn) { btn.disabled = true; btn._t = btn.textContent; btn.textContent = "Sending…"; }
      AS.send(form).then(function (ok) {
        if (btn) { btn.disabled = false; btn.textContent = btn._t; }
        if (ok) {
          var done = form.getAttribute("data-done");
          var panel = done && $(done);
          if (panel) { form.hidden = true; panel.hidden = false; panel.scrollIntoView({ behavior: "smooth", block: "center" }); }
          else { msg(form, "ok", form.getAttribute("data-ok") || "Thank you! Your message has been received."); form.reset(); }
          LS.set("as-last-form", { f: form.getAttribute("data-form"), t: Date.now() });
        } else {
          msg(form, "err", "Sorry, that didn't go through. Please check your connection and try again.");
        }
      });
    });
  });

  /* ---------- Multi-step forms ---------- */
  $$("[data-steps]").forEach(function (form) {
    var panels = $$(".step-panel", form), bar = $(".progress i", form), lab = $("[data-step-label]", form), i = 0;
    function show(n) {
      i = n; panels.forEach(function (p, k) { p.classList.toggle("active", k === i); });
      if (bar) bar.style.width = ((i + 1) / panels.length * 100) + "%";
      if (lab) lab.textContent = "Step " + (i + 1) + " of " + panels.length;
      var top = form.getBoundingClientRect().top + W.scrollY - 110; if (W.scrollY > top) W.scrollTo({ top: top, behavior: "smooth" });
    }
    $$("[data-next]", form).forEach(function (b) { b.addEventListener("click", function () { if (validate(form, panels[i])) show(Math.min(i + 1, panels.length - 1)); }); });
    $$("[data-prev]", form).forEach(function (b) { b.addEventListener("click", function () { show(Math.max(i - 1, 0)); }); });
    show(0);
  });

  /* ---------- Prefill from URL ---------- */
  var qs = new URLSearchParams(location.search);
  $$("form[data-prefill]").forEach(function (form) {
    qs.forEach(function (v, k) {
      $$('[name="' + k + '"]', form).forEach(function (el) {
        if (el.type === "checkbox" || el.type === "radio") { v.split(",").forEach(function (x) { if (el.value === x) el.checked = true; }); }
        else if (!el.value) el.value = v;
      });
    });
    var quiz = LS.get("as-quiz", null), note = $("[data-quiz-note]", form);
    if (quiz && note && quiz.top && quiz.top.length) {
      note.hidden = false;
      note.innerHTML = "Your Style DNA: <strong>" + quiz.top.map(function (t) { return AS.esc(t.n) + " (" + t.p + "%)"; }).join(", ") + "</strong>. We'll share this with your matched pro.";
      var hid = $('[name="style_dna"]', form); if (hid) hid.value = quiz.top.map(function (t) { return t.n + " " + t.p + "%"; }).join("; ");
      quiz.top.forEach(function (t) { $$('input[name="styles"][value="' + t.s + '"]', form).forEach(function (c) { c.checked = true; }); });
    }
  });

  /* ---------- Lite YouTube ---------- */
  D.addEventListener("click", function (e) {
    var y = e.target.closest && e.target.closest(".yt[data-id]");
    if (!y || y.querySelector("iframe")) return;
    var f = D.createElement("iframe");
    f.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(y.getAttribute("data-id")) + "?autoplay=1&rel=0";
    f.title = y.getAttribute("data-title") || "YouTube video"; f.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"; f.allowFullscreen = true;
    y.appendChild(f);
  });
  $$(".yt[data-id]").forEach(function (y) { y.setAttribute("tabindex", "0"); y.setAttribute("role", "button"); y.addEventListener("keydown", function (e) { if (e.key === "Enter") y.click(); }); });

  /* ---------- Saved styles (My Board) ---------- */
  var heart = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 21s-7.5-4.6-10-9.2C.3 8.6 2.2 4.5 6 4.5c2.1 0 3.4 1.1 4 2.2.6-1.1 1.9-2.2 4-2.2 3.8 0 5.7 4.1 4 7.3C19.5 16.4 12 21 12 21z"/></svg>';
  AS.board = function () { return LS.get("as-board", []); };
  function syncSave() {
    var b = AS.board();
    $$("[data-save]").forEach(function (el) {
      var on = b.indexOf(el.getAttribute("data-save")) > -1;
      if (el.classList.contains("btn")) el.textContent = on ? "♥ Saved" : "♡ Save";
      else if (!el.innerHTML.trim()) el.innerHTML = heart;
      el.setAttribute("aria-pressed", on ? "true" : "false");
      el.setAttribute("aria-label", on ? "Remove from My Board" : "Save to My Board");
    });
    $$("[data-board-count]").forEach(function (el) { el.textContent = b.length; });
  }
  D.addEventListener("click", function (e) {
    var el = e.target.closest && e.target.closest("[data-save]"); if (!el) return;
    e.preventDefault(); e.stopPropagation();
    var s = el.getAttribute("data-save"), b = AS.board(), i = b.indexOf(s);
    if (i > -1) { b.splice(i, 1); AS.toast("Removed from My Board"); } else { b.push(s); AS.toast("Saved to My Board"); }
    LS.set("as-board", b); syncSave(); if (AS.renderBoard) AS.renderBoard();
  });
  syncSave();

  /* ---------- Style of the Day (client roll-over so it changes at midnight UTC even between rebuilds) ---------- */
  var dailyEl = $("[data-daily-auto]");
  if (dailyEl) AS.data("styles").then(function (list) {
    var day = Math.floor(Date.now() / 864e5), s = list[(day * 7919) % list.length];
    if (s && dailyEl.getAttribute("data-daily-auto") !== s.s) {
      $$("[data-daily-name]").forEach(function (e) { e.textContent = s.n; });
      $$("[data-daily-tag]").forEach(function (e) { e.textContent = s.t; });
      $$("[data-daily-link]").forEach(function (e) { e.href = R + "styles/" + s.s + "/"; });
      $$("[data-daily-pal]").forEach(function (e) { e.innerHTML = s.c.map(function (c) { return '<span style="background:' + c[1] + '"></span>'; }).join(""); });
    }
  }).catch(function () {});

  /* ---------- Copy hex ---------- */
  D.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-copy]"); if (!b) return;
    var v = b.getAttribute("data-copy");
    if (navigator.clipboard) navigator.clipboard.writeText(v).then(function () { AS.toast("Copied " + v); }); else AS.toast(v);
  });

  /* ---------- Sticky CTA ---------- */
  var sticky = $("#sticky-cta");
  if (sticky && !sessionStorage.getItem("as-cta-x")) {
    W.addEventListener("scroll", function () { sticky.classList.toggle("show", W.scrollY > 900 && (W.innerHeight + W.scrollY) < D.body.scrollHeight - 500); }, { passive: true });
    var x = $(".x", sticky); if (x) x.addEventListener("click", function () { sticky.remove(); try { sessionStorage.setItem("as-cta-x", 1); } catch (e) {} });
  }

  /* ---------- Atlas filter ---------- */
  var atlas = $("#atlas");
  if (atlas) {
    var cards = $$(".style-card", atlas), q = $("#atlas-q"), cur = qs.get("p") || "all";
    function apply() {
      var t = (q && q.value || "").toLowerCase().trim(), shown = 0;
      cards.forEach(function (c) {
        var ok = (cur === "all" || c.getAttribute("data-p") === cur) && (!t || c.getAttribute("data-k").indexOf(t) > -1);
        c.hidden = !ok; if (ok) shown++;
      });
      var cnt = $("#atlas-count"); if (cnt) cnt.textContent = shown + " styles";
      $$("[data-pf]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-pf") === cur ? "true" : "false"); });
    }
    $$("[data-pf]").forEach(function (b) { b.addEventListener("click", function () { cur = b.getAttribute("data-pf"); apply(); history.replaceState(null, "", cur === "all" ? location.pathname : "?p=" + cur); }); });
    if (q) q.addEventListener("input", apply);
    apply();
  }

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function (e) { e.textContent = new Date().getFullYear(); });
})();
