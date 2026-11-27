"""Erzeugt content/M06_Feinschliff.ipynb für die JupyterLite-Seite."""
import json
import pathlib
import sys

HIER = pathlib.Path(__file__).parent

# Helfer, Dateien und Bausteine aus K4 und K5 übernehmen
_m05 = (HIER / "gen_m05.py").read_text(encoding="utf-8")
exec(_m05.split("\n# ================================================================== Einstieg\n")[0])

K5_TEILE = [DATEN_LEER, LISTE, SPEICHERN, LADEN, NEU_K5, UMDREHEN, WEITER, START_LADEN]
STANDARD_JS = "// app.js\n" + "\n\n".join(t.strip("\n") for t in K5_TEILE)

SETUP = (HIER / "m06_setup.js").read_text(encoding="utf-8")
SETUP = SETUP.replace("__HTML__", json.dumps(INDEX_HTML, ensure_ascii=False))
SETUP = SETUP.replace("__CSS__", json.dumps(STYLE_CSS, ensure_ascii=False))
SETUP = SETUP.replace("__JS__", json.dumps(STANDARD_JS, ensure_ascii=False))

# ------------------------------------------------------------------ Löschknopf
LISTE_LOESCHEN = """
function listeAnzeigen() {
  const liste = document.querySelector("#karten-liste");
  liste.innerHTML = "";

  for (const karte of karten) {
    const eintrag = document.createElement("li");
    eintrag.textContent = karte.frage;

    const loeschKnopf = document.createElement("button");
    loeschKnopf.textContent = "Löschen";
    loeschKnopf.addEventListener("click", async function () {
      const pos = karten.indexOf(karte);
      if (pos >= 0) {
        karten.splice(pos, 1);
        listeAnzeigen();
        await speichern();
      }
    });

    eintrag.appendChild(loeschKnopf);
    liste.appendChild(eintrag);
  }
}
"""
LISTE_LOESCHEN_LEITFADEN = LISTE_LOESCHEN.replace('"click", async function () {', '"click", function () {')
LISTE_LOESCHEN_OHNE_SPEICHERN = LISTE_LOESCHEN.replace("        listeAnzeigen();\n        await speichern();\n",
                                                       "        listeAnzeigen();\n")
assert LISTE_LOESCHEN_LEITFADEN != LISTE_LOESCHEN and LISTE_LOESCHEN_OHNE_SPEICHERN != LISTE_LOESCHEN


def k5_mit(ersatz=None, **_):
    """K5-Endstand, einzelne Bausteine ersetzt: ersatz = {alter_baustein: neuer_baustein}."""
    ersatz = ersatz or {}
    return [ersatz.get(t, t) for t in K5_TEILE]


# ================================================================== Einstieg
md(r"""
# M6 – Feinschliff

*Begleit-Notebook zu Modul **K6 „Feinschliff“** im Kompaktkurs „Vom Web zur Desktop-App mit Tauri“*

Ihre Lernkarten-App kann inzwischen alles Nötige: Karten anlegen, anzeigen, durchblättern, speichern, laden. Aber sie sieht aus wie eine App, die jemand anderes gebaut hat. In diesem Modul machen Sie sie zu **Ihrer eigenen**.

**Kein neuer Stoff.** Sie wenden an, was Sie aus K2 bis K5 kennen. Zwei Aufgaben:

1. **Gestalten**: dem Ganzen einen eigenen Look geben
2. **Verbessern**: eine Sache auswählen, die Ihnen auffällt, und sie umsetzen

> ## Die eine Regel: Eine Verbesserung, nicht fünf.
> Wer fünf Sachen auf einmal angeht, hat am Ende fünf halbe Sachen und eine kaputte Datei. Der Satz, der bremst: *„Wenn das fertig ist, habe ich **eine** Verbesserung.“*

## 🎯 Das können Sie am Ende

- ein eigenes Farbschema mit drei passenden Farben umsetzen und den Kontrast prüfen
- **genau eine** Verbesserung formulieren, umsetzen und prüfen, mit Bausteinen aus den bisherigen Modulen
- nach jeder Änderung an den Daten an zwei Dinge denken: `listeAnzeigen()` und `await speichern()`
- Ihre Entscheidung vor der Gruppe begründen

## 🧭 Inhalt

0. Vorbereitung
1. Ihr Stand von K5, und erst einmal sichern
2. Eigene Gestaltung
3. Eine eigene Verbesserung
4. Beispiel: der Löschknopf
5. Prüfen: Ist der Rest heil geblieben?
6. Vorstellen
7. Diagnosetabelle, Checkliste und Ausblick auf K7
""")

md(r"""
## So funktioniert dieses Notebook

Alles aus M5 gilt weiter: Jede `// app.js`-Zelle öffnet ein Fenster mit Konsole, **⟳ Neu starten** und **📄 lernkarten.json**. Ihre Karten aus M5 sind noch da, denn es ist dieselbe Datei.

Neu für die Gestaltung:

| Neu | Wozu |
|---|---|
| **Vorschau** | Eine `index.html`- oder `style.css`-Zelle zeigt sofort die **ganze App** mit der zuletzt ausgeführten `app.js`, mit Ihren Karten. |
| **Hinweise** | Benutzt Ihre `style.css` etwas, das nicht auf der Kursliste steht, sagt die Vorschau Bescheid. |
| **`kontrast(farbe1, farbe2)`** | prüft, ob Text auf einem Hintergrund gut lesbar ist |

Die Zeichen kennen Sie: 🤔 **Vorhersage** · ✏️ **Ihre Aufgabe** · 🐞 **Absichtlicher Fehler** · 🖱️ **Klicken Sie** · 💡 **Lösung**.
""")

# ================================================================== 0
md(r"""
---
## 0 Vorbereitung

Führen Sie die eingeklappte Zelle **als Erstes** aus. Wenn darunter **🧰 Werkzeugkiste bereit** steht, kann es losgehen.
""")

code(SETUP, hidden=True)

# ================================================================== 1
md(r"""
---
## 1 Ihr Stand von K5, und erst einmal sichern

Das ist Ihr `app.js` vom Ende von K5. Die Karten kommen aus `lernkarten.json`.
""")

app(*K5_TEILE)

md(r"""
> **Ist die Liste leer?** Dann gibt es in diesem Browser noch keine Datei. Legen Sie drei, vier Karten an. Sie werden gespeichert und stehen in allen Fenstern weiter unten zur Verfügung. Zum Gestalten ist es angenehmer, wenn etwas zu sehen ist.

### Vor dem Umbauen: eine Kopie

Legen Sie **vor der ersten Änderung** eine Kopie an. Nicht aus Misstrauen, sondern weil der Stand von K5 sonst nicht wiederherstellbar ist.

- **In der echten App**, im Projektordner `~/Projekte/lernkarten`:
  ```nu
  cp -r src src-stand-k5
  ```
- **Hier im Notebook:** Rechtsklick auf dieses Notebook im Dateibrowser links → **Duplicate**.
""")

# ================================================================== 2
md(r"""
---
## 2 Eigene Gestaltung

Freie Arbeit an `style.css`. Die Vorgabe ist bewusst knapp:

- Die Anwendung muss **bedienbar** bleiben.
- Die **drei Farben** müssen zueinander passen: Hintergrund, Karte, Knöpfe.
- Der Text muss aus **zwei Metern** Entfernung lesbar sein.

Das sind Ihre drei Dateien. Hier wird gestaltet: Ändern Sie die `style.css`-Zelle, führen Sie sie aus, und die Vorschau darunter zeigt Ihre App. **Nach jeder Änderung hinsehen**, nicht erst am Ende.
""")

code(INDEX_HTML)
code(STYLE_CSS)

md(r"""
### Anregungen

Wählen Sie **eine oder zwei**, nicht alle:

| Anregung | Womit |
|---|---|
| eigenes Farbschema | `background-color`, `color`, `border` |
| andere Schriftgröße für Frage und Antwort | `font-size` |
| Karte hervorheben, etwa mit Rahmen und Schatten | `border`, `border-radius`, `box-shadow` |
| den wichtigsten Knopf auffälliger machen | `font-weight`, `padding`, `#id` statt `.klasse` |
| Abstand zwischen Frage und Antwort | `margin`, `gap` |
| die ganze App auf eine Breite begrenzen | `max-width` |

> **Was hier nicht kommt:** keine neuen CSS-Eigenschaften, kein Grid, kein `position: absolute`. Alles Nötige steht im K2-Merkblatt.
> Probiert jemand trotzdem etwas Neues aus, gilt der Satz: *„Das steht nicht auf unserer Liste. Wenn es klappt, behalten wir es, wenn nicht, zurück zur Liste.“* Die Vorschau sagt ihn Ihnen auch.

<details>
<summary><b>📋 Die Kursliste für CSS</b> (zum Aufklappen anklicken)</summary>

**Selektoren:** `element`, `.klasse`, `#id`, `element:hover`

**Eigenschaften:** `color`, `background-color`, `font-family`, `font-size`, `font-weight`, `padding`, `margin`, `border`, `border-radius`, `box-shadow`, `width`, `max-width`, `display: flex`, `flex-direction`, `gap`, `justify-content`, `align-items`, `cursor`

**Farben** ausschließlich als Hex-Wert, zum Beispiel `#2a4d69`.

</details>

### Der Kontrast-Check

*„Können Sie das aus zwei Metern Entfernung lesen?“* Hinsehen ist der wichtigste Test. Die Funktion `kontrast` hilft dabei: Sie bekommt **Textfarbe** und **Hintergrundfarbe** und sagt, wie gut man das lesen kann.

🤔 **Vorhersage:** Welche der drei Kombinationen aus der bisherigen `style.css` ist am schwächsten?
""")

code(r"""
kontrast("#222222", "#f4f4f4");   // Schrift auf dem Seitenhintergrund
kontrast("#ffffff", "#2a4d69");   // weiße Schrift auf dem Knopf „Karte anlegen“
kontrast("#ffffff", "#6b8f71");   // weiße Schrift auf „Umdrehen“ und „Nächste“
""")

md(r"""
Die grünen Knöpfe kommen nur auf etwa **3,6 : 1**. Ab **4,5 : 1** gilt normaler Text als gut lesbar, ab **7 : 1** als sehr gut. Ein etwas dunkleres Grün wie `#4a7350` schafft es.

Das ist eine kleine Lektion in **Barrierefreiheit**: Nicht alle Menschen sehen gleich gut, und nicht jeder Bildschirm ist gleich hell.

### ✏️ Ihre Aufgabe 2

1. Wählen Sie **drei Farben**: Seitenhintergrund, Karte, Knöpfe. Dazu passende Schriftfarben.
2. Prüfen Sie jede Kombination aus Schrift und Hintergrund mit `kontrast` in der Zelle unten.
3. Tragen Sie die Farben in die `style.css`-Zelle oben ein und schauen Sie die Vorschau an.
4. Setzen Sie eine oder zwei Anregungen aus der Tabelle um.
""")

code(r"""
// Ihre Farben prüfen: erst die Schrift, dann der Hintergrund
kontrast("#222222", "#f4f4f4");

""")

loesung("💡 Ein Beispiel-Farbschema: „Sand und Rost“", r"""
Nur ein Beispiel. Ihr Schema darf ganz anders aussehen, gerade das ist der Punkt dieses Moduls.

| Rolle | Farbe | Kontrast |
|---|---|---|
| Seitenhintergrund / Schrift | `#fdf6e3` / `#3b2f2f` | 11,9 : 1 |
| Karte / Schrift | `#ffffff` / `#3b2f2f` | 12,9 : 1 |
| Knopf „Karte anlegen“ / Schrift | `#9c3d10` / `#ffffff` | 6,8 : 1 |
| Knöpfe auf der Karte / Schrift | `#2f6f6a` / `#ffffff` | 5,8 : 1 |

Die geänderten Regeln in `style.css`:

```css
body {
  background-color: #fdf6e3;
  color: #3b2f2f;
  font-family: sans-serif;
}

button {
  background-color: #9c3d10;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  cursor: pointer;
}

button:hover {
  background-color: #7a2f0c;
}

.knopf-anzeige {
  background-color: #2f6f6a;
}

#anzeige {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background-color: #ffffff;
  border: 2px solid #e8dcc0;
  border-radius: 12px;
  box-shadow: 0 4px 12px #d9ccae;
  padding: 20px;
  margin-top: 24px;
  max-width: 400px;
}

#karte-frage {
  font-size: 24px;
  font-weight: 700;
}

#knopf-neu {
  font-weight: 700;
  padding: 12px 16px;
}
```
""")

md(r"""
### 🤔 Was kommt in diesem Modul **nicht** vor?

| Werkzeug | kommt vor? |
|---|---|
| CSS Grid | |
| `position: absolute` | |
| Pfeilfunktionen `=>` | |
| `class` und `this` | |
| `border-radius` | |
| `box-shadow` | |
""")

loesung("💡 Auflösung", r"""
| Werkzeug | kommt vor? |
|---|---|
| CSS Grid | ✘ ein Layoutsystem genügt |
| `position: absolute` | ✘ erzeugt mehr Probleme, als es löst |
| Pfeilfunktionen `=>` | ✘ zweite Schreibweise für Funktionen |
| `class` und `this` | ✘ Objektorientierung ist ein eigener Kurs |
| `border-radius` | ✔ aus K2 |
| `box-shadow` | ✔ aus K2 |
""")

# ================================================================== 3
md(r"""
---
## 3 Eine eigene Verbesserung

Wählen Sie **genau eine** Verbesserung aus und setzen Sie sie selbst um. Jede kommt mit Bausteinen aus, die Sie schon kennen:

| Wunsch | Werkzeug | Modul |
|---|---|---|
| **A** Anzahl der Karten anzeigen | `karten.length`, `.textContent` | K3, K4 |
| **B** Leere Eingabe abfangen | `if`, `.value`, `.trim()` | K3, K4 |
| **C** Antwort wieder verbergen | `if`, `.textContent` | K3, K4 |
| **D** Zählen, wie viele Karten schon gezeigt wurden | Zähler-Variable (`let`), `if` | K3 |
| **E** Löschknopf pro Listeneintrag | `createElement`, `addEventListener`, `indexOf`, `splice` | K4, Abschnitt 4 |

### Die vier Schritte

1. **Formulieren:** Was genau soll passieren? Ein Satz mit **„wenn … dann“**.
2. **Nachschlagen:** Welche Bausteine aus der Tabelle werden gebraucht?
3. **Umsetzen:** klein anfangen, nach jeder Änderung hinsehen.
4. **Prüfen:** Stimmt das Ergebnis? Bleibt der Rest heil? (Abschnitt 5)

> **Nach jeder Änderung an den Daten** gibt es zwei Fragen:
>
> | Was passiert | Dann aufrufen |
> |---|---|
> | Die Liste der Karten hat sich geändert | `listeAnzeigen()` |
> | Die Karten sollen auf der Platte bleiben | `await speichern()` |

### ✏️ Schritt 1: Formulieren

Doppelklicken Sie auf diese Zelle und ergänzen Sie:

> **Meine Verbesserung:** Wenn … , dann … .
>
> **Bausteine:** …
""")

md(r"""
### Die Werkstattkarten

Lesen Sie **nur die Karte** Ihrer Verbesserung. Die Lösung ist zugeklappt: erst selbst versuchen.

---

**A · Anzahl der Karten anzeigen**
*Wenn sich die Liste ändert, dann steht über ihr, wie viele Karten es gibt.*

- Sie brauchen ein Element dafür. Ergänzen Sie in der `index.html`-Zelle (Abschnitt 2) unter `<h2>Alle Karten</h2>` einen Absatz mit eigener `id` und führen Sie die Zelle aus.
- Die richtige Stelle zum Schreiben ist dort, wo die Liste sowieso neu aufgebaut wird.
""")

loesung("💡 Lösung A", r"""
In `index.html`:

```html
<h2>Alle Karten</h2>
<p id="karten-anzahl"></p>
<ul id="karten-liste"></ul>
```

In `app.js`, als letzte Zeile **innerhalb** von `listeAnzeigen()`:

```js
document.querySelector("#karten-anzahl").textContent = karten.length + " Karten";
```

Da `listeAnzeigen()` nach dem Laden, Anlegen und Löschen aufgerufen wird, stimmt die Zahl immer.

Sehen Sie `Cannot set properties of null`? Dann wurde die `index.html`-Zelle nicht ausgeführt, oder die `id` ist anders geschrieben. Laut vorlesen!
""")

md(r"""
**B · Leere Eingabe abfangen**
*Wenn jemand nur Leerzeichen eintippt, dann wird keine Karte angelegt, und im Fenster steht ein Hinweis.*

- Im Moment wird nur `""` abgefangen. Probieren Sie es aus: drei Leerzeichen in beide Felder, „Karte anlegen“.
- `.trim()` aus K3 entfernt die Leerzeichen am Rand.
""")

loesung("💡 Lösung B", r"""
Im Knopf „Karte anlegen“ beim Holen gleich säubern, und den Hinweis ins Fenster schreiben statt in die Konsole:

```js
const frage = document.querySelector("#frage-feld").value.trim();
const antwort = document.querySelector("#antwort-feld").value.trim();

if (frage === "" || antwort === "") {
  document.querySelector("#karte-antwort").textContent = "Bitte Frage und Antwort ausfüllen";
  return;
}
```
""")

md(r"""
**C · Antwort wieder verbergen**
*Wenn die Antwort zu sehen ist und ich auf „Umdrehen“ klicke, dann verschwindet sie wieder.*

- Im Moment bleibt die Antwort stehen, egal wie oft Sie klicken.
- Sie brauchen ein zweites `if` im Knopf „Umdrehen“: Steht in `#karte-antwort` schon etwas?
""")

loesung("💡 Lösung C", r"""
Im Knopf „Umdrehen“ den Teil mit dem `if` so erweitern:

```js
if (frageElement.textContent === karte.frage) {
  if (antwortElement.textContent === "") {
    antwortElement.textContent = karte.antwort;
  } else {
    antwortElement.textContent = "";
  }
} else {
  frageElement.textContent = karte.frage;
}
```

Ein `if` in einem `if` ist erlaubt. Lesen Sie es laut: „Steht die Frage da? Dann: Ist die Antwort leer? Dann zeigen, sonst verbergen.“
""")

md(r"""
**D · Zählen, wie viele Karten schon gezeigt wurden**
*Wenn ich auf „Nächste“ klicke, dann zählt die App mit. Wenn ich einmal durch alle Karten bin, dann meldet sie das.*

- Eine Zähler-Variable, die sich ändert: `const` oder `let`?
- Sie gehört nach oben zu `aktuelleKarte`, nicht in die Klickfunktion. Warum?
""")

loesung("💡 Lösung D", r"""
Oben, unter `let aktuelleKarte = 0;`:

```js
let gezeigt = 0;
```

Im Knopf „Nächste“, nach dem Weiterzählen von `aktuelleKarte`:

```js
gezeigt = gezeigt + 1;
console.log("Schon gezeigt: " + gezeigt);
if (gezeigt === karten.length) {
  console.log("Einmal durch alle Karten!");
}
```

Stünde `let gezeigt = 0;` **in** der Klickfunktion, finge der Zähler bei jedem Klick wieder bei null an.

Wer die Zahl lieber im Fenster sieht, legt wie bei A einen Absatz mit eigener `id` an.
""")

md(r"""
**E · Löschknopf:** siehe Abschnitt 4. Dort ist er Schritt für Schritt vorgeführt.

---

### ✏️ Ihre Werkbank

Bauen Sie Ihre **eine** Verbesserung hier ein. Die Zelle enthält Ihr `app.js` vom Ende von K5. Wenn sie fertig ist, führen Sie die `style.css`-Zelle aus Abschnitt 2 noch einmal aus: Die Vorschau zeigt dann Gestaltung **und** Verbesserung zusammen.
""")

app(*K5_TEILE)

# ================================================================== 4
md(r"""
---
## 4 Beispiel: der Löschknopf

An diesem Beispiel sieht man, was „**eine** Verbesserung“ bedeutet und wie viel dahintersteckt. Jeder Eintrag in der Liste bekommt einen eigenen Knopf. Er wird in `listeAnzeigen()` gebaut, genau wie der Eintrag selbst.

### Zwei Rezepte, genau einmal

`indexOf` und `splice` stehen nicht in der allgemeinen Kursliste, sondern unter **„bedingt erlaubt“**. Wer diese Verbesserung wählt, bekommt sie hier als Rezept, als vollständige Zeile:

| Rezept | Was es tut |
|---|---|
| `const pos = karten.indexOf(karte);` | die **Stelle** dieser Karte in der Liste finden (`-1`, wenn sie nicht drin ist) |
| `karten.splice(pos, 1);` | an dieser Stelle **eine** Karte entfernen |

`>=` heißt „größer oder gleich“: `pos >= 0` bedeutet „die Karte wurde gefunden“.

### 🐞 Die Fassung aus dem Leitfaden

🤔 Diese Fassung steht so im Leitfaden. Führen Sie sie aus. Was meldet die Konsole, und warum? Denken Sie an den Merksatz aus K5.
""")

app(*k5_mit({LISTE: LISTE_LOESCHEN_LEITFADEN}))

md(r"""
`SyntaxError: await is only valid in async functions …`. Im Klick steht `await speichern();`, aber die Klickfunktion ist kein `async`. Das ganze Fenster läuft deshalb nicht, auch die Karten erscheinen nicht.

> **Wo `await` steht, muss `async` davorstehen.** Auch in einer Funktion ohne Namen.

### Die reparierte Fassung

🖱️ Löschen Sie eine Karte. Schauen Sie auf 📄 und klicken Sie dann **⟳ Neu starten**: Die Karte bleibt weg.
""")

app(*k5_mit({LISTE: neu(LISTE_LOESCHEN)}))

md(r"""
Drei Bausteine stecken darin, alle aus den bisherigen Modulen:

| Baustein | Woher |
|---|---|
| `document.createElement("button")`, `addEventListener` | K4 |
| `karten.indexOf(karte)` und `karten.splice(pos, 1)` | Liste aus K3, als Rezept |
| `await speichern();` | K5 |

> **„Der Löschknopf verschwindet beim Klick!“** Das ist richtig so. Nach dem Löschen baut `listeAnzeigen()` die Liste neu auf, und dabei wird jeder Knopf neu erzeugt. Erst leeren, dann neu aufbauen, wie in K4.

### 🐞 Löschen ohne Speichern

🖱️ In dieser Fassung fehlt eine Zeile. Löschen Sie eine Karte, schauen Sie auf 📄, und klicken Sie **⟳ Neu starten**.
""")

app(*k5_mit({LISTE: LISTE_LOESCHEN_OHNE_SPEICHERN}))

md(r"""
Die Karte ist nach dem Neustart **wieder da**. Gelöscht wurde nur im Arbeitsspeicher, die Datei hat davon nie erfahren. Das war die Warnung aus K5: *Speichern an nur einer Stelle reicht nicht.*

> **Löschknopf klebt am Text?** Ein Abstand mit Mitteln aus der Kursliste, in `style.css`:
> ```css
> li {
>   display: flex;
>   gap: 12px;
>   align-items: center;
>   margin-bottom: 6px;
> }
> ```

> **Zweite Verbesserung im Kopf?** „Und dann noch eine Rückfrage, bevor gelöscht wird …“ Das ist eine **zweite** Verbesserung. Erst die eine fertig machen.
""")

# ================================================================== 5
md(r"""
---
## 5 Prüfen: Ist der Rest heil geblieben?

Eine Verbesserung ist erst fertig, wenn **alles andere noch funktioniert**. Gehen Sie in Ihrer Werkbank-Zelle (Abschnitt 3) diese Liste durch:

- [ ] Die Karten aus der Datei erscheinen beim Start.
- [ ] Eine neue Karte anlegen: Sie erscheint sofort in der Liste, die Felder werden geleert.
- [ ] Leere Eingabe: Es wird keine Karte angelegt.
- [ ] „Umdrehen“ zeigt Frage, dann Antwort.
- [ ] „Nächste“ blättert und fängt nach der letzten Karte wieder vorn an.
- [ ] **⟳ Neu starten**: Alle Änderungen an den Karten sind noch da.
- [ ] Die Konsole zeigt keine rote Meldung.
- [ ] Ihre Verbesserung tut, was Ihr „wenn … dann“-Satz sagt.

Fällt etwas durch, schauen Sie in die Diagnosetabelle in Abschnitt 7.
""")

# ================================================================== 6
md(r"""
---
## 6 Vorstellen

Jede Person zeigt der Gruppe ihre App und erklärt **eine** getroffene Entscheidung. Die Frage ist immer dieselbe:

> **„Warum genau diese Entscheidung? Was wäre schlechter geworden, wenn Sie es anders gemacht hätten?“**

Eine Begründung ist wertvoller als fünf nachgemachte Regeln. Gesucht wird nicht die beste Lösung, sondern **Ihre**.

Beim Vorstellen gleich mitprüfen: Ist der Text aus **zwei Metern** Entfernung lesbar?

### ✏️ Ihre Notizen fürs Vorstellen

Doppelklicken Sie auf diese Zelle und ergänzen Sie:

> **Meine Farben:** … (Kontrast: …)
>
> **Meine Verbesserung:** Wenn … , dann … .
>
> **Warum gerade diese?** …
>
> **Was wäre schlechter, wenn ich es anders gemacht hätte?** …
""")

# ================================================================== 7
md(r"""
---
## 7 Diagnosetabelle, Checkliste und Ausblick

### Typische Stolperstellen in K6

| Was zu sehen ist | Was das meistens heißt |
|---|---|
| Viele halbe Sachen, nichts funktioniert richtig | zu viel auf einmal: zurück auf **eine** Verbesserung |
| Etwas, das vorher ging, geht nicht mehr | beim Umbauen beschädigt: mit der Kopie von K5 vergleichen |
| Text schlecht lesbar | Kontrast zu gering: `kontrast(schrift, hintergrund)` |
| Änderung an den Daten, aber die Liste zeigt das Alte | `listeAnzeigen()` fehlt |
| Änderung ist nach dem Neustart weg | `await speichern()` fehlt |
| `SyntaxError: await is only valid in async functions` | `async` fehlt vor der Funktion, auch vor `function () {` im Klick |
| `Cannot set properties of null` | das Element gibt es nicht: `id` im HTML ergänzt und die Zelle ausgeführt? |
| Löschknopf verschwindet beim Klick | richtig so: die Liste wird neu aufgebaut |

### ✅ Checkliste

Haken Sie ab (Doppelklick auf diese Zelle, dann `[ ]` zu `[x]` ändern):

- [ ] Ein eigenes Farbschema umgesetzt, die drei Farben passen zueinander
- [ ] Den Kontrast geprüft, mit `kontrast` und aus zwei Metern
- [ ] **Genau eine** Verbesserung ausgewählt, umgesetzt und begründet
- [ ] Den Rest der App geprüft: Er ist heil geblieben
- [ ] Die App der Gruppe vorgestellt
- [ ] Den Stand gesichert, bevor K7 beginnt

### Wie geht es weiter?

In **K7 „Als Anwendung ausliefern“** wird aus Ihrem Projekt eine richtige Anwendung: ein Flatpak, das mit eigenem Eintrag im Anwendungsmenü erscheint. Was Sie dort ausliefern, ist genau das, was Sie hier gestaltet und verbessert haben. Übertragen Sie deshalb Ihre `style.css` und Ihr `app.js` aus diesem Notebook in Ihr Projekt.

**Zum Nachschlagen:** K6 Merkblatt · K6 Übungsblatt · Anhang Sprachumfang JavaScript
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
    c["id"] = f"m06-{i:03d}"
    c["source"] = c["source"].splitlines(keepends=True)

with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(len(cells), "Zellen geschrieben")
