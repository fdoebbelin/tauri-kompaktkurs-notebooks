"""Erzeugt content/M04_JavaScript_im_Fenster.ipynb für die JupyterLite-Seite."""
import json
import pathlib
import sys

HIER = pathlib.Path(__file__).parent
cells = []


def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": text.strip("\n")})


def code(text, hidden=False):
    meta = {"jupyter": {"source_hidden": True}} if hidden else {}
    cells.append({"cell_type": "code", "metadata": meta, "execution_count": None,
                  "outputs": [], "source": text.strip("\n")})


def loesung(titel, inhalt):
    md(f"<details>\n<summary><b>{titel}</b> (zum Aufklappen anklicken)</summary>\n\n{inhalt.strip()}\n\n</details>")


def app(*teile):
    """Eine app.js-Zelle aus mehreren Bausteinen zusammensetzen."""
    code("// app.js\n" + "\n\n".join(t.strip("\n") for t in teile))


# ------------------------------------------------------------------ Dateien
INDEX_HTML = """<!-- index.html -->
<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <title>Lernkarten</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <h1>Lernkarten von Anna</h1>

    <div id="eingabe">
      <h2>Neue Karte</h2>
      <input id="frage-feld" type="text" placeholder="Frage" />
      <textarea id="antwort-feld" placeholder="Antwort"></textarea>
      <button id="knopf-neu">Karte anlegen</button>
    </div>

    <div id="anzeige">
      <p id="karte-frage">Noch keine Karte</p>
      <p id="karte-antwort"></p>
      <div id="knopf-leiste">
        <button id="knopf-umdrehen" class="knopf-anzeige">Umdrehen</button>
        <button id="knopf-weiter" class="knopf-anzeige">Nächste</button>
      </div>
    </div>

    <h2>Alle Karten</h2>
    <ul id="karten-liste"></ul>

    <script src="app.js"></script>
  </body>
</html>"""

STYLE_CSS = """/* style.css */
body {
  background-color: #f4f4f4;
  color: #222222;
  font-family: sans-serif;
}

button {
  background-color: #2a4d69;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  cursor: pointer;
}

button:hover {
  background-color: #3d6b91;
}

.knopf-anzeige {
  background-color: #6b8f71;
}

#eingabe {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 400px;
}

input {
  border: 1px solid #cccccc;
  border-radius: 6px;
  padding: 8px;
  font-size: 16px;
  font-family: sans-serif;
}

textarea {
  border: 1px solid #cccccc;
  border-radius: 6px;
  padding: 8px;
  font-size: 16px;
  font-family: sans-serif;
}

#anzeige {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background-color: #ffffff;
  border: 2px solid #cccccc;
  border-radius: 12px;
  padding: 20px;
  margin-top: 24px;
  max-width: 400px;
}

#karte-frage {
  font-size: 20px;
  font-weight: 700;
}

#knopf-leiste {
  display: flex;
  gap: 12px;
}"""

SETUP = (HIER / "m04_setup.js").read_text(encoding="utf-8")
SETUP = SETUP.replace("__HTML__", json.dumps(INDEX_HTML, ensure_ascii=False))
SETUP = SETUP.replace("__CSS__", json.dumps(STYLE_CSS, ensure_ascii=False))

# ------------------------------------------------------------------ app.js-Bausteine
DATEN = """
const karten = [
  { frage: "Was ist HTML?", antwort: "Die Struktur einer Seite" },
  { frage: "Was ist CSS?", antwort: "Das Aussehen einer Seite" },
  { frage: "Was ist eine id?", antwort: "Der Name eines Elements" }
];

let aktuelleKarte = 0;

function karteAnlegen(frage, antwort) {
  const neueKarte = { frage: frage, antwort: antwort };
  karten.push(neueKarte);
  return neueKarte;
}
"""

LISTE = """
function listeAnzeigen() {
  const liste = document.querySelector("#karten-liste");
  liste.innerHTML = "";

  for (const karte of karten) {
    const eintrag = document.createElement("li");
    eintrag.textContent = karte.frage;
    liste.appendChild(eintrag);
  }
}
"""

NEU = """
// Knopf „Karte anlegen“
const knopfNeu = document.querySelector("#knopf-neu");

knopfNeu.addEventListener("click", function () {
  const frage = document.querySelector("#frage-feld").value;
  const antwort = document.querySelector("#antwort-feld").value;

  if (frage === "" || antwort === "") {
    console.log("Bitte Frage und Antwort ausfüllen");
    return;
  }

  karteAnlegen(frage, antwort);
  listeAnzeigen();

  document.querySelector("#frage-feld").value = "";
  document.querySelector("#antwort-feld").value = "";
});
"""

NEU_OHNE_ANZEIGE = NEU.replace("  karteAnlegen(frage, antwort);\n  listeAnzeigen();\n",
                               "  karteAnlegen(frage, antwort);\n")
assert NEU_OHNE_ANZEIGE != NEU

UMDREHEN = """
// Knopf „Umdrehen“
const knopfUmdrehen = document.querySelector("#knopf-umdrehen");

knopfUmdrehen.addEventListener("click", function () {
  const karte = karten[aktuelleKarte];
  if (!karte) {
    console.log("Noch keine Karte da");
    return;
  }

  const frageElement = document.querySelector("#karte-frage");
  const antwortElement = document.querySelector("#karte-antwort");

  if (frageElement.textContent === karte.frage) {
    antwortElement.textContent = karte.antwort;
  } else {
    frageElement.textContent = karte.frage;
  }
});
"""

WEITER = """
// Knopf „Nächste“
const knopfWeiter = document.querySelector("#knopf-weiter");

knopfWeiter.addEventListener("click", function () {
  if (karten.length === 0) {
    console.log("Noch keine Karte da");
    return;
  }

  aktuelleKarte = (aktuelleKarte + 1) % karten.length;

  document.querySelector("#karte-frage").textContent = karten[aktuelleKarte].frage;
  document.querySelector("#karte-antwort").textContent = "";
});
"""

WEITER_AUFGABE = """
// ★ NEU: Knopf „Nächste“ – Ihre Aufgabe
const knopfWeiter = document.querySelector("#knopf-weiter");

knopfWeiter.addEventListener("click", function () {
  // 1. Gibt es keine Karten? Dann Meldung in die Konsole und mit return aufhören.

  // 2. aktuelleKarte um eins weiterzählen. Nach der letzten Karte wieder bei 0.

  // 3. Die Frage der aktuellen Karte in #karte-frage schreiben.

  // 4. #karte-antwort leeren.

});
"""

START = """
// Die Anzeige zu Beginn
listeAnzeigen();
"""


def neu(baustein):
    """Kennzeichnet einen Baustein als neu hinzugekommen."""
    zeilen = baustein.strip("\n").split("\n")
    if zeilen[0].startswith("// "):
        zeilen[0] = "// ★ NEU: " + zeilen[0][3:]
    else:
        zeilen.insert(0, "// ★ NEU")
    return "\n".join(zeilen)


# ================================================================== Einstieg
md(r"""
# M4 – JavaScript im Fenster

*Begleit-Notebook zu Modul **K4 „JavaScript im Fenster“** im Kompaktkurs „Vom Web zur Desktop-App mit Tauri“*

In M3 hat Ihr Programm nur in der Konsole gesprochen. **Jetzt spricht es das Fenster an.** Die Knöpfe reagieren, die Karten erscheinen, die Lernkarten-App funktioniert. Das ist die Belohnung für die Durststrecke in K3.

> „Sie haben eine Sprache gelernt. Jetzt kommt das letzte Stück: Diese Sprache kann etwas ansprechen. Und das Stück, das gefehlt hat, ist erstaunlich klein.“

| Bisher (K3) | Ab jetzt (K4) |
|---|---|
| `console.log(karten[0].frage)` | der Text steht im Fenster |
| die Konsole zeigt alles | das Fenster zeigt alles |
| das Programm rechnet nur | das Programm verändert, was sichtbar ist |

## 🎯 Das können Sie am Ende

- Elemente der Oberfläche mit `document.querySelector` greifen
- Text in der Oberfläche mit `.textContent` ändern und Eingabefelder mit `.value` lesen und leeren
- mit `addEventListener` auf Klicks reagieren, ohne in die Klammer-Falle zu tappen
- aus dem Datenbestand mit `listeAnzeigen()` die Kartenliste bauen: **erst leeren, dann neu aufbauen**
- die drei Knöpfe „Karte anlegen“, „Umdrehen“ und „Nächste“ funktionsfähig machen
- den fehlenden Aufruf finden: Die Daten sind da, die Anzeige nicht

## 🧭 Inhalt

0. Vorbereitung
1. Ihre Dateien: `index.html` und `style.css`
2. Ein Element greifen
3. Text verändern
4. Anzeige gegen Eingabefeld: `textContent` und `value`
5. Auf Klicks reagieren
6. Aus Daten wird Anzeige
7. Die drei Knöpfe
8. Absichtlicher Fehler: der fehlende Aufruf
9. Fehlerjagd
10. Werkstatt für Schnellere
11. Diagnosetabelle, Checkliste und Ausblick auf K5
""")

md(r"""
## So funktioniert dieses Notebook

Jede Zelle, die mit der Zeile **`// app.js`** beginnt, ist ein vollständiger Stand Ihrer Datei `app.js`. Beim Ausführen (**Umschalt + Enter**) öffnet sich darunter ein **kleines Anwendungsfenster** mit Ihrer Oberfläche, und unter dem Fenster die **Konsole**.

| | Hier im Notebook | In der Lernkarten-App |
|---|---|---|
| Wo steht der Code? | in einer `// app.js`-Zelle | in `src/app.js` |
| Wie wird er ausgeführt? | Umschalt + Enter | speichern, dann Rechtsklick ins Fenster → **Neu laden** |
| Wo ist die Oberfläche? | im Fenster unter der Zelle | im Anwendungsfenster |
| Wo ist die Konsole? | grauer Bereich unter dem Fenster | Rechtsklick → **Element untersuchen** → **Konsole** |

> **📌 Jede Ausführung ist ein Neustart**
> Wenn Sie eine `// app.js`-Zelle erneut ausführen, startet das Fenster von vorn, genau wie beim Neuladen der App. Was Sie vorher eingetippt oder angelegt haben, ist dann weg. Behalten Sie das im Kopf: Genau dieses Problem löst K5.

Die Zeichen kennen Sie aus M3: 🤔 **Vorhersage** · ✏️ **Ihre Aufgabe** · 🐞 **Absichtlicher Fehler** · 💡 **Lösung**. Neu ist 🖱️ **Klicken Sie**: Hier probieren Sie im Fenster selbst aus.

Zeilennummern im Code schalten Sie mit **Esc**, dann **Umschalt + L** ein. Die Konsole nennt bei Fehlern die Zeile in Ihrer `app.js`-Zelle.
""")

# ================================================================== 0
md(r"""
---
## 0 Vorbereitung

Führen Sie die folgende Zelle **als Erstes** aus. Sie ist eingeklappt, weil Sie sie nicht lesen müssen, genau wie den vorbereiteten Rust-Teil Ihrer App. Sie baut das kleine Anwendungsfenster, in dem Ihre `app.js` läuft.

Wenn darunter **🧰 Werkzeugkiste bereit** steht, kann es losgehen.

> Sehen Sie später `ReferenceError: document is not defined`? Dann wurde diese Zelle nicht ausgeführt, zum Beispiel nach einem Neustart des Kernels.
""")

code(SETUP, hidden=True)

# ================================================================== 1
md(r"""
---
## 1 Ihre Dateien: `index.html` und `style.css`

Das sind Ihre beiden Dateien aus K1 und K2. Führen Sie beide Zellen aus. Danach sehen Sie die Oberfläche, noch ohne jede Funktion.
""")

code(INDEX_HTML)
code(STYLE_CSS)

md(r"""
### Ihre `id`-Liste

Jetzt wird die Liste aus K1 zum ersten Mal gebraucht. Sie ist der Grund, warum sie angelegt wurde.

| Nr. | `id` | Element | Wofür |
|---|---|---|---|
| 1 | `eingabe` | `div` | Kiste um den Eingabebereich |
| 2 | `frage-feld` | `input` | Eingabe der Frage |
| 3 | `antwort-feld` | `textarea` | Eingabe der Antwort |
| 4 | `knopf-neu` | `button` | „Karte anlegen“ |
| 5 | `anzeige` | `div` | Kiste um die Karte |
| 6 | `karte-frage` | `p` | zeigt die Frage |
| 7 | `karte-antwort` | `p` | zeigt die Antwort, anfangs leer |
| 8 | `knopf-umdrehen` | `button` | „Umdrehen“ |
| 9 | `knopf-weiter` | `button` | „Nächste“ |
| 10 | `karten-liste` | `ul` | Liste aller Karten, anfangs leer |
| 11 | `knopf-leiste` | `div` | Kiste um die beiden Knöpfe (aus K2) |

### ✏️ Ihre Aufgabe 1

Machen Sie die App zu Ihrer eigenen: Ändern Sie in der `index.html`-Zelle `Lernkarten von Anna` in Ihren Namen und führen Sie die Zelle erneut aus. Wer möchte, ändert in `style.css` auch eine Farbe. Alle Fenster weiter unten verwenden ab dann Ihre Fassung.

### Ihr `app.js` am Ende von K3

So endete K3: ein Datenbestand und eine Funktion. 🤔 **Vorhersage:** Was zeigt das Fenster, was die Konsole?
""")

app(DATEN, 'console.log("Karten im Datenbestand: " + karten.length);')

md(r"""
Im Fenster ändert sich **nichts**, nur die Konsole meldet `3`. Ihr Programm kennt die Karten, aber es spricht das Fenster noch nicht an. Das ändern wir jetzt.
""")

# ================================================================== 2
md(r"""
---
## 2 Ein Element greifen

Um etwas im Fenster zu verändern, muss das Programm das Element erst **finden**. Dafür gibt es genau einen Weg:
""")

app("""
const ueberschrift = document.querySelector("#karte-frage");
console.log(ueberschrift);
console.log(ueberschrift.textContent);
""")

md(r"""
`document.querySelector` bekommt einen **Selektor**: genau dieselbe Schreibweise wie in CSS.

| Gesucht | Selektor |
|---|---|
| Element mit der `id` `karte-frage` | `#karte-frage` |
| Elemente mit der Klasse `knopf-anzeige` | `.knopf-anzeige` |
| Knöpfe | `button` |

> `querySelector` liefert immer **ein** Element, nämlich das **erste**, auf das der Selektor passt. Bei `button` ist das der Knopf „Karte anlegen“.

> **Der Name muss exakt derselbe sein.**
> `#karte-frage` im JavaScript und `id="karte-frage"` im HTML müssen gleich geschrieben sein, Groß- und Kleinschreibung zählt. Deshalb die Kursregel aus K1: alles klein, kein Leerzeichen.

### 🐞 Absichtlicher Fehler: `null`

🤔 **Vorhersage:** Beide Selektoren haben einen Fehler. Was zeigt die Konsole?
""")

app("""
const versuch1 = document.querySelector("karte-frage");
const versuch2 = document.querySelector("#Karte-Frage");
console.log(versuch1);
console.log(versuch2);
console.log(versuch2.textContent);
""")

md(r"""
Zweimal `null`, dann eine rote Meldung: `Cannot read properties of null (reading 'textContent')`, mit Zeile 6.

- `null` heißt: **Ich habe nichts gefunden.** Es ist der Bruder von `undefined` aus M3.
- Beim ersten Versuch fehlt das `#`. Das Programm sucht dann ein Element **namens** `karte-frage`, so wie es `button` oder `p` gibt, und findet keins.
- Beim zweiten stimmt die Groß- und Kleinschreibung nicht.

> **Die Fehlermeldung nennt `null`, nicht die Ursache.** Der Handgriff: Lesen Sie den Selektor aus JavaScript und die `id` aus dem HTML **laut** nebeneinander. Fast immer hört man den Unterschied.

Reparieren Sie beide Zeilen und führen Sie die Zelle erneut aus.

### ✏️ Ihre Aufgabe 2

Greifen Sie **alle Elemente** aus Ihrer `id`-Liste und geben Sie jedes in der Konsole aus. Zwei sind schon da. Fertig sind Sie, wenn in der Konsole kein einziges `null` steht.
""")

app("""
const eingabe = document.querySelector("#eingabe");
console.log(eingabe);

const frageFeld = document.querySelector("#frage-feld");
console.log(frageFeld);

// Ihre weiteren neun Elemente:

""")

loesung("💡 Lösung 2 (Ausschnitt)", r"""
```js
const antwortFeld = document.querySelector("#antwort-feld");
console.log(antwortFeld);

const knopfNeu = document.querySelector("#knopf-neu");
console.log(knopfNeu);

// … und so weiter für anzeige, karte-frage, karte-antwort,
// knopf-leiste, knopf-umdrehen, knopf-weiter, karten-liste
```

Jede Zeile in der Konsole sieht dann aus wie `<button id="knopf-neu">`. Steht irgendwo `null`, vergleichen Sie den Namen laut mit der `id`-Liste.
""")

# ================================================================== 3
md(r"""
---
## 3 Text verändern

Jetzt kommt der Moment, auf den K3 hingearbeitet hat. Führen Sie die Zelle aus und schauen Sie ins Fenster:
""")

app("""
const ueberschrift = document.querySelector("#karte-frage");
ueberschrift.textContent = "Mein Programm schreibt ins Fenster!";
""")

md(r"""
Sofort sichtbar. `.textContent` ist der Text, der in einem Element steht, und mit `=` schreiben Sie einen neuen hinein.

> **`textContent` ersetzt den gesamten Inhalt.** Vorher stand dort „Noch keine Karte“, danach nur noch der neue Text. Es wird nichts angehängt.

### ✏️ Ihre Aufgabe 3

Verändern Sie **drei** Elemente und schauen Sie nach jedem Schritt ins Fenster:

1. die Überschrift `h1` (sie hat keine `id`, der Selektor ist einfach `h1`)
2. `#karte-antwort`, der bisher leere Absatz
3. die Beschriftung des Knopfs `#knopf-neu`
""")

app("""
// 1. Überschrift:


// 2. Antwort:


// 3. Knopf-Beschriftung:

""")

loesung("💡 Lösung 3", r"""
```js
// app.js
const titel = document.querySelector("h1");
titel.textContent = "Meine Lernkarten";

const antwort = document.querySelector("#karte-antwort");
antwort.textContent = "Die Struktur einer Seite";

const knopf = document.querySelector("#knopf-neu");
knopf.textContent = "Neue Karte speichern";
```
""")

# ================================================================== 4
md(r"""
---
## 4 Anzeige gegen Eingabefeld: `textContent` und `value`

Das ist der Unterschied, den Sie sich merken müssen.
""")

app("""
const frageFeld = document.querySelector("#frage-feld");

frageFeld.value = "Was ist JavaScript?";

console.log("value:       [" + frageFeld.value + "]");
console.log("textContent: [" + frageFeld.textContent + "]");
""")

md(r"""
Das Programm hat eine Frage ins Eingabefeld geschrieben. Ausgelesen wird sie mit `.value`, und `.textContent` ist bei einem Eingabefeld leer. Die eckigen Klammern machen das Leere sichtbar.

| | Angezeigte Elemente (`p`, `h1`, `li`, `button`) | Eingabefelder (`input`, `textarea`) |
|---|---|---|
| Was drinsteht | **Text** | **Wert** |
| Lesen | `.textContent` | `.value` |
| Schreiben | `.textContent = "…"` | `.value = "…"` |

> **Anzeigen haben Text, Eingabefelder haben einen Wert.** Das ist keine Eselsbrücke, das sind zwei verschiedene Wörter für zwei verschiedene Dinge.

Und so wird ein Feld **geleert**. Das brauchen Sie später, nachdem eine Karte angelegt wurde:

```js
frageFeld.value = "";
```

### 🤔 Zuordnen: Welche Form passt?

| Element | `.textContent` oder `.value`? |
|---|---|
| der Absatz `#karte-frage` | |
| das Eingabefeld `#frage-feld` | |
| die mehrzeilige Antwort `#antwort-feld` | |
| der Knopf `#knopf-weiter` | |
""")

loesung("💡 Auflösung", r"""
| Element | Richtige Form |
|---|---|
| `#karte-frage` (`p`) | `.textContent` |
| `#frage-feld` (`input`) | `.value` |
| `#antwort-feld` (`textarea`) | `.value`. Auch die `textarea` ist ein Eingabefeld, obwohl sie größer ist. |
| `#knopf-weiter` (`button`) | `.textContent`, die Beschriftung ist angezeigter Text |
""")

# ================================================================== 5
md(r"""
---
## 5 Auf Klicks reagieren

🖱️ Führen Sie die Zelle aus und **klicken Sie dann im Fenster mehrmals auf „Umdrehen“**. Achten Sie auf die Konsole.
""")

app("""
const knopf = document.querySelector("#knopf-umdrehen");

knopf.addEventListener("click", function () {
  console.log("geklickt");
});
""")

md(r"""
`addEventListener` bedeutet: **„Wenn das passiert, tu das.“** Es bekommt zwei Angaben:

1. **was passiert**: `"click"`
2. **was dann passiert**: eine Funktion

> **Neu: eine Funktion ohne Namen.** `function () { … }` ist eine Maschine wie in K3, nur ohne Namen, weil sie nur an genau dieser Stelle gebraucht wird. Sie läuft nicht beim Aufschreiben, sondern **jedes Mal beim Klick**.

> **Erst nur `console.log`, dann die echte Wirkung.** Diesen Zwischenschritt sollten Sie immer gehen. Wenn später etwas nicht klappt, wissen Sie sonst nicht, ob der Klick nicht ankommt oder die Wirkung nicht funktioniert.

### Beim Klick ein Eingabefeld lesen

🖱️ Tippen Sie eine Frage ins Feld und klicken Sie auf **„Karte anlegen“**. Ändern Sie den Text und klicken Sie noch einmal.
""")

app("""
const knopfNeu = document.querySelector("#knopf-neu");

knopfNeu.addEventListener("click", function () {
  const frage = document.querySelector("#frage-feld").value;
  console.log("Im Feld steht: " + frage);
});
""")

md(r"""
🤔 **Vorhersage:** In der nächsten Zelle wird das Feld **vor** dem Klick gelesen, also beim Start. Was erscheint, wenn Sie etwas eintippen und klicken?
""")

app("""
const knopfNeu = document.querySelector("#knopf-neu");
const frage = document.querySelector("#frage-feld").value;

knopfNeu.addEventListener("click", function () {
  console.log("Im Feld steht: [" + frage + "]");
});
""")

loesung("💡 Auflösung", r"""
Immer `[]`, egal was Sie tippen. Das Feld wurde beim Start gelesen, und da war es leer. Was Sie danach tippen, bekommt das Programm nie zu sehen.

**Regel:** Eingabefelder werden **im** Klick gelesen, also innerhalb der Funktion. Erst dann steht drin, was die Person eingetippt hat.
""")

md(r"""
### 🐞 Absichtlicher Fehler: die Klammern

🖱️ Führen Sie die Zelle aus. Schauen Sie **sofort** in die Konsole, **bevor** Sie klicken. Klicken Sie dann mehrmals auf „Umdrehen“.
""")

app("""
function meldung() {
  console.log("geklickt");
}

const knopf = document.querySelector("#knopf-umdrehen");
knopf.addEventListener("click", meldung());
""")

md(r"""
„geklickt“ steht schon **vor** dem ersten Klick in der Konsole, genau einmal. Danach passiert beim Klicken nichts mehr, und es gibt **keine Fehlermeldung**.

```js
knopf.addEventListener("click", meldung());   // falsch: läuft sofort, einmal
knopf.addEventListener("click", meldung);     // richtig: läuft bei jedem Klick
```

> ## Merksatz: Der Name einer Funktion, ohne Klammern, ist die Sache selbst. Mit Klammern ist es ein Aufruf.

Reparieren Sie die Zelle: Klammern hinter `meldung` weg, erneut ausführen, klicken.
""")

# ================================================================== 6
md(r"""
---
## 6 Aus Daten wird Anzeige

Das ist die zentrale Funktion des Kurses: Sie macht aus dem Datenbestand eine Liste im Fenster.
""")

app(DATEN, LISTE, START)

md(r"""
Zeile für Zeile:

| Zeile | Was sie tut |
|---|---|
| `const liste = document.querySelector("#karten-liste");` | die leere Liste aus dem HTML holen |
| `liste.innerHTML = "";` | alles Vorhandene entfernen |
| `for (const karte of karten)` | jede Karte durchgehen |
| `document.createElement("li")` | einen **neuen** Listeneintrag bauen |
| `eintrag.textContent = karte.frage;` | seinen Inhalt setzen |
| `liste.appendChild(eintrag);` | ihn an die Liste hängen |

> **Warum steht im HTML nur `<ul id="karten-liste"></ul>`?** Das ist ein leerer Rahmen. Der Inhalt entsteht erst, wenn das Programm läuft. Deshalb war die Liste in Abschnitt 1 unsichtbar, und das war so geplant.

### 🐞 Warum erst leeren?

🤔 **Vorhersage:** Hier ist die Leerzeile auskommentiert, und `listeAnzeigen()` wird zweimal aufgerufen, so wie es passiert, wenn zwei Karten nacheinander angelegt werden. Wie viele Einträge zeigt das Fenster?
""")

app(DATEN, LISTE.replace('  liste.innerHTML = "";', '  // liste.innerHTML = "";'),
    "listeAnzeigen();\nlisteAnzeigen();")

md(r"""
**Sechs** Einträge, jede Karte doppelt. Ohne das Leeren hängt jeder Aufruf alles noch einmal an. Entfernen Sie die `//` vor `liste.innerHTML = "";` und führen Sie die Zelle erneut aus.

> ## Merksatz: Erst leeren, dann aus den Daten neu aufbauen.
> Dann kann `listeAnzeigen()` so oft aufgerufen werden, wie Sie wollen, und zeigt immer genau, was in `karten` steht.

### ✏️ Ihre Aufgabe 6

Ändern Sie `listeAnzeigen()` so, dass jeder Eintrag **Frage und Antwort** zeigt, zum Beispiel `Was ist HTML? → Die Struktur einer Seite`. Erinnern Sie sich an `karteAlsText` aus M3?
""")

app(DATEN, LISTE, START)

loesung("💡 Lösung 6", r"""
Nur eine Zeile ändert sich:

```js
eintrag.textContent = karte.frage + " → " + karte.antwort;
```

Für die weiteren Abschnitte bleibt es bei der Frage allein. So steht es auch im Leitfaden.
""")

# ================================================================== 7
md(r"""
---
## 7 Die drei Knöpfe

Jetzt wird die Oberfläche funktionsfähig. Jede Zelle in diesem Abschnitt ist Ihr **ganzes** `app.js`. Was neu dazukommt, ist mit **★ NEU** markiert.

Im Code tauchen vier kleine Zeichen auf, die Sie aus K3 noch nicht kennen:

| Zeichen | Bedeutung | Beispiel |
|---|---|---|
| `\|\|` | **oder** | `frage === "" \|\| antwort === ""`: Frage leer **oder** Antwort leer |
| `!` | **nicht** | `!karte`: es gibt **keine** Karte |
| `return;` | **hier aufhören**, ohne etwas abzuliefern | nach einer Meldung abbrechen |
| `%` | **Rest beim Teilen** („modulo“) | `4 % 3` ergibt `1` |

### 7a Knopf „Karte anlegen“
""")

app(DATEN, LISTE, neu(NEU), START)

md(r"""
🖱️ Legen Sie zwei eigene Karten an. Klicken Sie dann einmal auf „Karte anlegen“, ohne etwas einzutippen, und schauen Sie in die Konsole.

Der Ablauf, **in genau dieser Reihenfolge**:

1. **Werte holen**: aus beiden Eingabefeldern, mit `.value`
2. **Prüfen**: Ist etwas leer? Dann Meldung und abbrechen.
3. **Anlegen**: `karteAnlegen(frage, antwort)` hängt die Karte an die Liste `karten`
4. **Anzeigen**: `listeAnzeigen()` baut die Liste im Fenster neu auf
5. **Leeren**: beide Felder zurücksetzen

> **Schritt 3 und 4 dürfen nicht vertauscht werden.** Wird erst angezeigt und dann angelegt, sieht man die neue Karte erst beim nächsten Klick. Wird nur angelegt und nicht angezeigt, passiert im Fenster gar nichts. Das ist der häufigste Fehler dieses Moduls, Sie treffen ihn in Abschnitt 8 wieder.

### 7b Knopf „Umdrehen“
""")

app(DATEN, LISTE, NEU, neu(UMDREHEN), START)

md(r"""
🖱️ Klicken Sie zweimal auf **„Umdrehen“**: Beim ersten Mal erscheint die Frage der aktuellen Karte, beim zweiten Mal die Antwort darunter.

Hier wird zum ersten Mal ein Text **gelesen und geschrieben**: `frageElement.textContent` steht im `if` auf der rechten Seite des Vergleichs, und `antwortElement.textContent` links vom `=`.

> 🤔 Lesen Sie das `if` laut: „Wenn oben schon die Frage der aktuellen Karte steht, dann zeige die Antwort. Sonst zeige erst einmal die Frage.“

### 7c ✏️ Ihre Aufgabe: Knopf „Nächste“

Ergänzen Sie den Knopf **„Nächste“**. Er soll zur nächsten Karte blättern und nach der letzten wieder bei der ersten anfangen. Die vier Schritte stehen als Kommentare im Code.

**Tipps:**
- `aktuelleKarte` ist ein `let`. Genau für diesen Fall wurde es in K3 so angelegt.
- Für Schritt 2 haben Sie in M3 die Funktion `naechsteNummer` geschrieben. Es geht auch kürzer mit `%`: `(aktuelleKarte + 1) % karten.length`
""")

app(DATEN, LISTE, NEU, UMDREHEN, WEITER_AUFGABE, START)

md(r"""
🖱️ **So testen Sie:** „Nächste“, dann „Umdrehen“, „Umdrehen“, wieder „Nächste“. Nach der dritten Karte muss wieder „Was ist HTML?“ kommen. Legen Sie eine vierte Karte an und blättern Sie bis zu ihr.
""")

loesung("💡 Lösung 7c", r"""
```js
knopfWeiter.addEventListener("click", function () {
  if (karten.length === 0) {
    console.log("Noch keine Karte da");
    return;
  }

  aktuelleKarte = (aktuelleKarte + 1) % karten.length;

  document.querySelector("#karte-frage").textContent = karten[aktuelleKarte].frage;
  document.querySelector("#karte-antwort").textContent = "";
});
```

`%` ist der Rest beim Teilen: Bei 3 Karten wird aus `2 + 1 = 3` der Rest `3 % 3 = 0`, also wieder die erste Karte.

Ihre Lösung aus M3 ist genauso richtig:

```js
if (aktuelleKarte === karten.length - 1) {
  aktuelleKarte = 0;
} else {
  aktuelleKarte = aktuelleKarte + 1;
}
```
""")

md(r"""
### 7d So sieht `app.js` am Ende von K4 aus

Die vollständige Datei. 🖱️ Probieren Sie alles durch: anlegen, blättern, umdrehen.
""")

app(DATEN, LISTE, NEU, UMDREHEN, WEITER, START)

md(r"""
🤔 **Und jetzt:** Legen Sie eine eigene Karte an und führen Sie die Zelle dann **erneut** aus. Wo ist Ihre Karte?

Sie ist weg. Jeder Neustart beginnt wieder mit den drei Karten aus dem Programmtext, in der echten App genauso. **Genau das löst K5:** Dort werden die Karten in einer Datei gespeichert und überleben den Neustart.
""")

# ================================================================== 8
md(r"""
---
## 8 🐞 Absichtlicher Fehler: der fehlende Aufruf

In dieser Fassung fehlt **eine einzige Zeile**. 🖱️ Legen Sie eine neue Karte an.
""")

app(DATEN, LISTE, NEU_OHNE_ANZEIGE, UMDREHEN, WEITER, START)

md(r"""
Die Felder werden geleert, aber die Liste wächst nicht. **Keine Fehlermeldung.** Wurde die Karte überhaupt angelegt?

**Der Diagnoseweg:**

1. **Sind die Daten da?** Fügen Sie im Knopf „Karte anlegen“ direkt unter `karteAnlegen(frage, antwort);` diese Zeile ein und führen Sie die Zelle erneut aus:
   ```js
   console.log("Karten im Datenbestand: " + karten.length);
   ```
   Legen Sie wieder eine Karte an. Steigt die Zahl? Dann sind die Daten da.
2. **Was fehlt jetzt noch?** Die Daten sind da, die Anzeige nicht. Welche Funktion baut die Anzeige?
3. **Reparieren** und testen.

> „Das Programm macht beides richtig, aber es macht nicht beides. Das eine ohne das andere ist nichts.“
""")

loesung("💡 Lösung", r"""
Es fehlt der Aufruf von `listeAnzeigen();` direkt nach `karteAnlegen(frage, antwort);`:

```js
karteAnlegen(frage, antwort);
listeAnzeigen();
```

**Merken Sie sich die Frage für jede Änderung an den Daten:** *Habe ich danach die Anzeige neu aufgebaut?*
""")

# ================================================================== 9
md(r"""
---
## 9 Fehlerjagd

In jeder Zelle steckt **genau ein** Fehler. Führen Sie sie aus, beschreiben Sie, was Sie sehen, und reparieren Sie sie. Darüber steht jeweils, was passieren **soll**.

**a)** Beim Start soll die Antwort „Die Struktur einer Seite“ im Fenster stehen.
""")

app("""
const antwort = document.querySelector("karte-antwort");
antwort.textContent = "Die Struktur einer Seite";
""")

md(r"""
**b)** 🖱️ Beim Klick auf „Karte anlegen“ soll die eingetippte Frage in der Konsole erscheinen.
""")

app("""
const knopfNeu = document.querySelector("#knopf-neu");

knopfNeu.addEventListener("click", function () {
  const frage = document.querySelector("#frage-feld").textContent;
  console.log("Neue Frage: " + frage);
});
""")

md(r"""
**c)** 🖱️ Die Antwort soll erst erscheinen, wenn auf „Umdrehen“ geklickt wird.
""")

app("""
function antwortZeigen() {
  document.querySelector("#karte-antwort").textContent = "Die Struktur einer Seite";
}

const knopf = document.querySelector("#knopf-umdrehen");
knopf.addEventListener("click", antwortZeigen());
""")

md(r"""
**d)** 🖱️ Legen Sie zwei Karten nacheinander an. Jede Karte soll genau **einmal** in der Liste stehen.
""")

app(DATEN, LISTE.replace('  liste.innerHTML = "";\n', ""), NEU, START)

md(r"""
**e)** 🖱️ Eine neu angelegte Karte soll **sofort** in der Liste erscheinen, nicht erst beim nächsten Klick.
""")

app(DATEN, LISTE,
    NEU.replace("  karteAnlegen(frage, antwort);\n  listeAnzeigen();\n",
                "  listeAnzeigen();\n  karteAnlegen(frage, antwort);\n"),
    START)

loesung("💡 Lösungen zur Fehlerjagd", r"""
| | Was Sie sehen | Ursache | Reparatur |
|---|---|---|---|
| a) | rote Meldung mit `null` | `#` fehlt im Selektor | `"#karte-antwort"` |
| b) | `Neue Frage: ` ohne Text | `.textContent` bei einem Eingabefeld | `.value` |
| c) | Antwort steht schon beim Start, Klick tut nichts | Klammern beim `addEventListener` | `antwortZeigen` ohne `()` |
| d) | Einträge stehen doppelt und dreifach | `liste.innerHTML = "";` fehlt | Zeile wieder einfügen |
| e) | neue Karte erscheint erst beim nächsten Anlegen | erst angezeigt, dann angelegt | `karteAnlegen` vor `listeAnzeigen` |

Nur a) erzeugt eine Fehlermeldung. Bei allen anderen läuft das Programm und tut etwas anderes als gedacht. Deshalb lohnt sich der Zwischenschritt über `console.log`.
""")

# ================================================================== 10
md(r"""
---
## 10 Werkstatt für Schnellere

Hier kommt kein neuer Stoff, nur Verbesserungen mit dem, was Sie schon können. Arbeiten Sie in der Zelle unten. Sie enthält das vollständige `app.js`.

1. **Meldung im Fenster:** Statt `console.log("Bitte Frage und Antwort ausfüllen")` soll der Hinweis in `#karte-antwort` erscheinen, damit ihn auch jemand ohne Konsole sieht.
2. **Nur Leerzeichen abfangen:** Wer nur Leerzeichen eintippt, legt im Moment eine „leere“ Karte an. Nutzen Sie `.trim()` aus M3.
3. **Gleich etwas zeigen:** Beim Start soll statt „Noch keine Karte“ sofort die Frage der ersten Karte dastehen.
4. **Frage und Antwort in der Liste** wie in Aufgabe 6.
""")

app(DATEN, LISTE, NEU, UMDREHEN, WEITER, START)

loesung("💡 Lösungsideen", r"""
**1. Meldung im Fenster**, im Knopf „Karte anlegen“:

```js
if (frage === "" || antwort === "") {
  document.querySelector("#karte-antwort").textContent = "Bitte Frage und Antwort ausfüllen";
  return;
}
```

**2. Leerzeichen abfangen**: beim Holen gleich säubern:

```js
const frage = document.querySelector("#frage-feld").value.trim();
const antwort = document.querySelector("#antwort-feld").value.trim();
```

**3. Gleich etwas zeigen**, ganz unten bei der Anzeige zu Beginn:

```js
listeAnzeigen();
document.querySelector("#karte-frage").textContent = karten[aktuelleKarte].frage;
```

**4.** siehe Lösung 6.
""")

# ================================================================== 11
md(r"""
---
## 11 Diagnosetabelle, Checkliste und Ausblick

### Die Diagnosetabelle, erweitert um K4

| Was zu sehen ist | Was das meistens heißt |
|---|---|
| rote Meldung mit **`null`** | Element nicht gefunden: `#` vergessen oder `id` falsch geschrieben. Laut vorlesen! |
| Daten sind da (Konsole), Fenster zeigt nichts | Anzeigefunktion nicht aufgerufen |
| Einträge stehen doppelt | `liste.innerHTML = "";` vergessen |
| Eingabe kommt leer an | `.textContent` statt `.value`, oder das Feld wurde vor dem Klick gelesen |
| Wirkung schon beim Start, Klick tut nichts | Klammern bei `addEventListener("click", name())` |
| neue Karte erscheint erst beim nächsten Klick | erst angezeigt, dann angelegt |
| gar nichts, keine Meldung | Funktion nie aufgerufen (aus K3) |
| `undefined` | da war nichts, wo etwas sein sollte (aus K3) |

### ✅ Checkliste

Haken Sie ab (Doppelklick auf diese Zelle, dann `[ ]` zu `[x]` ändern):

- [ ] Ich habe alle Elemente meiner `id`-Liste im Programm gegriffen und in der Konsole ausgegeben
- [ ] Ich kann `.textContent` und `.value` unterscheiden und weiß, wofür welches da ist
- [ ] Ich habe auf einen Klick reagiert und kenne die Klammer-Falle
- [ ] Ich kann `listeAnzeigen()` Zeile für Zeile erklären: erst leeren, dann neu aufbauen
- [ ] Der Knopf „Karte anlegen“ liest, prüft, legt an, zeigt an und leert
- [ ] Die Knöpfe „Umdrehen“ und „Nächste“ funktionieren
- [ ] Ich habe den fehlenden Aufruf von `listeAnzeigen()` gesucht und repariert

### Wie geht es weiter?

Ihre App funktioniert, aber sie hat kein Gedächtnis: Jeder Neustart beginnt wieder mit den drei Karten aus dem Programmtext. In **K5 „Daten behalten“** speichert die App die Karten in einer Datei, und sie überleben den Neustart. Dafür ruft Ihr JavaScript den vorbereiteten Rust-Teil der App auf.

**Zum Nachschlagen:** K4 Merkblatt · K4 Übungsblatt · Anhang Sprachumfang JavaScript
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
    c["id"] = f"m04-{i:03d}"
    c["source"] = c["source"].splitlines(keepends=True)

with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(len(cells), "Zellen geschrieben")
