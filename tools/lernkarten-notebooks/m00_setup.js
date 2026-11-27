// Vorbereitete Werkzeugkiste für M0: nur ausführen, nicht lesen müssen.
// Sie verwendet Schreibweisen, die im Kurs bewusst NICHT vorkommen.
// Was sie tut: Jede Zelle, die mit "// app.js" beginnt, wird nicht hier im
// Notebook ausgeführt, sondern in einem kleinen Anwendungsfenster mit
// index.html und style.css – samt eigener Konsole darunter.
// Neu in M5: Sie spielt auch den Programmkern (main.rs). window.__TAURI__.core.invoke
// kennt "karten_laden" und "karten_speichern" und hält lernkarten.json im Speicher
// des Browsers fest, damit die Karten einen Neustart überleben.
// In M0: "# Fertige App" zeigt die fertige Lernkarten-App, "# Ebene 1/2/3" ihre drei
// Schichten, "# Terminal" ein Übungs-Terminal für die Startbefehle, und Zellen mit
// "<!-- index.html -->" zeigen Ihr eigenes Projekt. Alles ist simuliert.
(function () {
  var STANDARD_HTML = __HTML__;
  var STANDARD_CSS = __CSS__;
  var STANDARD_JS = __JS__;
  var STANDARD_DESKTOP = __DESKTOP__;
  var FERTIG_STAND = { html: __FERTIG_HTML__, css: __FERTIG_CSS__, js: __FERTIG_JS__, name: "Lernkarten" };

  // ---------- Ausgabe im Notebook selbst ----------
  function zeige(wert, tiefe) {
    if (wert === undefined) { return "undefined"; }
    if (wert === null) { return "null"; }
    if (typeof wert === "string") { return tiefe === 0 ? wert : '"' + wert + '"'; }
    if (typeof wert === "function") { return "ƒ " + (wert.name || "anonym") + "()"; }
    if (Array.isArray(wert)) {
      return "[" + wert.map(function (w) { return zeige(w, tiefe + 1); }).join(", ") + "]";
    }
    if (typeof wert === "object") {
      return "{ " + Object.keys(wert).map(function (f) { return f + ": " + zeige(wert[f], tiefe + 1); }).join(", ") + " }";
    }
    return String(wert);
  }
  function ausgabe(kanal, werte) {
    var text = Array.prototype.map.call(werte, function (w) { return zeige(w, 0); }).join(" ");
    postMessage({ type: "stream", bundle: { name: kanal, text: text + "\n" } });
  }
  console.log = function () { ausgabe("stdout", arguments); };
  console.info = console.log;
  console.error = function () { ausgabe("stderr", arguments); };
  console.warn = console.error;

  // ---------- Die drei Dateien der App ----------
  var dateien = { html: STANDARD_HTML, css: STANDARD_CSS, js: STANDARD_JS, desktop: STANDARD_DESKTOP };

  // ---------- Hinweise zu style.css ----------
  function cssPruefen(css) {
    var funde = [];
    if (/display\s*:\s*grid/i.test(css)) { funde.push("display: grid (CSS Grid)"); }
    if (/position\s*:\s*absolute/i.test(css)) { funde.push("position: absolute"); }
    if (/\b(rgb|rgba|hsl|hsla)\s*\(/i.test(css)) { funde.push("Farben als rgb()/hsl() statt Hex-Wert"); }
    for (var i = 0; i < funde.length; i++) {
      console.log("💬 " + funde[i] + " steht nicht auf unserer Liste. Wenn es klappt, behalten wir es – wenn nicht, zurück zur Liste.");
    }
  }

  // ---------- Kontrast zweier Hex-Farben ----------
  function leuchtdichte(hex) {
    var h = String(hex).trim().replace("#", "");
    if (h.length === 3) { h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2]; }
    if (!/^[0-9a-f]{6}$/i.test(h)) { return null; }
    var teile = [0, 2, 4].map(function (p) {
      var c = parseInt(h.substr(p, 2), 16) / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * teile[0] + 0.7152 * teile[1] + 0.0722 * teile[2];
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
  var laeufe = 0;

  function ohneKennung(text) {
    return text.replace(/^\s*(<!--\s*index\.html\s*-->|\/\*\s*style\.css\s*\*\/)[^\n]*\n?/, "");
  }
  function koerper(html) {
    var treffer = /<body[^>]*>([\s\S]*)<\/body>/i.exec(html);
    var inhalt = treffer ? treffer[1] : html;
    return inhalt.replace(/<script[^>]*src=["']?app\.js["']?[^>]*>\s*<\/script>/i, "");
  }
  function titel(html) {
    var treffer = /<title>([\s\S]*?)<\/title>/i.exec(html);
    return treffer ? treffer[1].trim() : "Lernkarten";
  }
  function attribut(text) {
    return text.replace(/&/g, "&amp;").replace(/"/g, "&quot;");
  }
  function htmlText(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Läuft IM Fenster: leitet console.log und Fehler in die Konsole unter dem Fenster um.
  function fensterSkript(versatz, schluessel) {
    return "(" + function (VERSATZ, SCHLUESSEL) {
      var rahmen = window.frameElement ? window.frameElement.closest(".lk-fenster") : null;
      var zeilen = rahmen ? rahmen.querySelector(".lk-konsole") : null;
      var original = window.console.log.bind(window.console);
      if (zeilen) { zeilen.innerHTML = ""; }
      function zeige(w, tiefe) {
        if (w === undefined) { return "undefined"; }
        if (w === null) { return "null"; }
        if (typeof w === "string") { return tiefe === 0 ? w : '"' + w + '"'; }
        if (typeof w === "function") { return "ƒ " + (w.name || "anonym") + "()"; }
        if (w instanceof Promise) { return "Promise { <pending> }"; }
        if (w instanceof Element) {
          var t = "<" + w.tagName.toLowerCase();
          if (w.id) { t += ' id="' + w.id + '"'; }
          if (w.className) { t += ' class="' + w.className + '"'; }
          return t + ">";
        }
        if (Array.isArray(w)) {
          if (w.length === 0) { return "[]"; }
          var teile = w.map(function (x) { return zeige(x, tiefe + 1); });
          var mitObjekten = w.some(function (x) { return x !== null && typeof x === "object"; });
          if (mitObjekten) {
            var ein = "  ".repeat(tiefe + 1);
            return "[\n" + ein + teile.join(",\n" + ein) + "\n" + "  ".repeat(tiefe) + "]";
          }
          return "[" + teile.join(", ") + "]";
        }
        if (typeof w === "object") {
          var felder = Object.keys(w);
          if (felder.length === 0) { return "{}"; }
          return "{ " + felder.map(function (f) { return f + ": " + zeige(w[f], tiefe + 1); }).join(", ") + " }";
        }
        return String(w);
      }
      function zeile(text, fehler) {
        if (!zeilen) { return; }
        var leer = zeilen.querySelector(".lk-leer");
        if (leer) { leer.remove(); }
        var div = zeilen.ownerDocument.createElement("div");
        div.textContent = text;
        div.style.whiteSpace = "pre-wrap";
        div.style.padding = "2px 0";
        div.style.borderBottom = "1px solid rgba(128,128,128,.2)";
        if (fehler) {
          div.style.color = "#b3261e";
          div.style.background = "#fdecea";
          div.style.padding = "2px 4px";
        }
        zeilen.appendChild(div);
      }
      window.console.log = function () {
        original.apply(null, arguments);
        zeile(Array.prototype.map.call(arguments, function (w) { return zeige(w, 0); }).join(" "), false);
      };
      window.console.info = window.console.log;
      window.console.error = function () {
        zeile(Array.prototype.map.call(arguments, function (w) { return zeige(w, 0); }).join(" "), true);
      };
      window.console.warn = window.console.error;
      window.addEventListener("error", function (e) {
        var nummer = e.lineno - VERSATZ;
        var ort = nummer > 0 ? "    (app.js, Zeile " + nummer + ")" : "";
        zeile("❌ " + e.message + ort, true);
      });
      window.addEventListener("unhandledrejection", function (e) {
        var grund = e.reason;
        var text = typeof grund === "string" ? grund : (grund && grund.name ? grund.name + ": " + grund.message : String(grund));
        var ort = "";
        var stelle = grund && grund.stack ? /about:srcdoc:(\d+):\d+/.exec(grund.stack) : null;
        if (stelle && Number(stelle[1]) - VERSATZ > 0) { ort = "    (app.js, Zeile " + (Number(stelle[1]) - VERSATZ) + ")"; }
        zeile("❌ Uncaught (in promise) " + text + ort, true);
      });

      // ---------- Der nachgebildete Programmkern ----------
      var dateiFeld = rahmen ? rahmen.querySelector(".lk-datei") : null;
      var dateiInfo = rahmen ? rahmen.querySelector(".lk-datei-info") : null;
      function dateiLesen() {
        try { return window.localStorage.getItem(SCHLUESSEL); } catch (f) { return null; }
      }
      function dateiZeigen(aktion) {
        var text = dateiLesen();
        if (dateiFeld) { dateiFeld.textContent = text === null ? "(Die Datei gibt es noch nicht.)" : text; }
        if (dateiInfo) {
          var jetzt = new Date();
          var zeit = ("0" + jetzt.getHours()).slice(-2) + ":" + ("0" + jetzt.getMinutes()).slice(-2) + ":" + ("0" + jetzt.getSeconds()).slice(-2);
          dateiInfo.textContent = aktion ? "· " + aktion + " (" + zeit + ")" : "";
        }
      }
      window.__TAURI__ = { core: { invoke: function (name, argumente) {
        return new Promise(function (erfuellt, abgelehnt) {
          setTimeout(function () {
            if (name === "karten_laden") {
              var text = dateiLesen();
              var liste = text === null ? [] : JSON.parse(text);
              dateiZeigen("karten_laden: " + liste.length + " Karten gelesen");
              erfuellt(liste);
            } else if (name === "karten_speichern") {
              if (!argumente || !("karten" in argumente)) {
                abgelehnt("invalid args `karten` for command `karten_speichern`: command karten_speichern missing required key karten");
                return;
              }
              try { window.localStorage.setItem(SCHLUESSEL, JSON.stringify(argumente.karten, null, 2)); } catch (f) { }
              dateiZeigen("karten_speichern: " + (argumente.karten ? argumente.karten.length : 0) + " Karten geschrieben");
              erfuellt(null);
            } else {
              abgelehnt("Command " + name + " not found");
            }
          }, 300);
        });
      } } };
      dateiZeigen("");
      if (rahmen) {
        var neustart = rahmen.querySelector(".lk-neustart");
        var loeschen = rahmen.querySelector(".lk-datei-loeschen");
        var iframe = window.frameElement;
        if (neustart) { neustart.onclick = function () { iframe.srcdoc = iframe.srcdoc; }; }
        if (loeschen) {
          loeschen.onclick = function () {
            try { window.localStorage.removeItem(SCHLUESSEL); } catch (f) { }
            dateiZeigen("Datei gelöscht");
          };
        }
      }
      function hoehe() {
        if (!window.frameElement || !document.body) { return; }
        var unten = document.body.getBoundingClientRect().bottom + window.scrollY;
        var rand = parseFloat(getComputedStyle(document.body).marginBottom) || 0;
        var neu = Math.ceil(unten + rand) + "px";
        if (window.frameElement.style.height !== neu) { window.frameElement.style.height = neu; }
      }
      window.addEventListener("load", hoehe);
      document.addEventListener("DOMContentLoaded", function () {
        new ResizeObserver(hoehe).observe(document.body);
      });
    }.toString() + ")(" + versatz + ", " + JSON.stringify(schluessel) + ");";
  }

  // ================= Ab hier neu in M7 =================
  var DEV = { schluessel: "tauri-kompaktkurs/lernkarten.json", pfad: "~/.local/share/de.metarow.Lernkarten/lernkarten.json" };
  var FLATPAK = { schluessel: "tauri-kompaktkurs/flatpak/lernkarten.json", pfad: "~/.var/app/de.metarow.Lernkarten/data/de.metarow.Lernkarten/lernkarten.json" };
  var PROJEKT = "~/Projekte/lernkarten";
  var zustand = { ort: "host", pfad: "~", gebaut: null, repo: false, remote: false, installiert: null, bundle: false, gestartet: false, ersterStart: true };
  var FERTIG = { schluessel: "tauri-kompaktkurs/m0-fertig/lernkarten.json", pfad: "lernkarten.json der fertigen Anwendung", titel: "Lernkarten · die fertige Anwendung" };
  var IHR_PROJEKT = { schluessel: "tauri-kompaktkurs/m0-projekt/lernkarten.json", pfad: "", titel: "Lernkarten · Ihr Projekt", schlicht: true };

  function stand() {
    return { html: dateien.html, css: dateien.css, js: dateien.js, name: desktopName(dateien.desktop) };
  }
  function desktopName(text) {
    var t = /^Name\s*=\s*(.*)$/m.exec(text || "");
    return t ? t[1].trim() : "";
  }

  function fensterHtml(s, art, verzoegert) {
    var html = ohneKennung(s.html);
    var css = ohneKennung(s.css);
    var js = s.js;
    var oben = "<!DOCTYPE html>\n<html lang=\"de\">\n<head>\n<meta charset=\"UTF-8\">\n" +
      "<style>\n" + css + "\n</style>\n<script>__SHIM__<\/script>\n</head>\n<body>\n" +
      koerper(html) + "\n<script>\n";
    var versatz = oben.split("\n").length - 1 + fensterSkript(0, art.schluessel).split("\n").length - 1;
    var dokument = oben.replace("__SHIM__", fensterSkript(versatz, art.schluessel)) + js + "\n<\/script>\n</body>\n</html>";
    var titelText = art.titel || (art === DEV ? "Lernkarten · Entwicklungslauf (cargo tauri dev)" : (s.name || "Lernkarten") + " · installiert");
    if (art === IHR_PROJEKT) { titelText = titel(s.html) + "  ·  Ihr Projekt"; }
    var balken = art === DEV || art === IHR_PROJEKT ? "#8a4b12" : "#303030";
    var panels = art.schlicht ? "" : panelHtml(art);
    return '<div class="lk-fenster" style="max-width:760px;border:1px solid #9e9e9e;border-radius:10px;overflow:hidden;' +
      'box-shadow:0 3px 12px rgba(0,0,0,.18);margin:6px 0;font-family:system-ui,sans-serif;' + (verzoegert ? "display:none;" : "") + '">' +
      '<div style="background:' + balken + ';color:#f0f0f0;padding:6px 12px;font-size:13px;display:flex;justify-content:space-between;align-items:center;">' +
      '<span>🗂️ ' + htmlText(titelText) + '</span>' +
      '<button class="lk-neustart" title="App schließen und neu starten" style="background:#4a4a4a;color:#f0f0f0;border:1px solid #6a6a6a;border-radius:5px;padding:2px 10px;font-size:12px;cursor:pointer;">⟳ Neu starten</button></div>' +
      '<iframe title="Lernkarten-Fenster" ' + (verzoegert ? "data-srcdoc" : "srcdoc") + '="' + attribut(dokument) + '" ' +
      'style="display:block;width:100%;height:420px;border:0;background:#ffffff;"></iframe>' + panels + '</div>';
  }
  function panelHtml(art) {
    return '<div style="border-top:2px solid #9e9e9e;background:#f6f6f6;color:#1f1f1f;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;">' +
      '<div style="padding:4px 10px;background:#e4e4e4;color:#444;font-family:system-ui,sans-serif;font-size:12px;">Konsole</div>' +
      '<div class="lk-konsole" style="padding:4px 10px 6px 10px;min-height:20px;"><div class="lk-leer" style="color:#888;">(noch keine Ausgabe)</div></div></div>' +
      '<div style="border-top:2px solid #9e9e9e;background:#fffdf2;color:#1f1f1f;font-size:12px;">' +
      '<div style="padding:4px 10px;background:#eee6c8;color:#444;display:flex;justify-content:space-between;align-items:center;gap:8px;">' +
      '<span>📄 ' + htmlText(art.pfad) + ' <span class="lk-datei-info" style="opacity:.75"></span></span>' +
      '<button class="lk-datei-loeschen" title="Datei löschen" style="background:#fff;color:#444;border:1px solid #bbb;border-radius:5px;padding:1px 8px;font-size:12px;cursor:pointer;">🗑 Datei löschen</button></div>' +
      '<pre class="lk-datei" style="margin:0;padding:6px 10px;max-height:200px;overflow:auto;white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;background:transparent;color:#1f1f1f;"></pre>' +
      '</div>';
  }
  function zeigeHtml(html, text) {
    postMessage({ type: "display_data", bundle: { data: { "text/html": html, "text/plain": text || "[Anzeige]" }, metadata: {}, transient: {} } });
  }

  // ---------- Das Anwendungsmenü ----------
  function menue() {
    var app = zustand.installiert;
    var kacheln = [["📁", "Dateien"], ["🌐", "Firefox"], ["⬛", "Terminal"], ["📝", "Texteditor"], ["⚙️", "Einstellungen"]];
    var gitter = "";
    for (var i = 0; i < kacheln.length; i++) {
      gitter += '<div class="kachel kulisse" title="nur Kulisse"><div class="sym">' + kacheln[i][0] + '</div><div>' + kacheln[i][1] + '</div></div>';
    }
    if (app) {
      gitter += '<div class="kachel lernkarten" title="Starten"><div class="sym">🗂️</div><div>' + htmlText(app.name || "Lernkarten") + '</div></div>';
    }
    var hinweis = app ? "Klicken Sie auf Ihre App, um sie zu starten." : "Lernkarten ist noch nicht installiert. Erst bauen, dann installieren (Abschnitt 3 und 4).";
    var innen = "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>" +
      "body{margin:0;font-family:system-ui,sans-serif;background:linear-gradient(135deg,#1e3a5f,#3b2f5f);color:#fff;padding:18px;}" +
      ".gitter{display:flex;flex-wrap:wrap;gap:18px;}" +
      ".kachel{width:96px;text-align:center;font-size:13px;padding:10px 4px;border-radius:12px;}" +
      ".sym{font-size:40px;line-height:52px;}" +
      ".kulisse{opacity:.6;cursor:default;}" +
      ".lernkarten{cursor:pointer;background:rgba(255,255,255,.12);outline:2px solid rgba(255,255,255,.5);}" +
      ".lernkarten:hover{background:rgba(255,255,255,.25);}" +
      "p{margin:14px 0 0 0;font-size:13px;opacity:.85;}</style></head><body>" +
      "<div class='gitter'>" + gitter + "</div><p>" + hinweis + "</p>" +
      "<script>var k=document.querySelector('.lernkarten');if(k){k.addEventListener('click',function(){" +
      "var m=window.frameElement.closest('.lk-menue');var f=m.querySelector('.lk-fenster');f.style.display='block';" +
      "var i=f.querySelector('iframe');i.srcdoc=i.getAttribute('data-srcdoc');});}" +
      "<\/script></body></html>";
    var html = '<div class="lk-menue" style="max-width:760px;">' +
      '<div style="border-radius:10px;overflow:hidden;border:1px solid #555;margin:6px 0;">' +
      '<div style="background:#111;color:#ddd;padding:5px 12px;font-size:12px;font-family:system-ui,sans-serif;">Anwendungsmenü</div>' +
      '<iframe title="Anwendungsmenü" srcdoc="' + attribut(innen) + '" style="display:block;width:100%;height:' + (app ? 300 : 300) + 'px;border:0;"></iframe></div>' +
      (app ? fensterHtml(app, FLATPAK, true) : "") + "</div>";
    zeigeHtml(html, "[Anwendungsmenü]");
  }

  // ---------- open lernkarten.json als Tabelle ----------
  function jsonTabelle(art) {
    var innen = "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>body{margin:0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;white-space:pre;color:#1f1f1f;background:#fff;}</style></head><body><div id='t'></div><script>" +
      "var text=null;try{text=localStorage.getItem(" + JSON.stringify(art.schluessel) + ");}catch(e){}" +
      "var aus;if(text===null){aus='Error: nu::shell::io::not_found\\n\\n  × Datei nicht gefunden: " + art.pfad + "\\n  help: Die Datei entsteht erst, wenn die App zum ersten Mal speichert.';}" +
      "else{var l=JSON.parse(text);if(l.length===0){aus='╭────────────╮\\n│ empty list │\\n╰────────────╯';}else{" +
      "var b0=3,b1=5,b2=7;l.forEach(function(k,i){b0=Math.max(b0,String(i).length+2);b1=Math.max(b1,String(k.frage).length+2);b2=Math.max(b2,String(k.antwort).length+2);});" +
      "function z(a,b,c){return '│'+a.padStart(b0-1)+' │ '+b.padEnd(b1-1)+'│ '+c.padEnd(b2-1)+'│';}" +
      "function s(l,m,r){return l+'─'.repeat(b0)+m+'─'.repeat(b1)+m+'─'.repeat(b2)+r;}" +
      "var r=[s('╭','┬','╮'),z('#','frage','antwort'),s('├','┼','┤')];l.forEach(function(k,i){r.push(z(String(i),String(k.frage),String(k.antwort)));});r.push(s('╰','┴','╯'));aus=r.join('\\n');}}" +
      "document.getElementById('t').textContent=aus;" +
      "if(window.frameElement){window.frameElement.style.height=(document.body.scrollHeight+4)+'px';}" +
      "<\/script></body></html>";
    zeigeHtml('<iframe title="open" srcdoc="' + attribut(innen) + '" style="display:block;width:100%;max-width:760px;height:60px;border:0;"></iframe>', "[Tabelle]");
  }

  // ---------- Das Übungs-Terminal ----------
  function prompt() {
    var p = zustand.pfad;
    return zustand.ort === "container" ? "⬢ tauri-dev " + p + " ❯ " : p + " ❯ ";
  }
  function nuTabelle(spalten, zeilen) {
    var breiten = spalten.map(function (s, i) {
      var b = s.length;
      zeilen.forEach(function (z) { b = Math.max(b, String(z[i]).length); });
      return b + 2;
    });
    var nr = Math.max(3, String(zeilen.length).length + 2);
    function strich(l, m, r) { return l + "─".repeat(nr) + breiten.map(function (b) { return m + "─".repeat(b); }).join("") + r; }
    function zeile(n, werte) { return "│" + (" " + n).padEnd(nr) + werte.map(function (w, i) { return "│ " + String(w).padEnd(breiten[i] - 1); }).join("") + "│"; }
    var aus = [strich("╭", "┬", "╮"), zeile("#", spalten), strich("├", "┼", "┤")];
    zeilen.forEach(function (z, i) { aus.push(zeile(String(i), z)); });
    aus.push(strich("╰", "┴", "╯"));
    return aus.join("\n");
  }
  function nichtGefunden(befehl) {
    var wort = befehl.split(/\s+/)[0];
    return "Error: nu::shell::external_command\n\n  × External command failed\n   ╭─[entry #1:1:1]\n 1 │ " + befehl +
      "\n   · " + "─".repeat(wort.length) + "\n   ·  ╰── executable was not found\n   ╰────\n  help: No such file or directory (os error 2)";
  }
  function imProjekt() { return zustand.pfad === PROJEKT; }
  function hat(teile, wort) { return teile.indexOf(wort) >= 0; }

  function befehl(zeile) {
    var t = zeile.trim().split(/\s+/);
    var z = zustand;
    var aus = [];
    if (t[0] === "exit") {
      if (z.ort === "container") { z.ort = "host"; return "(Container verlassen. Sie sind jetzt auf dem Host.)"; }
      return "(Auf dem Host würde exit das Terminal schließen. Im Kurs braucht es nur EIN exit, um aus dem Container zu kommen.)";
    }
    if (t[0] === "toolbox" && t[1] === "enter") {
      if (z.ort === "container") { return "Error: toolbox: already inside a toolbox container"; }
      z.ort = "container"; return "(Sie sind jetzt im Container tauri-dev.)";
    }
    if (/^if \("\/run\/\.toolboxenv" \| path exists\)/.test(zeile.trim())) {
      return z.ort === "container" ? "im Container" : "auf dem Host";
    }
    if (t[0] === "cd") {
      var ziel = t[1] || "~";
      if (ziel === "~" ) { z.pfad = "~"; return ""; }
      if (ziel === ".." ) { z.pfad = z.pfad === PROJEKT ? "~/Projekte" : "~"; return ""; }
      if (ziel === "~/Projekte/lernkarten" || (ziel === "lernkarten" && z.pfad === "~/Projekte") || (ziel === "Projekte/lernkarten" && z.pfad === "~")) { z.pfad = PROJEKT; return ""; }
      if (ziel === "~/Projekte" || (ziel === "Projekte" && z.pfad === "~")) { z.pfad = "~/Projekte"; return ""; }
      return "Error: nu::shell::directory_not_found\n\n  × Directory not found: " + ziel;
    }
    if (t[0] === "pwd") { return z.pfad.replace("~", "/var/home/anna"); }
    if (t[0] === "clear") { return ""; }
    if (t[0] === "ls" && t.length === 1) {
      if (!imProjekt()) { return nuTabelle(["name", "type"], [["Projekte", "dir"]]); }
      var zeilen = [["de.metarow.Lernkarten.desktop", "file"], ["de.metarow.Lernkarten.metainfo.xml", "file"], ["de.metarow.Lernkarten.yml", "file"], ["src", "dir"], ["src-tauri", "dir"]];
      if (z.gebaut) { zeilen.unshift(["build-dir", "dir"]); zeilen.push(["repo", "dir"]); }
      if (z.bundle) { zeilen.push(["lernkarten.flatpak", "file"]); }
      return nuTabelle(["name", "type"], zeilen);
    }
    if (t[0] === "ls" && t[1] === "~/.local/share" && /where name =~ "?Lernkarten"?/.test(zeile)) {
      return nuTabelle(["name", "type"], [["/var/home/anna/.local/share/de.metarow.Lernkarten", "dir"]]);
    }
    if (t[0] === "ls" && /^~\/\.local\/share\/de\.metarow\.Lernkarten\/?$/.test(t[1] || "")) {
      return nuTabelle(["name", "type"], [["lernkarten.json", "file"]]);
    }
    if (t[0] === "ls" && /^~\/\.var\/app\/de\.metarow\.Lernkarten\/data\/?$/.test(t[1] || "")) {
      if (!z.installiert) { return "Error: nu::shell::directory_not_found\n\n  × Directory not found: ~/.var/app/de.metarow.Lernkarten/data\n  help: Den Ordner gibt es erst, wenn die App installiert ist."; }
      return nuTabelle(["name", "type"], [["/var/home/anna/.var/app/de.metarow.Lernkarten/data/de.metarow.Lernkarten", "dir"]]);
    }
    if (t[0] === "open" && /lernkarten\.json$/.test(t[1] || "")) {
      if (t[1].indexOf("~/.var/app/") === 0) { return { tabelle: FLATPAK }; }
      if (t[1].indexOf("~/.local/share/") === 0) { return { tabelle: DEV }; }
      return "Error: nu::shell::io::not_found\n\n  × Datei nicht gefunden: " + t[1];
    }
    if (t[0] === "swaymsg" && t[1] === "splith") {
      return "[{ \"success\": true }]\n(Das nächste Fenster öffnet sich neben dem aktuellen: Editor links, Anwendung rechts.)";
    }
    if (t[0] === "with-env" && /cargo tauri dev/.test(zeile)) { t = ["cargo", "tauri", "dev"]; }
    if (t[0] === "cargo" && t[1] === "tauri" && t[2] === "dev") {
      if (z.ort !== "container") { return nichtGefunden(zeile.trim()) + "\n\n(Hinweis: cargo gibt es nur im Container. Erst: toolbox enter tauri-dev)"; }
      if (!imProjekt()) { return "Error: couldn't find a Tauri project in the current directory\n(Hinweis: cd ~/Projekte/lernkarten)"; }
      var log = "        Info Watching /var/home/anna/Projekte/lernkarten/src-tauri for changes...\n";
      if (z.ersterStart) {
        log += "    Updating crates.io index\n Downloading 398 crates ...\n   Compiling proc-macro2 v1.0.95\n   Compiling serde v1.0.219\n   Compiling glib v0.18.5\n   Compiling webkit2gtk v2.0.1\n   … (sehr viele Zeilen mehr) …\n   Compiling tauri v2.5.1\n";
      }
      log += "   Compiling lernkarten v0.1.0 (/var/home/anna/Projekte/lernkarten/src-tauri)\n    Finished `dev` profile [unoptimized + debuginfo] target(s) in " + (z.ersterStart ? "2m 47s" : "3.84s") + "\n     Running `target/debug/lernkarten`";
      if (z.ersterStart) { log += "\n\n(Der erste Start dauert in echt einige Minuten. Das ist kein Absturz: Das Programm wird übersetzt. Jeder weitere Start geht schnell.)"; }
      z.ersterStart = false;
      return { dev: true, text: log };
    }
    if (t[0] === "flatpak") {
      if (z.ort === "container") {
        return nichtGefunden(zeile.trim());
      }
      if (t[1] === "run" && t[2] === "org.flatpak.Builder") {
        var manifest = t[t.length - 1];
        if (!imProjekt()) { return "error: Can't parse '" + manifest + "': Failed to open file “" + z.pfad.replace("~", "/var/home/anna") + "/" + manifest + "”: No such file or directory\n(Hinweis: cd ~/Projekte/lernkarten)"; }
        if (manifest !== "de.metarow.Lernkarten.yml") { return "error: Can't parse '" + manifest + "': Failed to open file “/var/home/anna/Projekte/lernkarten/" + manifest + "”: No such file or directory\n(Hinweis: Wie heißt die Bauanleitung genau? ls zeigt es.)"; }
        var mitRepo = t.some(function (w) { return w === "--repo=repo"; });
        aus.push("Downloading sources");
        aus.push("Starting build of de.metarow.Lernkarten");
        aus.push("========================================================================");
        aus.push("Building module lernkarten in /var/home/anna/Projekte/lernkarten/.flatpak-builder/build/lernkarten-1");
        aus.push("========================================================================");
        aus.push("Running: cargo build --release --manifest-path src-tauri/Cargo.toml");
        aus.push("    Updating crates.io index");
        aus.push(" Downloading 412 crates ...");
        aus.push("   Compiling proc-macro2 v1.0.95");
        aus.push("   Compiling serde v1.0.219");
        aus.push("   Compiling webkit2gtk v2.0.1");
        aus.push("   … (viele hundert Zeilen mehr) …");
        aus.push("   Compiling tauri v2.5.1");
        aus.push("   Compiling lernkarten v0.1.0 (/run/build/lernkarten/src-tauri)");
        aus.push("    Finished `release` profile [optimized] target(s) in 6m 41s");
        aus.push("Running: install -Dm755 src-tauri/target/release/lernkarten /app/bin/lernkarten");
        aus.push("Running: install -Dm644 de.metarow.Lernkarten.desktop /app/share/applications/de.metarow.Lernkarten.desktop");
        aus.push("Running: install -Dm644 de.metarow.Lernkarten.metainfo.xml /app/share/metainfo/de.metarow.Lernkarten.metainfo.xml");
        aus.push("Running: install -Dm644 src-tauri/icons/128x128.png /app/share/icons/hicolor/128x128/apps/de.metarow.Lernkarten.png");
        aus.push("Committing stage build-lernkarten to cache");
        aus.push("Cleaning up");
        aus.push("Finishing app");
        if (mitRepo) {
          aus.push("Exporting de.metarow.Lernkarten to repo");
          aus.push("Commit: 3f9c2e8a41b7d05c6e1f2a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d");
          aus.push("Metadata Total: 1043");
          aus.push("Content Written: 412");
          aus.push("Pruning cache");
        }
        z.gebaut = stand();
        if (mitRepo) { z.repo = true; }
        aus.push("");
        aus.push(mitRepo ? "(Im Notebook geht das in einer Sekunde. In echt dauert der erste Bau mehrere Minuten, und es läuft viel mehr Text durch.)"
                         : "(Gebaut, aber ohne --repo=repo: Das Ergebnis liegt nur in build-dir und kann nicht installiert werden.)");
        return aus.join("\n");
      }
      if (t[1] === "remote-add") {
        if (!z.repo) { return "error: Can't load uri file:///var/home/anna/Projekte/lernkarten/repo/: Unable to load summary from remote lernkarten-lokal: Error opening file /var/home/anna/Projekte/lernkarten/repo/summary: No such file or directory\n(Hinweis: Erst bauen, dann entsteht repo.)"; }
        z.remote = true;
        return "";
      }
      if (t[1] === "install") {
        if (!z.remote) { return "error: No remote refs found for ‘lernkarten-lokal’\n(Hinweis: Erst die Paketquelle eintragen: flatpak remote-add …)"; }
        if (z.installiert) { return "Skipping: de.metarow.Lernkarten/x86_64/master is already installed\n(Hinweis: Eine neue Fassung holen Sie mit: flatpak update de.metarow.Lernkarten)"; }
        z.installiert = z.gebaut;
        return "Looking for matches…\n\n\n        ID                          Branch    Op    Remote              Download\n 1. [✓] de.metarow.Lernkarten       master    i     lernkarten-lokal    < 4,2 MB\n\nProceed with these changes to the user installation? [Y/n]: y\n\nInstallation complete.";
      }
      if (t[1] === "update") {
        if (!z.installiert) { return "error: de.metarow.Lernkarten not installed"; }
        if (z.installiert === z.gebaut) { return "Looking for updates…\n\nNothing to do."; }
        z.installiert = z.gebaut;
        return "Looking for updates…\n\n\n        ID                          Branch    Op    Remote              Download\n 1. [✓] de.metarow.Lernkarten       master    u     lernkarten-lokal    < 4,2 MB\n\nUpdates complete.";
      }
      if (t[1] === "list") {
        var apps = [["Firefox", "org.mozilla.firefox", "flathub"]];
        if (z.installiert) { apps.push([z.installiert.name || "Lernkarten", "de.metarow.Lernkarten", "lernkarten-lokal"]); }
        return nuTabelle(["Name", "Application ID", "Origin"], apps);
      }
      if (t[1] === "info" && hat(t, "--show-permissions")) {
        if (!z.installiert) { return "error: de.metarow.Lernkarten/*unspecified*/*unspecified* not installed"; }
        return "[Context]\nshared=ipc;\nsockets=wayland;fallback-x11;\ndevices=dri;";
      }
      if (t[1] === "run" && t[2] === "de.metarow.Lernkarten") {
        if (!z.installiert) { return "error: app/de.metarow.Lernkarten/x86_64/master not installed"; }
        return { flatpak: true, text: "" };
      }
      if (t[1] === "override") { return ""; }
      if (t[1] === "build-bundle") {
        if (!z.repo) { return "error: 'repo' is not a valid repository: opening repo: opendir(objects): No such file or directory"; }
        z.bundle = true; return "";
      }
      return "error: Unbekannter Befehl im Übungs-Terminal: " + zeile.trim() + "\n(Das Übungs-Terminal kennt nur die Befehle aus dem Kurs.)";
    }
    if (t[0] === "rm" || t[0] === "sudo" || t[0] === "rpm-ostree") {
      return "(Dieser Befehl ist im Übungs-Terminal absichtlich gesperrt.)";
    }
    return nichtGefunden(zeile.trim());
  }

  function terminal(code) {
    var zeilen = code.split("\n").slice(1);
    var block = [];
    function raus() {
      if (block.length) { postMessage({ type: "stream", bundle: { name: "stdout", text: block.join("\n") + "\n" } }); block = []; }
    }
    for (var i = 0; i < zeilen.length; i++) {
      var zeile = zeilen[i];
      if (zeile.trim() === "" || zeile.trim().charAt(0) === "#") { continue; }
      block.push(prompt() + zeile.trim());
      var erg = befehl(zeile);
      if (typeof erg === "string") {
        if (erg !== "") { block.push(erg); }
      } else if (erg.dev) {
        block.push(erg.text); raus();
        zeigeHtml(fensterHtml(stand(), IHR_PROJEKT, false), "[Lernkarten-Fenster]");
      } else if (erg.flatpak) {
        raus();
        zeigeHtml(fensterHtml(zustand.installiert, FLATPAK, false), "[Lernkarten-Fenster]");
      } else if (erg.tabelle) {
        raus();
        jsonTabelle(erg.tabelle);
      }
      block.push("");
    }
    raus();
  }

  if (!self.__lkEvalOriginal) { self.__lkEvalOriginal = self.eval; }
  self.eval = function (code) {
    var anfang = code.replace(/^\s+/, "");
    if (anfang.indexOf("# Terminal") === 0) { terminal(anfang); return undefined; }
    if (anfang.indexOf("# Anwendungsmenü") === 0) { menue(); return undefined; }
    if (anfang.indexOf("# Fertige App") === 0) { zeigeHtml(fensterHtml(FERTIG_STAND, FERTIG, false), "[Lernkarten-Fenster]"); return undefined; }
    var ebene = /^# Ebene ([123])/.exec(anfang);
    if (ebene) {
      var n = Number(ebene[1]);
      var titel = ["", "Ebene 1 · nur index.html (Rohbau)", "Ebene 2 · index.html + style.css (Rohbau + Anstrich)", "Ebene 3 · alle drei Dateien (Rohbau + Anstrich + Bewohner)"][n];
      var teil = { html: FERTIG_STAND.html, css: n >= 2 ? FERTIG_STAND.css : "", js: n >= 3 ? FERTIG_STAND.js : "", name: "Lernkarten" };
      zeigeHtml(fensterHtml(teil, { schluessel: FERTIG.schluessel, pfad: "", titel: titel, schlicht: true }, false), "[Lernkarten-Fenster]");
      return undefined;
    }
    if (anfang.indexOf("[Desktop Entry]") === 0) {
      dateien.desktop = anfang;
      var name = desktopName(anfang);
      if (!name) { console.log("❌ Die Zeile Name= fehlt oder ist leer. Ohne Namen kein Menüeintrag."); return undefined; }
      if (!/^Exec=lernkarten\s*$/m.test(anfang) || !/^Icon=de\.metarow\.Lernkarten\s*$/m.test(anfang)) {
        console.log("⚠️ Exec= oder Icon= wurde verändert. Ändern Sie nur Name= und Comment=, der Rest muss zur Bauanleitung passen.");
      }
      console.log("✅ de.metarow.Lernkarten.desktop gespeichert. Anzeigename: " + name);
      console.log("   Ins Anwendungsmenü kommt der neue Name erst mit dem nächsten Bau und Installieren.");
      return undefined;
    }
    if (anfang.indexOf("// app.js") === 0) { dateien.js = anfang; console.log("✅ app.js gespeichert."); return undefined; }
    if (anfang.indexOf("<!-- index.html") === 0) {
      dateien.html = anfang;
      console.log("✅ index.html gespeichert. Das Fenster Ihres Projekts zeigt jetzt:");
      zeigeHtml(fensterHtml(stand(), IHR_PROJEKT, false), "[Lernkarten-Fenster]");
      return undefined;
    }
    if (anfang.indexOf("/* style.css") === 0) { dateien.css = anfang; console.log("✅ style.css gespeichert."); return undefined; }
    return self.__lkEvalOriginal(code);
  };

  console.log("🧰 Werkzeugkiste bereit: fertige App, Übungs-Terminal und Vorschau für Ihr Projekt.");
})();
