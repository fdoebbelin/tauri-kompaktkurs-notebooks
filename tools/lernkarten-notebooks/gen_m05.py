"""Erzeugt content/M05_Daten_behalten.ipynb für die JupyterLite-Seite."""
import json
import pathlib
import sys

HIER = pathlib.Path(__file__).parent

# Helfer, Dateien und K4-Bausteine aus dem M4-Generator übernehmen
_m04 = (HIER / "gen_m04.py").read_text(encoding="utf-8")
exec(_m04.split("# ================================================================== Einstieg")[0])

SETUP = (HIER / "m05_setup.js").read_text(encoding="utf-8")
SETUP = SETUP.replace("__HTML__", json.dumps(INDEX_HTML, ensure_ascii=False))
SETUP = SETUP.replace("__CSS__", json.dumps(STYLE_CSS, ensure_ascii=False))

# ------------------------------------------------------------------ K5-Bausteine
DATEN_LEER = DATEN.replace(
    """const karten = [
  { frage: "Was ist HTML?", antwort: "Die Struktur einer Seite" },
  { frage: "Was ist CSS?", antwort: "Das Aussehen einer Seite" },
  { frage: "Was ist eine id?", antwort: "Der Name eines Elements" }
];""",
    """// Die Karten kommen ab jetzt aus der Datei. Die Liste startet leer.
const karten = [];""")
assert DATEN_LEER != DATEN

SPEICHERN = """
async function speichern() {
  await window.__TAURI__.core.invoke("karten_speichern", { karten: karten });
  console.log("gespeichert");
}
"""

LADEN = """
async function laden() {
  const geladen = await window.__TAURI__.core.invoke("karten_laden");
  for (const karte of geladen) {
    karten.push(karte);
  }
  listeAnzeigen();
}
"""

START_LADEN = """
// Beim Start: Karten aus der Datei laden
laden();
"""

NEU_K5 = NEU.replace('knopfNeu.addEventListener("click", function () {',
                     'knopfNeu.addEventListener("click", async function () {')
NEU_K5 = NEU_K5.replace("  karteAnlegen(frage, antwort);\n  listeAnzeigen();\n",
                        "  karteAnlegen(frage, antwort);\n  listeAnzeigen();\n  await speichern();\n")
assert NEU_K5.count("async") == 1 and "await speichern" in NEU_K5

# ================================================================== Einstieg
md(r"""
# M5 – Daten behalten

*Begleit-Notebook zu Modul **K5 „Daten behalten“** im Kompaktkurs „Vom Web zur Desktop-App mit Tauri“*

Ihre Lernkarten-App funktioniert, aber sie hat **kein Gedächtnis**: Nach jedem Neustart sind Ihre Karten weg. In diesem Modul schlagen Sie die Brücke zum zweiten Teil Ihrer Anwendung, dem **Programmkern** in Rust. Er schreibt die Karten in eine Datei, und sie überleben den Neustart.

Das ist der Punkt, an dem sich Ihre Anwendung von einer Webseite unterscheidet.

## 🎯 Das können Sie am Ende

- erklären, warum eine Webseite keine Dateien schreiben darf, eine installierte Anwendung aber schon
- die zwei Teile der Anwendung benennen: **Fenster** und **Programmkern**
- die beiden vorbereiteten Funktionen in `main.rs` in eigenen Worten beschreiben
- mit `invoke`, `await` und `async` den Programmkern aufrufen, als **Rezept**
- `speichern()` und `laden()` schreiben und an den richtigen Stellen aufrufen
- den Merksatz anwenden: **Wo `await` steht, muss `async` davorstehen.**

## 🧭 Inhalt

0. Vorbereitung
1. Das Problem: Nach dem Neustart ist alles weg
2. Die zwei Teile einer Desktop-Anwendung
3. Der vorbereitete Programmkern
4. Der erste Aufruf: `speichern()`
5. Laden beim Start
6. Speichern an den richtigen Stellen
7. Absichtlicher Fehler: das fehlende `await`
8. Fehlerjagd
9. Wo liegt die Datei? Und eine Werkstatt für Schnellere
10. Diagnosetabelle, Checkliste und Ausblick auf K6
""")

md(r"""
## So funktioniert dieses Notebook

Wie in M4 öffnet jede Zelle, die mit **`// app.js`** beginnt, ein kleines Anwendungsfenster mit Konsole. Neu sind zwei Dinge:

| Neu | Wozu |
|---|---|
| Knopf **⟳ Neu starten** oben im Fenster | schließt die App und startet sie neu, so wie Schließen und Öffnen der echten Anwendung |
| Bereich **📄 lernkarten.json** unter der Konsole | zeigt, was gerade in der Datei steht, und meldet jeden Zugriff des Programmkerns |
| Knopf **🗑 Datei löschen** | setzt die Datei zurück, als wäre die App frisch installiert |

> **📌 Ehrlicher Hinweis: Hier spielt die Werkzeugkiste den Programmkern.**
> Im Notebook gibt es kein Rust. Die Vorbereitungszelle bildet die beiden Funktionen aus `main.rs` nach und legt `lernkarten.json` im Speicher Ihres Browsers ab. Für Ihr JavaScript sieht das genauso aus wie in der echten App: Sie rufen `window.__TAURI__.core.invoke(...)` auf und bekommen dieselben Antworten und Fehlermeldungen.
> Die Datei bleibt erhalten, auch wenn Sie eine Zelle erneut ausführen oder das Notebook schließen. Alle Fenster in diesem Notebook teilen sich **eine** Datei.

Die Zeichen kennen Sie: 🤔 **Vorhersage** · ✏️ **Ihre Aufgabe** · 🐞 **Absichtlicher Fehler** · 🖱️ **Klicken Sie** · 💡 **Lösung**.
""")

# ================================================================== 0
md(r"""
---
## 0 Vorbereitung

Führen Sie die eingeklappte Zelle **als Erstes** aus. Sie enthält die Werkzeugkiste aus M4 mit dem nachgebildeten Programmkern und Ihre `index.html` und `style.css` aus K1 und K2.

Wenn darunter **🧰 Werkzeugkiste bereit** steht, kann es losgehen.

> Wer seine eigene Oberfläche aus M4 verwenden möchte, kopiert die `index.html`- und `style.css`-Zellen von dort hierher und führt sie nach der Vorbereitung aus.
""")

code(SETUP, hidden=True)

# ================================================================== 1
md(r"""
---
## 1 Das Problem: Nach dem Neustart ist alles weg

Das ist Ihr `app.js` vom Ende von K4. 🖱️ Legen Sie eine eigene Karte an. Klicken Sie dann oben im Fenster auf **⟳ Neu starten**.
""")

app(DATEN, LISTE, NEU, UMDREHEN, WEITER, START)

md(r"""
Ihre Karte ist weg. Beim Start stehen wieder nur die drei Karten, die im Programmtext stehen. Alles, was beim Benutzen dazukam, lebte nur im Arbeitsspeicher, und der wird beim Schließen geräumt.

### 🤔 Warum kann eine Webseite das nicht?

Überlegen Sie, bevor Sie aufklappen: Warum darf eine Webseite keine Dateien auf Ihren Rechner schreiben?
""")

loesung("💡 Antwort", r"""
Eine Webseite kommt von einem **fremden Server**. Sie wird beim Surfen einfach geladen, ohne dass Sie gefragt werden. Dürfte sie in Ihre Dateien schreiben, könnte jede Seite, die Sie besuchen, das auch.

Eine installierte Anwendung haben Sie **bewusst installiert**. Deshalb darf sie das.

> **Eine Webseite ist ein Gast. Eine installierte Anwendung ist eingezogen und hat einen Schlüssel für die Schränke.**
> Der Unterschied ist nicht die Technik, sondern die Erlaubnis.
""")

# ================================================================== 2
md(r"""
---
## 2 Die zwei Teile einer Desktop-Anwendung

```mermaid
flowchart LR
  A["Fenster<br/>index.html + style.css + app.js"] -->|invoke| B["Programmkern<br/>main.rs"]
  B --> C[(lernkarten.json)]
  B -->|Antwort| A
```

| Teil | Was man sieht | Was er darf |
|---|---|---|
| **Fenster** | alles: HTML, CSS, JavaScript | anzeigen, rechnen, auf Klicks reagieren |
| **Programmkern** | nichts | auf die Festplatte zugreifen |

Bis jetzt lief alles im Fenster. Ab jetzt **ruft das Fenster den Programmkern** und bittet ihn, etwas zu tun. Erinnern Sie sich an die zwei Ausgabeorte aus K3? Das **Terminal** zeigt Meldungen des Programmkerns, die **Konsole** zeigt Meldungen aus dem Fenster.

### 🤔 Wer macht was?

| Aufgabe | Fenster oder Programmkern? |
|---|---|
| den Knopf „Karte anlegen“ anzeigen | |
| auf den Klick reagieren | |
| die Liste `karten` im Arbeitsspeicher ergänzen | |
| die Karten in `lernkarten.json` schreiben | |
| die Datei beim Start lesen | |
| die gelesenen Karten in der Liste anzeigen | |
""")

loesung("💡 Auflösung", r"""
| Aufgabe | Wer |
|---|---|
| Knopf anzeigen | Fenster |
| auf den Klick reagieren | Fenster |
| `karten` ergänzen | Fenster |
| in `lernkarten.json` schreiben | **Programmkern** |
| die Datei lesen | **Programmkern** |
| gelesene Karten anzeigen | Fenster |

Nur die beiden Zugriffe auf die Datei gehören dem Programmkern. Alles andere bleibt, wo es war.
""")

# ================================================================== 3
md(r"""
---
## 3 Der vorbereitete Programmkern

Die Datei `src-tauri/src/main.rs` ist vollständig vorbereitet. **Rust wird nicht unterrichtet.** Sie lesen sie nur und beschreiben in normalem Deutsch, was passiert.

> Ihre Kursleitung hat die echte Datei. Sie kann im Detail etwas anders aussehen, die beiden Funktionen und ihre Namen sind dieselben.

```rust
use std::fs;
use tauri::Manager;

#[tauri::command]
fn karten_speichern(app: tauri::AppHandle, karten: serde_json::Value) {
    let ordner = app.path().app_data_dir().unwrap();
    fs::create_dir_all(&ordner).unwrap();
    let text = serde_json::to_string_pretty(&karten).unwrap();
    fs::write(ordner.join("lernkarten.json"), text).unwrap();
}

#[tauri::command]
fn karten_laden(app: tauri::AppHandle) -> serde_json::Value {
    let datei = app.path().app_data_dir().unwrap().join("lernkarten.json");
    match fs::read_to_string(datei) {
        Ok(text) => serde_json::from_str(&text).unwrap(),
        Err(_) => serde_json::json!([]),
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![karten_speichern, karten_laden])
        .run(tauri::generate_context!())
        .unwrap();
}
```

In normalem Deutsch:

| Stelle | Was sie bedeutet |
|---|---|
| `#[tauri::command]` | „Diese Funktion darf vom Fenster aus aufgerufen werden.“ |
| `fn karten_speichern(…, karten: …)` | eine Funktion mit dem Namen `karten_speichern`, sie bekommt `karten` mit |
| `app_data_dir()` | der **Anwendungsdatenordner**, ein fester Ordner nur für diese App |
| `to_string_pretty(&karten)` | die Liste in lesbaren Text verwandeln |
| `fs::write(… "lernkarten.json" …)` | den Text in die Datei schreiben |
| `fn karten_laden(…) -> …` | eine Funktion, die etwas **zurückgibt**, wie `return` in JavaScript |
| `Ok(text) => …` | Datei gefunden: den Text wieder in eine Liste verwandeln |
| `Err(_) => json!([])` | keine Datei da, zum Beispiel beim ersten Start: eine **leere Liste** zurückgeben |
| `generate_handler![…]` | die Liste der Funktionen, die das Fenster aufrufen darf |

| Funktion | Was sie tut |
|---|---|
| `karten_speichern(karten)` | schreibt die Liste als JSON in `lernkarten.json` im Anwendungsdatenordner |
| `karten_laden()` | liest die Datei und gibt die Liste zurück; fehlt die Datei, gibt sie eine leere Liste zurück |

> **Warum nicht das Datei-Plugin von Tauri?** Die Tauri-Plugins brauchen Node und einen Bundler. Der Kurs kommt ohne Node aus. Zwei vorbereitete Funktionen sind der einfachere Weg.

✏️ **Ihre Aufgabe:** Beschreiben Sie jede der beiden Funktionen in **einem** Satz, ohne die Tabelle anzusehen.
""")

# ================================================================== 4
md(r"""
---
## 4 Der erste Aufruf: `speichern()`

Diese Funktion ruft den Programmkern und bittet ihn, die Karten zu speichern. Ganz unten wird sie einmal zum Ausprobieren aufgerufen.

🖱️ Führen Sie die Zelle aus und schauen Sie auf die Konsole und auf **📄 lernkarten.json**.
""")

app(DATEN, LISTE, NEU, UMDREHEN, WEITER, neu(SPEICHERN), START,
    "// ★ NEU: einmal ausprobieren\nspeichern();")

md(r"""
In der Datei stehen jetzt Ihre drei Karten. Fällt Ihnen etwas auf? Der Text sieht fast genauso aus wie die Liste `karten` in Ihrem `app.js`. Diese Schreibweise heißt **JSON**: Listen und Objekte als Text, so dass sie in einer Datei Platz haben.

### Drei Wörter als Rezept

Diese drei Wörter lernen Sie als **Rezept**, nicht als Konzept:

| Wort | Rezeptregel |
|---|---|
| `invoke` | „Ruf den Programmkern.“ |
| `await` | „Warte, bis er fertig ist.“ |
| `async` | „Diese Funktion darf warten.“ |

> ## Merksatz: Wo `await` steht, muss `async` davorstehen.

Der Aufruf hat drei Teile:

| Teil | Bedeutung |
|---|---|
| `window.__TAURI__.core.invoke` | die Tür zum Programmkern |
| `"karten_speichern"` | der Name der Funktion dort drüben. Er muss **exakt** zum Namen in `main.rs` passen. |
| `{ karten: karten }` | die Daten, die mitgegeben werden |

> **Die geschweiften Klammern sind hier ein eigenes Ding.** `{ karten: karten }` ist die Liste der Angaben für den Aufruf. **Links** steht der Name, den die Rust-Funktion erwartet (`karten: …` in `main.rs`), **rechts** der Wert, der hingeschickt wird: Ihre Liste `karten`.

### 🐞 Absichtlicher Fehler: `await` ohne `async`

🤔 Hier fehlt ein Wort. Was meldet die Konsole?
""")

app(DATEN, LISTE, """
function speichern() {
  await window.__TAURI__.core.invoke("karten_speichern", { karten: karten });
  console.log("gespeichert");
}
""", START, "speichern();")

md(r"""
`SyntaxError: await is only valid in async functions …` mit Zeilennummer. Übersetzt: *`await` ist nur in `async`-Funktionen erlaubt.* Die Meldung sagt genau, was fehlt. Sie muss nur gelesen werden.

Beachten Sie: Bei einem `SyntaxError` läuft **gar nichts**, auch nicht `listeAnzeigen()`. Der Fehler steckt in der Schreibweise, deshalb wird die ganze Datei nicht ausgeführt. Setzen Sie `async` vor `function` und führen Sie die Zelle erneut aus.

### 🐞 Absichtlicher Fehler: der falsche Name

🤔 Lesen Sie den Namen im `invoke` und den Namen in `main.rs` **laut** nebeneinander.
""")

app(DATEN, LISTE, """
async function speichern() {
  await window.__TAURI__.core.invoke("karten_Speichern", { karten: karten });
  console.log("gespeichert");
}
""", START, "speichern();")

md(r"""
`Command karten_Speichern not found`: Der Programmkern kennt keine Funktion mit diesem Namen. Groß- und Kleinschreibung zählt, genau wie bei den `id`s in K4. Und `gespeichert` erscheint nicht, weil der Aufruf vorher abgebrochen ist.

Reparieren Sie den Namen.
""")

# ================================================================== 5
md(r"""
---
## 5 Laden beim Start

Ab jetzt ist die **Datei** der Datenbestand. Deshalb stehen keine Karten mehr im Programmtext: Die Liste startet **leer** und wird beim Start aus der Datei gefüllt.

🖱️ Führen Sie die Zelle aus. Legen Sie noch **keine** Karte an.
""")

app(neu(DATEN_LEER), LISTE, SPEICHERN, neu(LADEN), NEU, UMDREHEN, WEITER, neu(START_LADEN))

md(r"""
Die drei Karten erscheinen, obwohl `karten` leer startet. Sie kommen aus der Datei, die Sie in Abschnitt 4 geschrieben haben. Der Bereich 📄 meldet `karten_laden: 3 Karten gelesen`.

> Steht bei Ihnen „Noch keine Karte“ und die Liste ist leer? Dann gibt es die Datei noch nicht. Führen Sie die Zelle aus Abschnitt 4 einmal aus.

Zeile für Zeile:

| Zeile | Was sie tut |
|---|---|
| `const geladen = await …invoke("karten_laden")` | den Programmkern fragen und die Antwort **abwarten** |
| `for (const karte of geladen)` | jede geladene Karte durchgehen |
| `karten.push(karte);` | sie in die Liste der Anwendung übernehmen |
| `listeAnzeigen();` | die Anzeige neu aufbauen, **sonst ist alles da und unsichtbar** |

> **`listeAnzeigen()` nicht vergessen.** Nach dem Laden sind die Daten da, aber der Bildschirm zeigt noch die leere Liste. Das ist derselbe Fehler wie in K4, jetzt mit einer anderen Ursache.

Der Aufruf `laden();` ganz unten steht **ohne** `await`. Das ist Absicht: Der Start soll nicht warten, das Laden passiert nebenbei.

### 🐞 Warum startet `karten` jetzt leer?

🤔 In dieser Fassung stehen die drei Beispielkarten noch im Programmtext, so wie in K4. Was zeigt die Liste?
""")

app(DATEN, LISTE, SPEICHERN, LADEN, NEU, UMDREHEN, WEITER, START_LADEN)

md(r"""
**Sechs** Einträge, jede Karte doppelt: drei aus dem Programmtext, drei aus der Datei. Und es wird schlimmer: Sobald gespeichert wird, stehen alle sechs in der Datei, und beim nächsten Start sind es neun.

Deshalb gilt ab K5: **Der Programmtext enthält keine Karten mehr.** `const karten = [];` und alles Weitere kommt aus der Datei.
""")

# ================================================================== 6
md(r"""
---
## 6 Speichern an den richtigen Stellen

Laden funktioniert. 🖱️ Probieren Sie jetzt: Legen Sie eine eigene Karte an und klicken Sie auf **⟳ Neu starten**.
""")

app(DATEN_LEER, LISTE, SPEICHERN, LADEN, NEU, UMDREHEN, WEITER, START_LADEN)

md(r"""
Ihre Karte ist wieder weg. Geladen wird, aber gespeichert wird nie. Schauen Sie auf 📄: Ihre Karte steht nicht in der Datei.

### 🤔 Die Frage: Wo muss `speichern()` aufgerufen werden?

Diese Suche ist die eigentliche Übung, nicht der Code. Die Antwort sind die Stellen, an denen sich **die Daten ändern**:

| Stelle | Nach was | Gibt es das schon? |
|---|---|---|
| nach dem **Anlegen** einer Karte | eine Karte kam dazu | ja, Knopf „Karte anlegen“ |
| nach dem **Löschen** einer Karte | eine Karte ist weg | kommt in K6 |
| nach dem **Ändern** einer Karte | der Inhalt ist anders | kommt in K6 |

„Umdrehen“ und „Nächste“ ändern nur, **was angezeigt wird**, nicht die Daten. Dort wird nicht gespeichert.

### ✏️ Ihre Aufgabe 6

Bauen Sie in der Zelle oben das Speichern in den Knopf „Karte anlegen“ ein:

1. Setzen Sie hinter `listeAnzeigen();` die Zeile `await speichern();`
2. Führen Sie die Zelle aus. Was meldet die Konsole? Denken Sie an den Merksatz.
3. Reparieren Sie, legen Sie eine Karte an, klicken Sie **⟳ Neu starten**. Bleibt die Karte?
""")

loesung("💡 Lösung 6", r"""
Die Funktion im Klick braucht jetzt auch ein `async`, denn in ihr steht ein `await`:

```js
knopfNeu.addEventListener("click", async function () {
  // … Werte holen, prüfen …

  karteAnlegen(frage, antwort);
  listeAnzeigen();
  await speichern();

  document.querySelector("#frage-feld").value = "";
  document.querySelector("#antwort-feld").value = "";
});
```

Ohne `async` meldet die Konsole denselben `SyntaxError` wie in Abschnitt 4.

> **Speichern an nur einer Stelle reicht nicht.** Sobald es in K6 einen Löschknopf gibt, muss auch dort gespeichert werden. Sonst sind gelöschte Karten beim nächsten Start wieder da. Der Fehler ist beim Ausprobieren harmlos und fällt erst später auf.
""")

md(r"""
### So sieht `app.js` am Ende von K5 aus

🖱️ Die Probe, auf die alles hinausläuft: Legen Sie zwei Karten an, klicken Sie **⟳ Neu starten**, und Ihre Karten sind noch da. Führen Sie die Zelle sogar erneut aus: Sie bleiben.
""")

app(DATEN_LEER, LISTE, SPEICHERN, LADEN, NEU_K5, UMDREHEN, WEITER, START_LADEN)

# ================================================================== 7
md(r"""
---
## 7 🐞 Absichtlicher Fehler: das fehlende `await`

In `laden()` fehlt das `await`. Zum Vergleichen gibt die Funktion aus, was sie vom Programmkern bekommt. 🤔 **Vorhersage:** Was steht in der Konsole?
""")

app(DATEN_LEER, LISTE, """
async function laden() {
  const geladen = window.__TAURI__.core.invoke("karten_laden");
  console.log(geladen);
  for (const karte of geladen) {
    karten.push(karte);
  }
  listeAnzeigen();
}
""", START_LADEN)

md(r"""
In der Konsole steht **`Promise { <pending> }`** statt der Liste, und danach `TypeError: geladen is not iterable`.

> „Das Programm war zu schnell und hat nicht gewartet. Der Programmkern arbeitet im Hintergrund, aber das Fenster wollte sofort weiter und hatte die Antwort noch nicht.“

Ein `Promise` ist ein **Versprechen**: „Die Antwort kommt noch.“ Ohne `await` bekommen Sie das Versprechen, nicht die Antwort. Mit `await` warten Sie, bis das Versprechen eingelöst ist.

Setzen Sie das `await` wieder vor `window.__TAURI__…` und führen Sie die Zelle erneut aus. Jetzt steht in der Konsole die Liste.
""")

# ================================================================== 8
md(r"""
---
## 8 Fehlerjagd

In jeder Zelle steckt **genau ein** Fehler. Darüber steht, was passieren **soll**. Schauen Sie auf Konsole **und** 📄.

**a)** 🖱️ Eine neue Karte soll angelegt und gespeichert werden.
""")

app(DATEN_LEER, LISTE, SPEICHERN, LADEN,
    NEU_K5.replace("async function () {", "function () {"), START_LADEN)

md(r"""
**b)** Beim Start sollen die Karten aus der Datei erscheinen.
""")

app(DATEN_LEER, LISTE, LADEN.replace('"karten_laden"', '"karten_lade"'), START_LADEN)

md(r"""
**c)** Beim Start sollen die Karten aus der Datei erscheinen.
""")

app(DATEN_LEER, LISTE, """
async function laden() {
  const geladen = await window.__TAURI__.core.invoke("karten_laden");
  for (const karte of geladen) {
    karten.push(karte);
  }
  console.log("Karten im Datenbestand: " + karten.length);
}
""", START_LADEN)

md(r"""
**d)** Beim Start sollen die drei Beispielkarten gespeichert werden.
""")

app(DATEN, LISTE, SPEICHERN.replace("{ karten: karten }", "{ liste: karten }"), START, "speichern();")

md(r"""
**e)** 🖱️ Nach dem Anlegen einer Karte soll die **neue** Karte in der Datei stehen. Legen Sie eine an und schauen Sie in 📄.
""")

app(DATEN_LEER, LISTE, SPEICHERN, LADEN,
    NEU_K5.replace("  karteAnlegen(frage, antwort);\n  listeAnzeigen();\n  await speichern();\n",
                   "  await speichern();\n  karteAnlegen(frage, antwort);\n  listeAnzeigen();\n"),
    START_LADEN)

loesung("💡 Lösungen zur Fehlerjagd", r"""
| | Was Sie sehen | Ursache | Reparatur |
|---|---|---|---|
| a) | `SyntaxError: await is only valid in async functions …`, das ganze Fenster tut nichts | `await speichern()` in einer Funktion ohne `async` | `async function () {` |
| b) | `Command karten_lade not found` | Name passt nicht zu `main.rs` | `"karten_laden"` |
| c) | Konsole meldet 3 Karten, die Liste im Fenster bleibt leer | `listeAnzeigen()` fehlt nach dem Laden | `listeAnzeigen();` am Ende von `laden()` |
| d) | ``invalid args `karten` for command `karten_speichern` …`` | links in `{ … }` muss der Name aus `main.rs` stehen | `{ karten: karten }` |
| e) | die neue Karte fehlt in der Datei, sie kommt erst beim nächsten Anlegen dazu | erst gespeichert, dann angelegt | `await speichern();` nach `karteAnlegen` |

Bei c) und e) gibt es **keine** Fehlermeldung. Bei e) merken Sie den Fehler erst nach einem Neustart: Die zuletzt angelegte Karte ist weg. Wer auf 📄 schaut, sieht es sofort.

Wenn die Datei durch die Fehlerjagd durcheinandergeraten ist: **🗑 Datei löschen** und die Zelle aus Abschnitt 4 einmal ausführen.
""")

# ================================================================== 9
md(r"""
---
## 9 Wo liegt die Datei? Und eine Werkstatt für Schnellere

### In der echten App

Der Programmkern schreibt in den **Anwendungsdatenordner**, nicht in Ihren Projektordner. Unter Linux liegt er in Ihrem Home-Verzeichnis unter `.local/share/` und heißt wie die Kennung der App:

```nu
ls ~/.local/share/de.metarow.Lernkarten
```

Und so sehen Sie den Inhalt. Nushell zeigt eine JSON-Datei sogar gleich als Tabelle an:

```nu
open ~/.local/share/de.metarow.Lernkarten/lernkarten.json
```

> **Wer im Projektordner sucht, findet nichts.** Die App darf in „ihren“ Ordner schreiben, nicht irgendwohin. Das ist dieselbe Idee wie der Schlüssel für die Schränke: Sie hat den Schlüssel für **ihren** Schrank.

Hier im Notebook ist der Bereich 📄 Ihr Blick in diese Datei.

### Werkstatt für Schnellere

Kein neuer Stoff, nur Verbesserungen mit dem, was Sie schon können. Arbeiten Sie in der Zelle unten.

1. **Gleich etwas zeigen:** Nach dem Laden soll sofort die Frage der ersten Karte in `#karte-frage` stehen, falls es Karten gibt.
2. **Willkommenskarten:** Ist die Datei beim Start leer (frisch installiert), legt die App drei Startkarten an und speichert sie. Probieren Sie es mit **🗑 Datei löschen** und **⟳ Neu starten**.
""")

app(DATEN_LEER, LISTE, SPEICHERN, LADEN, NEU_K5, UMDREHEN, WEITER, START_LADEN)

loesung("💡 Lösungsideen", r"""
Beide Ideen gehören in `laden()`, hinter die Schleife:

```js
async function laden() {
  const geladen = await window.__TAURI__.core.invoke("karten_laden");
  for (const karte of geladen) {
    karten.push(karte);
  }

  // 2. Willkommenskarten
  if (karten.length === 0) {
    karteAnlegen("Was ist HTML?", "Die Struktur einer Seite");
    karteAnlegen("Was ist CSS?", "Das Aussehen einer Seite");
    karteAnlegen("Was ist JavaScript?", "Das Verhalten einer Seite");
    await speichern();
  }

  listeAnzeigen();

  // 1. Gleich etwas zeigen
  if (karten.length > 0) {
    document.querySelector("#karte-frage").textContent = karten[0].frage;
  }
}
```

`await speichern()` geht hier ohne Weiteres, denn `laden()` ist schon `async`.
""")

# ================================================================== 10
md(r"""
---
## 10 Diagnosetabelle, Checkliste und Ausblick

### Die Diagnosetabelle, erweitert um K5

| Was zu sehen ist | Was das meistens heißt |
|---|---|
| `SyntaxError: await is only valid in async functions` | `async` fehlt vor der Funktion, in der `await` steht |
| `Promise { <pending> }` statt einer Liste | `await` vergessen |
| `… is not iterable` direkt nach einem `invoke` | `await` vergessen |
| `Command … not found` | Name im `invoke` passt nicht zu `main.rs` |
| `invalid args … missing required key …` | Name links in `{ … }` passt nicht zu `main.rs` |
| Daten geladen (Konsole), Liste leer | `listeAnzeigen()` fehlt nach dem Laden |
| Karten nach dem Neustart weg | an dieser Stelle wird nicht gespeichert |
| Karten stehen nach jedem Start doppelt | Beispielkarten stehen noch im Programmtext |
| Datei im Projektordner nicht gefunden | sie liegt im Anwendungsdatenordner `~/.local/share/de.metarow.Lernkarten` |

### ✅ Checkliste

Haken Sie ab (Doppelklick auf diese Zelle, dann `[ ]` zu `[x]` ändern):

- [ ] Ich kann erklären, warum eine Webseite keine Dateien schreiben darf und eine installierte App schon
- [ ] Ich kann die beiden Funktionen aus `main.rs` in eigenen Worten beschreiben
- [ ] Ich habe `speichern()` geschrieben und die Datei `lernkarten.json` angesehen
- [ ] Ich habe `laden()` geschrieben und beim Start aufgerufen
- [ ] Ich weiß, warum `karten` jetzt leer startet
- [ ] Ich habe alle Stellen gefunden, an denen gespeichert werden muss
- [ ] Meine Karten überleben den Neustart
- [ ] Ich habe den Merksatz parat: **Wo `await` steht, muss `async` davorstehen.**

### Wie geht es weiter?

Ihre App kann jetzt alles, was sie können muss. In **K6 „Feinschliff“** machen Sie sie zu Ihrer eigenen: eigene Gestaltung und eine kleine Verbesserung, zum Beispiel ein Löschknopf für einzelne Karten. Denken Sie dann an diese Seite: **Nach dem Löschen muss gespeichert werden.**

**Zum Nachschlagen:** K5 Merkblatt · K5 Übungsblatt · Anhang Befehlskarte
""")

# ------------------------------------------------------------------ schreiben
nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"name": "javascript", "display_name": "JavaScript", "language": "javascript"},
        "language_info": {
            "codemirror_mode": {"name": "javascript"},
            "file_extension": ".js",
            "mimetype": "text/javascript",
            "name": "javascript",
            "nbconvert_exporter": "javascript",
            "pygments_lexer": "javascript",
            "version": "es2017",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"m05-{i:03d}"
    c["source"] = c["source"].splitlines(keepends=True)

with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(len(cells), "Zellen geschrieben")
