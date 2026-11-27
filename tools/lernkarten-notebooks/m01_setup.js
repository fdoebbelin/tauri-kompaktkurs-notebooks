// Vorbereitete Werkzeugkiste für M1: nur ausführen, nicht lesen müssen.
// Sie verwendet Schreibweisen, die im Kurs bewusst NICHT vorkommen.
// Was sie tut: Zellen, die mit "<!-- index.html -->" beginnen, zeigen die ganze Datei
// in einem kleinen Fenster. Zellen mit "<!-- spielwiese -->" zeigen ihren Inhalt in der
// Spielwiese unter der Überschrift. Dazu kommt idListe(...) zum Gegenlesen.
(function () {
  var STANDARD_HTML = __HTML__;
  var SPIELWIESE_VORNE = "<h1>Lernkarten von Anna</h1>\n\n<div id=\"spielwiese\">\n";
  var SPIELWIESE_HINTEN = "\n</div>\n";
  var dateien = { html: STANDARD_HTML };

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
  function ohneKennung(text) {
    return text.replace(/^\s*<!--\s*(index\.html|spielwiese)\s*-->[^\n]*\n?/, "");
  }
  function koerper(html) {
    var treffer = /<body[^>]*>([\s\S]*)<\/body>/i.exec(html);
    var inhalt = treffer ? treffer[1] : html;
    return inhalt.replace(/<script[^>]*src=["']?app\.js["']?[^>]*>\s*<\/script>/i, "");
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
        var neu = Math.max(Math.ceil(unten + rand), 60) + "px";
        if (iframe.style.height !== neu) { iframe.style.height = neu; }
      }
      function beschriftung(el) {
        var t = el.tagName.toLowerCase();
        if (el.id) { t += "#" + el.id; }
        if (el.className) { t += "." + String(el.className).trim().split(/\s+/).join("."); }
        var attr = [];
        ["type", "placeholder"].forEach(function (a) { if (el.hasAttribute(a)) { attr.push(a + '="' + el.getAttribute(a) + '"'); } });
        if (attr.length) { t += "  [" + attr.join(", ") + "]"; }
        var text = "";
        if (el.tagName === "TEXTAREA") {
          text = el.value;
        } else {
          for (var i = 0; i < el.childNodes.length; i++) {
            if (el.childNodes[i].nodeType === 3) { text += el.childNodes[i].textContent; }
          }
        }
        text = text.replace(/\s+/g, " ").trim();
        if (text) { t += "  „" + (text.length > 48 ? text.slice(0, 48) + "…" : text) + "“"; }
        var leerBar = ["P", "UL", "TEXTAREA", "DIV", "LI", "SPAN", "H1", "H2", "BUTTON"];
        if (!text && el.children.length === 0 && leerBar.indexOf(el.tagName) >= 0) { t += "  (leer)"; }
        return t;
      }
      function baum(el, vorne, zeilen) {
        var kinder = [];
        for (var i = 0; i < el.children.length; i++) {
          if (el.children[i].tagName !== "SCRIPT") { kinder.push(el.children[i]); }
        }
        for (var k = 0; k < kinder.length; k++) {
          var letztes = k === kinder.length - 1;
          zeilen.push(vorne + (letztes ? "└─ " : "├─ ") + beschriftung(kinder[k]));
          if (kinder[k].tagName !== "TEXTAREA") { baum(kinder[k], vorne + (letztes ? "   " : "│  "), zeilen); }
        }
      }
      function verstanden() {
        var feld = rahmen ? rahmen.querySelector(".lk-baum") : null;
        if (!feld) { return; }
        var zeilen = ["body"];
        baum(document.body, "", zeilen);
        var ids = {};
        var alle = document.querySelectorAll("[id]");
        for (var i = 0; i < alle.length; i++) { ids[alle[i].id] = (ids[alle[i].id] || 0) + 1; }
        var namen = Object.keys(ids);
        zeilen.push("");
        zeilen.push("Gefundene ids (" + namen.length + "):");
        namen.forEach(function (n) { zeilen.push("  " + n + (ids[n] > 1 ? "   ⚠️ kommt " + ids[n] + "-mal vor" : "")); });
        feld.textContent = zeilen.join("\n");
      }
      if (rahmen) {
        var kisten = rahmen.querySelector(".lk-kisten");
        if (kisten) {
          var an = false;
          var stil = null;
          kisten.onclick = function () {
            an = !an;
            if (an) {
              stil = document.createElement("style");
              stil.textContent = "* { outline: 1px dashed #e0457b !important; } p:empty, ul:empty { min-height: 4px; }";
              document.head.appendChild(stil);
            } else if (stil) { stil.remove(); stil = null; }
            kisten.textContent = an ? "▣ Kisten ausblenden" : "▣ Kisten zeigen";
          };
        }
      }
      window.addEventListener("load", function () { hoehe(); verstanden(); });
      document.addEventListener("DOMContentLoaded", function () {
        new ResizeObserver(hoehe).observe(document.body);
      });
    }.toString() + ")();";
  }

  function fenster(koerperHtml, titel) {
    var dokument = "<!DOCTYPE html>\n<html lang=\"de\">\n<head>\n<meta charset=\"UTF-8\">\n" +
      "<script>" + fensterSkript() + "<\/script>\n</head>\n<body>\n" + koerperHtml + "\n</body>\n</html>";
    var knopf = "background:#4a4a4a;color:#f0f0f0;border:1px solid #6a6a6a;border-radius:5px;padding:2px 10px;font-size:12px;cursor:pointer;";
    var aussen =
      '<div class="lk-fenster" style="max-width:760px;border:1px solid #9e9e9e;border-radius:10px;overflow:hidden;' +
      'box-shadow:0 3px 12px rgba(0,0,0,.18);margin:6px 0;font-family:system-ui,sans-serif;">' +
      '<div style="background:#303030;color:#f0f0f0;padding:6px 12px;font-size:13px;display:flex;justify-content:space-between;align-items:center;gap:10px;">' +
      '<span>🗂️ ' + titel + '</span>' +
      '<button class="lk-kisten" style="' + knopf + '">▣ Kisten zeigen</button></div>' +
      '<iframe title="Lernkarten-Fenster" srcdoc="' + attribut(dokument) + '" ' +
      'style="display:block;width:100%;height:200px;border:0;background:#ffffff;"></iframe>' +
      '<details style="border-top:2px solid #9e9e9e;background:#f6f6f6;color:#1f1f1f;">' +
      '<summary style="padding:5px 10px;background:#e4e4e4;color:#444;font-size:12px;cursor:pointer;">🔎 So hat der Browser Ihre index.html verstanden</summary>' +
      '<pre class="lk-baum" style="margin:0;padding:6px 10px;max-height:360px;overflow:auto;white-space:pre;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;background:transparent;color:#1f1f1f;"></pre>' +
      '</details></div>';
    zeigeHtml(aussen, "[Lernkarten-Fenster]");
  }

  // ---------- idListe(...) : die Heftliste gegen die Datei prüfen ----------
  self.idListe = function () {
    var heft = Array.prototype.map.call(arguments, function (n) { return String(n); });
    var text = ohneKennung(dateien.html).replace(/<!--[\s\S]*?-->/g, "");
    var muster = /\bid\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))/g;
    var inDatei = [];
    var t;
    while ((t = muster.exec(text)) !== null) { inDatei.push(t[2] !== undefined ? t[2] : (t[3] !== undefined ? t[3] : t[4])); }
    var zeilen = [];
    function regeln(name) {
      var fehler = [];
      if (name !== name.toLowerCase()) { fehler.push("Regel 1: alles klein"); }
      if (/\s/.test(name)) { fehler.push("Regel 2: kein Leerzeichen, Bindestrich nehmen"); }
      if (/_/.test(name)) { fehler.push("Regel 2: Bindestrich statt Unterstrich"); }
      return fehler;
    }
    zeilen.push("Heftliste gegen index.html (" + heft.length + " im Heft, " + inDatei.length + " in der Datei):");
    var gesehen = {};
    heft.forEach(function (name) {
      var f = regeln(name);
      var anzahl = inDatei.filter(function (d) { return d === name; }).length;
      var zeile;
      if (gesehen[name]) { zeile = "⚠️ " + name + "   steht zweimal im Heft"; }
      else if (anzahl === 0) { zeile = "❌ " + name + "   steht im Heft, aber nicht in der Datei"; }
      else if (anzahl > 1) { zeile = "⚠️ " + name + "   steht " + anzahl + "-mal in der Datei. Eine id darf nur EINMAL vorkommen."; }
      else { zeile = "✅ " + name; }
      if (f.length) { zeile += "   (verstößt gegen " + f.join(" und ") + ")"; }
      gesehen[name] = true;
      zeilen.push("  " + zeile);
    });
    inDatei.forEach(function (name, i) {
      if (heft.indexOf(name) < 0 && inDatei.indexOf(name) === i) {
        zeilen.push("  ⚠️ " + name + "   steht in der Datei, aber nicht im Heft");
      }
    });
    console.log(zeilen.join("\n"));
    return undefined;
  };

  // ---------- idRegeln(...) : nur die Kursregeln 1 und 2 prüfen ----------
  self.idRegeln = function () {
    var zeilen = [];
    Array.prototype.forEach.call(arguments, function (n) {
      var name = String(n);
      var fehler = [];
      if (name !== name.toLowerCase()) { fehler.push("Regel 1: alles klein"); }
      if (/\s/.test(name)) { fehler.push("Regel 2: kein Leerzeichen, Bindestrich nehmen"); }
      if (/_/.test(name)) { fehler.push("Regel 2: Bindestrich statt Unterstrich"); }
      zeilen.push((fehler.length ? "❌ " : "✅ ") + '"' + name + '"' + (fehler.length ? "   verstößt gegen " + fehler.join(" und ") : ""));
    });
    zeilen.push("(Regel 3, „auf Deutsch“, prüfen Sie selbst.)");
    console.log(zeilen.join("\n"));
    return undefined;
  };

  if (!self.__lkEvalOriginal) { self.__lkEvalOriginal = self.eval; }
  self.eval = function (code) {
    var anfang = code.replace(/^\s+/, "");
    if (anfang.indexOf("<!-- index.html") === 0) {
      dateien.html = anfang;
      fenster(koerper(ohneKennung(anfang)), "Lernkarten");
      return undefined;
    }
    if (anfang.indexOf("<!-- spielwiese") === 0) {
      var stueck = ohneKennung(anfang).split("\n").map(function (z) { return "  " + z; }).join("\n");
      fenster(SPIELWIESE_VORNE + stueck + SPIELWIESE_HINTEN, "Lernkarten · Spielwiese");
      return undefined;
    }
    return self.__lkEvalOriginal(code);
  };

  console.log("🧰 Werkzeugkiste bereit: Vorschau für index.html und Spielwiese, dazu idListe(...) und idRegeln(...).");
})();
