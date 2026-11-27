// Vorbereitete Werkzeugkiste für M5: nur ausführen, nicht lesen müssen.
// Sie verwendet Schreibweisen, die im Kurs bewusst NICHT vorkommen.
// Was sie tut: Jede Zelle, die mit "// app.js" beginnt, wird nicht hier im
// Notebook ausgeführt, sondern in einem kleinen Anwendungsfenster mit
// index.html und style.css – samt eigener Konsole darunter.
// Neu in M5: Sie spielt auch den Programmkern (main.rs). window.__TAURI__.core.invoke
// kennt "karten_laden" und "karten_speichern" und hält lernkarten.json im Speicher
// des Browsers fest, damit die Karten einen Neustart überleben.
(function () {
  var STANDARD_HTML = __HTML__;
  var STANDARD_CSS = __CSS__;

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
  var dateien = { html: STANDARD_HTML, css: STANDARD_CSS };
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
  function fensterSkript(versatz) {
    return "(" + function (VERSATZ) {
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
      var SCHLUESSEL = "tauri-kompaktkurs/lernkarten.json";
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
    }.toString() + ")(" + versatz + ");";
  }

  function fenster(appJs, hinweis) {
    laeufe = laeufe + 1;
    var html = ohneKennung(dateien.html);
    var css = ohneKennung(dateien.css);
    var oben = "<!DOCTYPE html>\n<html lang=\"de\">\n<head>\n<meta charset=\"UTF-8\">\n" +
      "<style>\n" + css + "\n</style>\n<script>__SHIM__<\/script>\n</head>\n<body>\n" +
      koerper(html) + "\n<script>\n";
    var versatz = oben.split("\n").length - 1 + fensterSkript(0).split("\n").length - 1;
    var dokument = oben.replace("__SHIM__", fensterSkript(versatz)) + appJs + "\n<\/script>\n</body>\n</html>";
    var leerText = hinweis || "(noch keine Ausgabe)";
    var aussen =
      '<div class="lk-fenster" style="max-width:760px;border:1px solid #9e9e9e;border-radius:10px;overflow:hidden;' +
      'box-shadow:0 3px 12px rgba(0,0,0,.18);margin:6px 0;font-family:system-ui,sans-serif;">' +
      '<div style="background:#303030;color:#f0f0f0;padding:6px 12px;font-size:13px;display:flex;justify-content:space-between;align-items:center;">' +
      '<span>🗂️ ' + htmlText(titel(dateien.html)) + '</span>' +
      '<button class="lk-neustart" title="App schließen und neu starten" style="background:#4a4a4a;color:#f0f0f0;border:1px solid #6a6a6a;border-radius:5px;padding:2px 10px;font-size:12px;cursor:pointer;">⟳ Neu starten</button></div>' +
      '<iframe title="Lernkarten-Fenster" srcdoc="' + attribut(dokument) + '" ' +
      'style="display:block;width:100%;height:420px;border:0;background:#ffffff;"></iframe>' +
      '<div style="border-top:2px solid #9e9e9e;background:#f6f6f6;color:#1f1f1f;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;">' +
      '<div style="padding:4px 10px;background:#e4e4e4;color:#444;font-family:system-ui,sans-serif;font-size:12px;">Konsole</div>' +
      '<div class="lk-konsole" style="padding:4px 10px 6px 10px;min-height:20px;">' +
      '<div class="lk-leer" style="color:#888;">' + htmlText(leerText) + '</div></div></div>' +
      '<div style="border-top:2px solid #9e9e9e;background:#fffdf2;color:#1f1f1f;font-size:12px;">' +
      '<div style="padding:4px 10px;background:#eee6c8;color:#444;display:flex;justify-content:space-between;align-items:center;gap:8px;">' +
      '<span>📄 lernkarten.json <span class="lk-datei-info" style="opacity:.75"></span></span>' +
      '<button class="lk-datei-loeschen" title="Datei löschen, als wäre die App frisch installiert" style="background:#fff;color:#444;border:1px solid #bbb;border-radius:5px;padding:1px 8px;font-size:12px;cursor:pointer;">🗑 Datei löschen</button></div>' +
      '<pre class="lk-datei" style="margin:0;padding:6px 10px;max-height:200px;overflow:auto;white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;background:transparent;color:#1f1f1f;"></pre>' +
      '</div></div>';
    postMessage({
      type: "display_data",
      bundle: { data: { "text/html": aussen, "text/plain": "[Lernkarten-Fenster]" }, metadata: {}, transient: {} }
    });
  }

  if (!self.__lkEvalOriginal) { self.__lkEvalOriginal = self.eval; }
  self.eval = function (code) {
    var anfang = code.replace(/^\s+/, "");
    if (anfang.indexOf("// app.js") === 0) {
      fenster(code);
      return undefined;
    }
    if (anfang.indexOf("<!-- index.html") === 0) {
      dateien.html = code;
      console.log("✅ index.html übernommen. So sieht die Oberfläche ohne app.js aus:");
      fenster("", "(leer: es gibt noch kein app.js)");
      return undefined;
    }
    if (anfang.indexOf("/* style.css") === 0) {
      dateien.css = code;
      console.log("✅ style.css übernommen. So sieht die Oberfläche ohne app.js aus:");
      fenster("", "(leer: es gibt noch kein app.js)");
      return undefined;
    }
    return self.__lkEvalOriginal(code);
  };

  console.log("🧰 Werkzeugkiste bereit. Zellen, die mit // app.js beginnen, öffnen ein Fenster mit Programmkern.");
})();
