// Vorbereitete Werkzeugkiste für M2: nur ausführen, nicht lesen müssen.
// Sie verwendet Schreibweisen, die im Kurs bewusst NICHT vorkommen.
// Was sie tut: Zellen, die mit "<!-- index.html -->" oder "/* style.css */" beginnen,
// zeigen sofort die Oberfläche der Lernkarten-App in einem kleinen Fenster.
// Dazu kommen die Hilfen farbe(...) und kontrast(schrift, hintergrund).
(function () {
  var STANDARD_HTML = __HTML__;
  var dateien = { html: STANDARD_HTML, css: "/* style.css */\n" };

  // ---------- Ausgabe im Notebook selbst ----------
  function ausgabe(kanal, werte) {
    var text = Array.prototype.map.call(werte, function (w) { return String(w); }).join(" ");
    postMessage({ type: "stream", bundle: { name: kanal, text: text + "\n" } });
  }
  console.log = function () { ausgabe("stdout", arguments); };
  console.info = console.log;
  console.error = function () { ausgabe("stderr", arguments); };
  console.warn = console.error;

  function zeigeHtml(html, text) {
    postMessage({ type: "display_data", bundle: { data: { "text/html": html, "text/plain": text || "[Anzeige]" }, metadata: {}, transient: {} } });
  }
  function attribut(text) { return text.replace(/&/g, "&amp;").replace(/"/g, "&quot;"); }
  function htmlText(text) { return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function ohneKennung(text) {
    return text.replace(/^\s*(<!--\s*index\.html\s*-->|\/\*\s*style\.css\s*\*\/)[^\n]*\n?/, "");
  }
  function koerper(html) {
    var treffer = /<body[^>]*>([\s\S]*)<\/body>/i.exec(html);
    var inhalt = treffer ? treffer[1] : html;
    return inhalt.replace(/<script[^>]*src=["']?app\.js["']?[^>]*>\s*<\/script>/i, "");
  }

  // ---------- Hinweise zu style.css ----------
  function cssPruefen(css) {
    var funde = [];
    if (/display\s*:\s*grid/i.test(css)) { funde.push("display: grid (CSS Grid)"); }
    if (/position\s*:\s*absolute/i.test(css)) { funde.push("position: absolute"); }
    if (/\b(rgb|rgba|hsl|hsla)\s*\(/i.test(css)) { funde.push("Farben als rgb()/hsl() statt Hex-Wert"); }
    if (/(color|background-color|border)\s*:[^;}]*\b(red|blue|green|white|black|gray|grey|yellow|orange|purple|pink|brown|navy|silver|lightgray|lightgrey|darkgray|darkgrey)\b/i.test(css)) {
      funde.push("Farbnamen wie red oder white statt Hex-Werten");
    }
    for (var i = 0; i < funde.length; i++) {
      console.log("💬 " + funde[i] + " steht nicht auf unserer Liste. Wenn es klappt, behalten wir es – wenn nicht, zurück zur Liste.");
    }
  }

  // ---------- Läuft IM Fenster ----------
  function fensterSkript() {
    return "(" + function () {
      var rahmen = window.frameElement ? window.frameElement.closest(".lk-fenster") : null;
      var iframe = window.frameElement;
      function hoehe() {
        if (!iframe || !document.body) { return; }
        var unten = document.body.getBoundingClientRect().bottom + window.scrollY;
        var rand = parseFloat(getComputedStyle(document.body).marginBottom) || 0;
        var neu = Math.ceil(unten + rand) + "px";
        if (iframe.style.height !== neu) { iframe.style.height = neu; }
      }
      function verstanden() {
        var feld = rahmen ? rahmen.querySelector(".lk-css") : null;
        if (!feld) { return; }
        var stilKnoten = document.querySelector("style[data-lk='style.css']");
        if (!stilKnoten || !stilKnoten.sheet) { return; }
        var quelle = stilKnoten.textContent.replace(/\/\*[\s\S]*?\*\//g, function (k) { return k.replace(/[^\n]/g, " "); });
        var regeln = stilKnoten.sheet.cssRules;
        var zeilen = [];
        var pos = 0;
        if (regeln.length === 0) { zeilen.push("(keine einzige Regel: style.css ist leer)"); }
        for (var r = 0; r < regeln.length; r++) {
          var regel = regeln[r];
          if (!regel.selectorText) { continue; }
          var anzahl = 0;
          try { anzahl = document.querySelectorAll(regel.selectorText.replace(/:hover/g, "")).length; } catch (f) { anzahl = -1; }
          var hinweis = anzahl === 0 ? "   ⚠️ trifft kein einziges Element" : "   (trifft " + anzahl + (anzahl === 1 ? " Element)" : " Elemente)");
          var muster = new RegExp(regel.selectorText.replace(/[.*+?^${}()|[\]\\#]/g, "\\$&").replace(/\s+/g, "\\s*") + "\\s*\\{", "g");
          muster.lastIndex = pos;
          var t = muster.exec(quelle);
          zeilen.push(regel.selectorText + " {" + hinweis);
          if (!t) { zeilen.push("}"); continue; }
          var anfang = t.index + t[0].length;
          var zu = quelle.indexOf("}", anfang);
          var auf = quelle.indexOf("{", anfang);
          var offen = zu < 0 || (auf >= 0 && auf < zu);
          var ende = offen ? (auf >= 0 ? auf : quelle.length) : zu;
          var koerper = quelle.slice(anfang, ende);
          if (offen && auf >= 0) { koerper = koerper.slice(0, Math.max(koerper.lastIndexOf(";") + 1, 0)); }
          pos = offen ? anfang : zu + 1;
          var erklaerungen = koerper.split(";");
          for (var e = 0; e < erklaerungen.length; e++) {
            var text = erklaerungen[e].replace(/\s+/g, " ").trim();
            if (!text) { continue; }
            var doppel = text.indexOf(":");
            var name = doppel > 0 ? text.slice(0, doppel).trim().toLowerCase() : text;
            var probe = document.createElement("div").style;
            probe.cssText = text;
            var gut = doppel > 0 && probe.length > 0;
            zeilen.push((gut ? "  ✅ " : "  ❌ ") + text + (gut ? ";" : "      ← nicht verstanden, verworfen"));
          }
          if (offen) {
            zeilen.push("  ⚠️ Hier fehlt die schließende Klammer }. Alles Folgende rutscht in diese Regel.");
            break;
          }
          zeilen.push("}");
        }
        feld.textContent = zeilen.join("\n");
      }
      if (rahmen) {
        var regler = rahmen.querySelector(".lk-breite");
        var wert = rahmen.querySelector(".lk-breite-wert");
        if (regler) {
          regler.oninput = function () {
            iframe.style.width = regler.value + "px";
            if (wert) { wert.textContent = regler.value + " px"; }
          };
          if (regler.value !== regler.max) { regler.oninput(); }
        }
        var kisten = rahmen.querySelector(".lk-kisten");
        if (kisten) {
          var an = kisten.getAttribute("data-an") === "1";
          var stil = null;
          function setzen() {
            if (an && !stil) {
              stil = document.createElement("style");
              stil.textContent = "* { outline: 1px dashed #e0457b !important; }";
              document.head.appendChild(stil);
            }
            if (!an && stil) { stil.remove(); stil = null; }
            kisten.textContent = an ? "▣ Kisten ausblenden" : "▣ Kisten zeigen";
            kisten.setAttribute("data-an", an ? "1" : "0");
          }
          kisten.onclick = function () { an = !an; setzen(); };
          document.addEventListener("DOMContentLoaded", setzen);
        }
      }
      window.addEventListener("load", function () { hoehe(); verstanden(); });
      document.addEventListener("DOMContentLoaded", function () {
        new ResizeObserver(hoehe).observe(document.body);
      });
    }.toString() + ")();";
  }

  function fenster() {
    var css = ohneKennung(dateien.css);
    var dokument = "<!DOCTYPE html>\n<html lang=\"de\">\n<head>\n<meta charset=\"UTF-8\">\n" +
      "<style data-lk=\"style.css\">\n" + css + "\n</style>\n<script>" + fensterSkript() + "<\/script>\n</head>\n<body>\n" +
      koerper(ohneKennung(dateien.html)) + "\n</body>\n</html>";
    var knopf = "background:#4a4a4a;color:#f0f0f0;border:1px solid #6a6a6a;border-radius:5px;padding:2px 10px;font-size:12px;cursor:pointer;";
    var aussen =
      '<div class="lk-fenster" style="max-width:760px;border:1px solid #9e9e9e;border-radius:10px;overflow:hidden;' +
      'box-shadow:0 3px 12px rgba(0,0,0,.18);margin:6px 0;font-family:system-ui,sans-serif;">' +
      '<div style="background:#303030;color:#f0f0f0;padding:6px 12px;font-size:13px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">' +
      '<span>🗂️ Lernkarten</span>' +
      '<span style="display:flex;align-items:center;gap:10px;font-size:12px;">' +
      '<label style="display:flex;align-items:center;gap:6px;">↔ Fensterbreite <input class="lk-breite" type="range" min="280" max="760" step="10" value="760" style="width:120px;"></label>' +
      '<span class="lk-breite-wert" style="min-width:52px;opacity:.8;">760 px</span>' +
      '<button class="lk-kisten" data-an="0" style="' + knopf + '">▣ Kisten zeigen</button></span></div>' +
      '<div style="background:repeating-linear-gradient(45deg,#d8d8d8 0 8px,#e6e6e6 8px 16px);">' +
      '<iframe title="Lernkarten-Fenster" srcdoc="' + attribut(dokument) + '" ' +
      'style="display:block;width:100%;height:420px;border:0;background:#ffffff;"></iframe></div>' +
      '<details style="border-top:2px solid #9e9e9e;background:#f6f6f6;color:#1f1f1f;">' +
      '<summary style="padding:5px 10px;background:#e4e4e4;color:#444;font-size:12px;cursor:pointer;">🔎 So hat der Browser Ihre style.css verstanden</summary>' +
      '<pre class="lk-css" style="margin:0;padding:6px 10px;max-height:320px;overflow:auto;white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;background:transparent;color:#1f1f1f;"></pre>' +
      '</details></div>';
    zeigeHtml(aussen, "[Lernkarten-Fenster]");
  }

  // ---------- farbe(...) und kontrast(...) ----------
  function hexTeile(hex) {
    var h = String(hex).trim().replace("#", "");
    if (h.length === 3) { h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2]; }
    if (!/^[0-9a-f]{6}$/i.test(h)) { return null; }
    return [h.substr(0, 2), h.substr(2, 2), h.substr(4, 2)];
  }
  self.farbe = function () {
    var kacheln = "";
    var text = [];
    for (var i = 0; i < arguments.length; i++) {
      var hex = String(arguments[i]).trim();
      var teile = hexTeile(hex);
      if (!teile) {
        kacheln += '<div style="padding:8px;color:#b3261e;">❌ ' + htmlText(hex) + ' ist kein Hex-Wert. Form: #rrggbb</div>';
        continue;
      }
      var werte = teile.map(function (t) { return parseInt(t, 16); });
      var namen = ["Rot", "Grün", "Blau"];
      var balken = "";
      for (var k = 0; k < 3; k++) {
        var f = ["#e53935", "#43a047", "#1e88e5"][k];
        balken += '<div style="display:flex;align-items:center;gap:6px;font-size:12px;"><span style="width:34px;">' + namen[k] + '</span>' +
          '<code>' + teile[k] + '</code><span style="display:inline-block;width:' + Math.round(werte[k] / 255 * 90) + 'px;height:8px;background:' + f + ';border-radius:2px;"></span>' +
          '<span style="opacity:.7;">' + werte[k] + ' / 255</span></div>';
      }
      kacheln += '<div style="display:flex;gap:10px;align-items:center;padding:6px;border:1px solid #ccc;border-radius:8px;background:#fff;color:#222;">' +
        '<div style="width:64px;height:52px;border-radius:6px;border:1px solid #999;background:#' + teile.join("") + ';"></div>' +
        '<div><div style="font-family:ui-monospace,monospace;font-weight:700;margin-bottom:3px;">#' + teile.join("").toLowerCase() + '</div>' + balken + '</div></div>';
      text.push("#" + teile.join("") + ": Rot " + werte[0] + ", Grün " + werte[1] + ", Blau " + werte[2]);
    }
    zeigeHtml('<div style="display:flex;flex-wrap:wrap;gap:10px;font-family:system-ui,sans-serif;">' + kacheln + '</div>', text.join("\n"));
    return undefined;
  };
  function leuchtdichte(hex) {
    var teile = hexTeile(hex);
    if (!teile) { return null; }
    var c = teile.map(function (t) {
      var x = parseInt(t, 16) / 255;
      return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  }
  self.kontrast = function (farbe1, farbe2) {
    var l1 = leuchtdichte(farbe1);
    var l2 = leuchtdichte(farbe2);
    if (l1 === null || l2 === null) {
      console.log("❌ Bitte zwei Hex-Farben angeben, zum Beispiel kontrast(\"#222222\", \"#f4f4f4\")");
      return undefined;
    }
    var wert = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    var urteil;
    if (wert >= 7) { urteil = "✅ sehr gut lesbar, auch aus zwei Metern"; }
    else if (wert >= 4.5) { urteil = "✅ gut lesbar für normalen Text"; }
    else if (wert >= 3) { urteil = "⚠️ nur für große oder fette Schrift ausreichend"; }
    else { urteil = "❌ zu schwach, schwer lesbar"; }
    console.log(farbe1 + " auf " + farbe2 + ":  Kontrast " + wert.toFixed(1).replace(".", ",") + " : 1   " + urteil);
    return undefined;
  };

  if (!self.__lkEvalOriginal) { self.__lkEvalOriginal = self.eval; }
  self.eval = function (code) {
    var anfang = code.replace(/^\s+/, "");
    if (anfang.indexOf("<!-- index.html") === 0) {
      dateien.html = anfang;
      console.log("✅ index.html gespeichert. So sieht sie mit der aktuellen style.css aus:");
      fenster();
      return undefined;
    }
    if (anfang.indexOf("/* style.css") === 0) {
      dateien.css = anfang;
      cssPruefen(anfang);
      fenster();
      return undefined;
    }
    return self.__lkEvalOriginal(code);
  };

  console.log("🧰 Werkzeugkiste bereit: Vorschau für index.html und style.css, farbe(...) und kontrast(...).");
})();
