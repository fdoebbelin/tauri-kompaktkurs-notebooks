"""Erzeugt content/M02_CSS_das_Aussehen.ipynb für die JupyterLite-Seite."""
import json
import pathlib
import sys

HIER = pathlib.Path(__file__).parent
_m04 = (HIER / "gen_m04.py").read_text(encoding="utf-8")
exec(_m04.split("\n# ================================================================== Einstieg\n")[0])

INDEX_K2 = INDEX_HTML
LEISTE_HTML = """      <div id="knopf-leiste">
        <button id="knopf-umdrehen" class="knopf-anzeige">Umdrehen</button>
        <button id="knopf-weiter" class="knopf-anzeige">Nächste</button>
      </div>
"""
INDEX_K1 = INDEX_K2.replace(LEISTE_HTML, """      <button id="knopf-umdrehen" class="knopf-anzeige">Umdrehen</button>
      <button id="knopf-weiter" class="knopf-anzeige">Nächste</button>
""")
assert INDEX_K1 != INDEX_K2

SETUP = (HIER / "m02_setup.js").read_text(encoding="utf-8")
SETUP = SETUP.replace("__HTML__", json.dumps(INDEX_K1, ensure_ascii=False))


def css(*regeln, neu=()):
    """Eine vollständige style.css aus Regeln; Regeln in `neu` werden markiert."""
    teile = []
    for r in regeln:
        r = r.strip("\n")
        teile.append(("/* ★ NEU */\n" + r) if r in [n.strip("\n") for n in neu] else r)
    code("/* style.css */\n" + "\n\n".join(teile))


# ------------------------------------------------------------------ Regeln
BODY1 = """body {
  background-color: #f4f4f4;
}"""
BODY = """body {
  background-color: #f4f4f4;
  color: #222222;
}"""
BUTTON = """button {
  background-color: #2a4d69;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}"""
BUTTON_P = BUTTON.replace("  cursor: pointer;\n}", "  cursor: pointer;\n  padding: 8px 16px;\n}")
KA = """.knopf-anzeige {
  background-color: #6b8f71;
}"""
ANZ0 = """#anzeige {
  background-color: #ffffff;
}"""
KF = """#karte-frage {
  font-size: 20px;
  font-weight: 700;
}"""
HOVER = """button:hover {
  background-color: #3d6b91;
}"""
ANZ1 = ANZ0.replace("}", "  border: 2px solid #cccccc;\n}")
ANZ2 = ANZ1.replace("}", "  padding: 20px;\n}")
ANZ3 = ANZ2.replace("}", "  margin: 24px;\n}")
ANZ4 = ANZ3.replace("}", "  border-radius: 12px;\n}")
ANZ5 = ANZ4.replace("}", "  max-width: 400px;\n}")
ANZ_WIDTH = ANZ4.replace("}", "  width: 400px;\n}")
EINGABE = """#eingabe {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 400px;
}"""
ANZ_ROW = ANZ5.replace("}", "  display: flex;\n  flex-direction: row;\n}")
ANZ_COL = ANZ5.replace("}", "  display: flex;\n  flex-direction: column;\n  gap: 12px;\n}")
LEISTE = """#knopf-leiste {
  display: flex;
  gap: 12px;
}"""
LEISTE_AUS = """#knopf-leiste {
  display: flex;
  gap: 12px;
  justify-content: center;
  align-items: center;
}"""
FELDER = """input {
  border: 1px solid #cccccc;
  border-radius: 6px;
  padding: 8px;
  font-size: 16px;
}

textarea {
  border: 1px solid #cccccc;
  border-radius: 6px;
  padding: 8px;
  font-size: 16px;
}"""

ENDE = [BODY, BUTTON_P, KA, HOVER, ANZ_COL, KF, EINGABE, LEISTE]

# ================================================================== Einstieg
md(r"""
# M2 – CSS: das Aussehen

*Begleit-Notebook zu Modul **K2 „CSS – das Aussehen“** im Kompaktkurs „Vom Web zur Desktop-App mit Tauri“*

In K1 haben Sie die **Struktur** Ihrer Lernkarten-App gebaut: alle Elemente, jedes mit einem Namen. Sie sieht aber noch aus wie ein Formular von 1995. Jetzt kommt das **Aussehen**. Das ist der optische Sprung des Kurses: Aus einer Sammlung von Feldern wird zum ersten Mal etwas, das man jemandem zeigen möchte.

## 🎯 Das können Sie am Ende

- eine CSS-Regel lesen und schreiben: **Wen betrifft es? Was soll anders sein? Wie soll es sein?**
- Farben als Hex-Wert lesen und selbst mischen
- Elemente auf drei Wegen treffen: **Typ**, **Klasse**, **`id`**, und wissen, welche Regel gewinnt
- das **Boxmodell** anwenden: `padding` und `margin` unterscheiden
- mit **Flexbox** Dinge unter- und nebeneinander anordnen
- die beiden typischen Fehler finden: fehlendes **Semikolon**, fehlende **Klammer**

## 🧭 Inhalt

0. Vorbereitung
1. Wie das Aussehen zur Struktur kommt
2. Der Aufbau einer CSS-Regel
3. Farben als Hex-Wert
4. Drei Wege, ein Element zu treffen
5. Wenn zwei Regeln dasselbe Element treffen
6. Das Boxmodell
7. Flexbox: Dinge anordnen
8. Die eigene Gestaltung
9. Absichtlicher Fehler: Semikolon und Klammer
10. Diagnosefragen, Checkliste und Ausblick auf K3
""")

md(r"""
## So funktioniert dieses Notebook

Jede Zelle, die mit **`/* style.css */`** beginnt, ist ein vollständiger Stand Ihrer Datei `style.css`. Beim Ausführen (**Umschalt + Enter**) zeigt ein kleines Fenster darunter Ihre Oberfläche. Eine Zelle mit **`<!-- index.html -->`** am Anfang ändert die Struktur.

> Im Kurs liegen `index.html` und `style.css` nebeneinander offen. Hier im Notebook steht die Vorschau direkt unter dem CSS, so sehen Sie Ursache und Wirkung auf einen Blick.

Im Fenster gibt es drei Hilfen:

| Hilfe | Wozu |
|---|---|
| **↔ Fensterbreite** | das Fenster schmaler ziehen, wie mit der Maus am Fensterrand |
| **▣ Kisten zeigen** | zeigt den Rand jeder Kiste als gestrichelte Linie, ideal für das Boxmodell |
| **🔎 So hat der Browser Ihre style.css verstanden** | zum Aufklappen. Zeigt jede Regel, die angekommen ist, und wie viele Elemente sie trifft. Nützlich, wenn etwas nicht wirkt. |

Dazu zwei Funktionen für normale Zellen: `farbe("#2a4d69")` zerlegt einen Hex-Wert, `kontrast("#222222", "#f4f4f4")` prüft die Lesbarkeit.

Die Zeichen: 🤔 **Vorhersage** · ✏️ **Ihre Aufgabe** · 🐞 **Absichtlicher Fehler** · 🖱️ **Ausprobieren** · 💡 **Lösung**.

> **Nach jeder Änderung hinsehen.** Das ist die wichtigste Regel dieses Moduls.
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
## 1 Wie das Aussehen zur Struktur kommt

Das ist Ihre `index.html` vom Ende von K1. Führen Sie die Zelle aus: So sieht die App **ohne** CSS aus, in der Werkseinstellung des Browsers.
""")

code(INDEX_K1)

md(r"""
Im Kopf der Datei steht seit K1 diese Zeile:

```html
<link rel="stylesheet" href="style.css" />
```

Sie sagt: Zu dieser Datei gehört ein **Anstrich**, und der steht in `style.css`. Solange die Datei leer ist, sieht alles nach Werkseinstellung aus. Das ändert sich jetzt.

> **CSS Grid kommt nicht vor.** Es gibt ein zweites Anordnungssystem mit Zeilen und Spalten. Für diese Oberfläche wird es nicht gebraucht.

Halten Sie Ihre **`id`-Liste aus K1** bereit. Ab Abschnitt 4 brauchen Sie sie.
""")

# ================================================================== 2
md(r"""
---
## 2 Der Aufbau einer CSS-Regel

```
body { background-color: #f4f4f4; }
 │      │                  │      │
 │      │                  │      └─ Semikolon: beendet die Erklärung
 │      │                  └──────── Wert: wie soll es sein
 │      └─────────────────────────── Eigenschaft: was soll anders sein
 └────────────────────────────────── Selektor: wen betrifft es
```

Drei Fragen, jedes Mal dieselben: **Wen betrifft es? Was soll anders sein? Wie soll es sein?**

Ihre erste Regel. Führen Sie die Zelle aus und **schauen Sie hin**.
""")

css(BODY1)

md(r"""
Der ganze Hintergrund ist hellgrau. Eine Zeile, und die ganze Seite ist anders.

Geschrieben wird über mehrere Zeilen: oben der Selektor mit der öffnenden Klammer, darunter eingerückt die Erklärungen, unten die schließende Klammer. Eine zweite Erklärung für die Schriftfarbe:
""")

css(BODY, neu=[BODY])

md(r"""
> **Das Semikolon ist Pflicht.** Fehlt es, versteht der Browser die betroffene **und** die nächste Erklärung nicht mehr. Das ist der häufigste Fehler dieses Moduls. In Abschnitt 9 bauen Sie ihn absichtlich ein.

### 🤔 Zerlegen Sie die Regel

```css
#karte-frage {
  font-size: 20px;
}
```

1. Selektor? 2. Welcher Selektortyp? 3. Eigenschaft? 4. Wert? 5. Wie viele Elemente trifft sie?
""")

loesung("💡 Antwort", r"""
1. Selektor: `#karte-frage`
2. ein `id`-Selektor, erkennbar an der Raute `#`
3. Eigenschaft: `font-size`
4. Wert: `20px`
5. genau **eines**, denn eine `id` darf nur einmal vergeben werden
""")

# ================================================================== 3
md(r"""
---
## 3 Farben als Hex-Wert

```
#f4f4f4
 └┬┘└┬┘└┬┘
  │  │  └─ Blau
  │  └──── Grün
  └─────── Rot
```

Jede Stelle läuft von `00` (nichts davon) bis `ff` (voll). Die Funktion `farbe` zerlegt einen Hex-Wert für Sie:
""")

code(r"""
farbe("#ffffff", "#000000", "#888888", "#f4f4f4");
""")

md(r"""
`#ffffff` ist Weiß (alles voll), `#000000` Schwarz (nichts), `#888888` ein mittleres Grau. Sind alle drei Anteile gleich, ist es immer ein Grau.

### 🤔 Vorhersage

Welche Farben sind das? Erst überlegen, dann ausführen.

| Hex-Wert | Ihre Vorhersage |
|---|---|
| `#ff0000` | |
| `#00ff00` | |
| `#ffff00` | |
| `#2a4d69` | |
""")

code(r"""
farbe("#ff0000", "#00ff00", "#ffff00", "#2a4d69");
""")

md(r"""
Rot, Grün, Gelb (Rot und Grün zusammen ergeben bei Licht Gelb) und ein dunkles Blau: wenig Rot, etwas Grün, etwas mehr Blau, alles eher niedrig, also dunkel.

### Eine brauchbare Startpalette
""")

code(r"""
// Seite, Karte, Text, Nebentext, Rahmen, Hauptfarbe, Hauptfarbe hell, Zweitfarbe
farbe("#f4f4f4", "#ffffff", "#222222", "#555555", "#cccccc", "#2a4d69", "#3d6b91", "#6b8f71");
""")

md(r"""
| Zweck | Vorschlag |
|---|---|
| Seitenhintergrund | `#f4f4f4` |
| Kartenhintergrund | `#ffffff` |
| Text | `#222222` |
| Nebentext | `#555555` |
| Rahmen | `#cccccc` |
| Hauptfarbe | `#2a4d69` |
| Hauptfarbe hell, für `:hover` | `#3d6b91` |
| Zweitfarbe | `#6b8f71` |

> **Kursregel Farben:** ausschließlich Hex-Werte, keine Farbnamen wie `red`. *„Es gibt beides, aber wenn drei Leute mischen, sieht die Datei aus wie ein Flohmarkt.“* Die Vorschau erinnert Sie daran, wenn sich ein Farbname einschleicht.

Eigene Farben sind erlaubt und erwünscht. Einzige Bedingung: Text auf seinem Hintergrund muss **aus zwei Metern** lesbar bleiben. `kontrast` hilft beim Prüfen:
""")

code(r"""
kontrast("#222222", "#f4f4f4");   // Text auf dem Seitenhintergrund
kontrast("#cccccc", "#ffffff");   // hellgrauer Text auf Weiß
""")

md(r"""
### ✏️ Ihre Aufgabe 3

Mischen Sie **Ihre eigene Hauptfarbe**: Ändern Sie die Ziffern und Buchstaben (`0`–`9`, `a`–`f`), bis sie Ihnen gefällt. Prüfen Sie dann, ob weiße Schrift darauf gut lesbar ist.
""")

code(r"""
farbe("#2a4d69");
kontrast("#ffffff", "#2a4d69");
""")

# ================================================================== 4
md(r"""
---
## 4 Drei Wege, ein Element zu treffen

| Selektor | Schreibweise | Trifft | Typischer Einsatz |
|---|---|---|---|
| **Typ** | `button` | alle Elemente dieser Sorte | Grundaussehen aller Knöpfe |
| **Klasse** | `.knopf-anzeige` | eine Gruppe | mehrere Elemente sollen gleich aussehen |
| **`id`** | `#karte-frage` | genau ein Element | ein bestimmtes Element, sonst nichts |

### Der Typselektor: alle auf einmal

🖱️ Führen Sie die Zelle aus und fahren Sie mit der Maus über einen Knopf.
""")

css(BODY, BUTTON, neu=[BUTTON])

md(r"""
Alle drei Knöpfe ändern sich gleichzeitig. `button` ohne Raute, ohne Punkt heißt: **alle Knöpfe**, die es gibt und die es je geben wird.

`cursor: pointer` macht den Mauszeiger zur Hand. Ohne das wirkt ein Knopf wie ein Bild. Die billigste Verbesserung, die es gibt.

### Der Klassenselektor: eine Gruppe

In der `index.html` tragen die beiden Blätterknöpfe ein zweites Namensschild:

```html
<button id="knopf-umdrehen" class="knopf-anzeige">Umdrehen</button>
<button id="knopf-weiter" class="knopf-anzeige">Nächste</button>
```

Sie gehören zusammen. Der wichtige Knopf ist der andere, der Karten anlegt. Also bekommen die beiden eine eigene Farbe, aber nicht jeder einzeln:
""")

css(BODY, BUTTON, KA, neu=[KA])

md(r"""
> **Der Zeichenwechsel**
> Im HTML steht `class="knopf-anzeige"` **ohne** Punkt und `id="karte-frage"` **ohne** Raute.
> Im CSS steht `.knopf-anzeige` **mit** Punkt und `#karte-frage` **mit** Raute.
> Das ist verwirrend und lässt sich nicht wegerklären. Es ist einfach so.

### Der `id`-Selektor: genau eines

Schlagen Sie Ihre `id`-Liste auf. Jeder Name darin ist eine **Adresse**, an die Sie etwas schicken können. Deshalb haben Sie sie angelegt.
""")

css(BODY, BUTTON, KA, ANZ0, KF, neu=[ANZ0, KF])

md(r"""
Der Anzeigebereich ist jetzt weiß, die Frage groß und fett. `font-weight: 700` heißt fett, `400` normal.

### 🐞 Absichtlicher Fehler: nichts passiert

In dieser Fassung stecken drei Fehler, alle in den letzten drei Regeln. 🤔 Was wird sich im Fenster ändern?
""")

css(BODY, BUTTON, """.anzeige {
  background-color: #ffffff;
}""", """#knopf-anzeige {
  background-color: #6b8f71;
}""", """#Karte-Frage {
  font-size: 20px;
  font-weight: 700;
}""")

md(r"""
**Nichts.** Und es gibt **keine Fehlermeldung**. Der Browser findet einfach kein Element, das passt.

> **Die Diagnoseregel:** Wenn nichts passiert, lesen Sie den Namen im CSS und den Namen im HTML **laut** nebeneinander vor. Nicht ansehen, vorlesen. Fast immer hört man es.

Klappen Sie unter dem Fenster **🔎 So hat der Browser Ihre style.css verstanden** auf: Alle drei Regeln sind angekommen, jede Zeile hat ein ✅, aber jede Regel **trifft kein einziges Element**.
""")

loesung("💡 Die drei Fehler", r"""
| Im CSS | Richtig | Was falsch war |
|---|---|---|
| `.anzeige` | `#anzeige` | Punkt statt Raute: `anzeige` ist eine `id`, keine Klasse |
| `#knopf-anzeige` | `.knopf-anzeige` | Raute statt Punkt: `knopf-anzeige` ist eine Klasse |
| `#Karte-Frage` | `#karte-frage` | Groß- statt Kleinschreibung. Deshalb die Kursregel aus K1: alles klein. |
""")

md(r"""
### ✏️ Ihre Aufgabe 4

Greifen Sie ein Element **aus Ihrer `id`-Liste** heraus, das noch keine Regel hat, und geben Sie ihm eine Eigenschaft, zum Beispiel `#karte-antwort` eine andere Farbe oder `#eingabe` einen Hintergrund. Ergänzen Sie die Regel unten in der Zelle.
""")

css(BODY, BUTTON, KA, ANZ0, KF, "/* Ihre Regel: */\n")

md(r"""
### 🤔 Welchen Selektor würden Sie schreiben?

| Vorhaben | Selektor |
|---|---|
| Alle Absätze bekommen dieselbe Schriftgröße | |
| Nur die Frage der aktuellen Karte wird fett | |
| Die beiden Blätterknöpfe werden grün | |
| Alle Eingabefelder bekommen einen Rahmen | |
| Der Kartenbereich bekommt runde Ecken | |
""")

loesung("💡 Auflösung", r"""
| Vorhaben | Selektor |
|---|---|
| alle Absätze | `p` |
| nur die Frage | `#karte-frage` |
| die beiden Blätterknöpfe | `.knopf-anzeige` |
| alle Eingabefelder | `input`, und für die Antwort zusätzlich `textarea` |
| der Kartenbereich | `#anzeige` |

**Warum drei Wege?** Einer würde reichen, aber dann müssten Sie jedes Element einzeln beschreiben. Mit den drei Wegen sagen Sie **einmal**, wie Knöpfe grundsätzlich aussehen, und danach nur noch die **Abweichungen**. Das ist der ganze Trick.
""")

# ================================================================== 5
md(r"""
---
## 5 Wenn zwei Regeln dasselbe Element treffen

Schauen Sie noch einmal auf die Knöpfe „Umdrehen“ und „Nächste“: Für sie gelten **zwei** Regeln, `button` sagt Blau, `.knopf-anzeige` sagt Grün. Sie sind grün. Warum gewinnt Grün?

```
Je genauer der Selektor, desto stärker.
#id   schlägt   .klasse   schlägt   element
```

`button` meint alle, `.knopf-anzeige` meint zwei bestimmte, ist also genauer und setzt sich durch.

### 🤔 Vorhersage

Hier gibt es zusätzlich eine `id`-Regel für den Knopf „Nächste“, und zwei gleich genaue Regeln für `body`. Welche Farbe hat „Nächste“? Und welche der Hintergrund?
""")

css("""body {
  background-color: #f4f4f4;
  color: #222222;
}""", BUTTON, KA, ANZ0, KF, """#knopf-weiter {
  background-color: #8a4b12;
}""", """body {
  background-color: #e8eef3;
}""")

loesung("💡 Auflösung", r"""
- **„Nächste“ ist braun** (`#8a4b12`). Drei Regeln treffen ihn: `button`, `.knopf-anzeige` und `#knopf-weiter`. Die `id` ist am genauesten und gewinnt. „Umdrehen“ bleibt grün.
- **Der Hintergrund ist hellblau** (`#e8eef3`). Beide `body`-Regeln sind gleich genau. Dann gewinnt die, die **weiter unten** in der Datei steht.

Die Schriftfarbe aus der ersten `body`-Regel gilt trotzdem weiter, denn die zweite sagt dazu nichts. Es wird nur das überschrieben, worüber beide etwas sagen.
""")

md(r"""
### Ein Zustand: `:hover`

🖱️ Fahren Sie mit der Maus über die Knöpfe.
""")

css(BODY, BUTTON, KA, ANZ0, KF, HOVER, neu=[HOVER])

md(r"""
Der Doppelpunkt heißt: **nur in diesem Zustand**, also nur, solange die Maus darauf steht. Eine Oberfläche, die auf die Maus reagiert, fühlt sich lebendig an.
""")

# ================================================================== 6
md(r"""
---
## 6 Das Boxmodell

Jedes Element ist eine Kiste aus vier Schichten:

```
┌─────────────────────────────────┐
│  margin  (außen, unsichtbar)    │
│  ┌───────────────────────────┐  │
│  │  border                   │  │
│  │  ┌─────────────────────┐  │  │
│  │  │  padding            │  │  │
│  │  │  ┌───────────────┐  │  │  │
│  │  │  │    Inhalt     │  │  │  │
│  │  │  └───────────────┘  │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

> ## Merksatz
> **`padding` schiebt den Inhalt vom Rahmen weg.**
> **`margin` schiebt den Rahmen von den Nachbarn weg.**

Bildvergleich: Ein gerahmtes Bild an der Wand. Das Passepartout zwischen Bild und Rahmen ist `padding`, der Rahmen ist `border`, der Abstand zum Nachbarbild ist `margin`.

Jetzt in fünf Schritten am Anzeigebereich. **Nach jedem Schritt hinsehen.** Schalten Sie ruhig **▣ Kisten zeigen** ein.

**Schritt 1: nur der Rahmen**
""")

css(BODY, BUTTON, KA, HOVER, ANZ1, KF, neu=[ANZ1])

md(r"""
Drei Angaben in einer Zeile: **wie dick, welche Art, welche Farbe**. Immer in dieser Reihenfolge. `solid` heißt durchgezogen.

**Schritt 2: Innenabstand**
""")

css(BODY, BUTTON, KA, HOVER, ANZ2, KF, neu=[ANZ2])

md(r"""
Der Text rückt vom Rahmen weg. Der Rahmen bleibt, wo er ist, der Inhalt rutscht nach innen. Deshalb wird die Kiste größer.

**Schritt 3: Außenabstand**
""")

css(BODY, BUTTON, KA, HOVER, ANZ3, KF, neu=[ANZ3])

md(r"""
Jetzt rückt die **ganze Kiste** weg, von der Überschrift darüber und vom Rand. Innen ändert sich nichts.

**Schritt 4: runde Ecken**
""")

css(BODY, BUTTON, KA, HOVER, ANZ4, KF, neu=[ANZ4])

md(r"""
**Schritt 5: Breite begrenzen**

🖱️ Ziehen Sie danach mit **↔ Fensterbreite** das Fenster schmaler und wieder breiter.
""")

css(BODY, BUTTON, KA, HOVER, ANZ5, KF, neu=[ANZ5])

md(r"""
`max-width` heißt: **höchstens** so breit. Ist das Fenster schmaler, wird die Kiste mit schmaler.

### 🐞 Und mit `width`?

🖱️ Hier steht `width` statt `max-width`. Ziehen Sie das Fenster wieder schmal.
""")

css(BODY, BUTTON, KA, HOVER, ANZ_WIDTH, KF)

md(r"""
Die Kiste bleibt stur 400 Pixel breit und **läuft aus dem Fenster**. Deshalb im Kurs immer `max-width`.

### Die Zahl davor

Eine Zahl bedeutet: alle vier Seiten gleich. Zwei Zahlen: die erste für **oben und unten**, die zweite für **links und rechts**. Mehr Formen kommen nicht vor.
""")

css(BODY, BUTTON_P, KA, HOVER, ANZ5, KF, neu=[BUTTON_P])

md(r"""
Die Knöpfe bekommen oben und unten 8, links und rechts 16 Pixel Luft.

> **Der klassische Verwechslungsfall:** „Ich wollte mehr Luft **im** Kasten und habe `margin` genommen. Jetzt ist der Kasten weiter weg, aber innen genauso eng.“ Die Prüffrage: **Soll sich der Rahmen bewegen oder der Inhalt?** Inhalt: `padding`. Rahmen: `margin`.

### ✏️ Ihre Aufgabe 6

Spielen Sie das Boxmodell an einem **selbst gewählten Element** aus Ihrer `id`-Liste durch, zum Beispiel `#eingabe`: erst Rahmen, dann Innenabstand, dann Außenabstand. **Nach jedem Schritt ausführen und hinsehen.**
""")

css(BODY, BUTTON_P, KA, HOVER, ANZ5, KF, "/* Ihr Element: */\n")

md(r"""
### 🤔 `padding` oder `margin`?

| Vorhaben | `padding` oder `margin`? |
|---|---|
| Der Text soll nicht am Rahmen kleben | |
| Zwischen Karte und Überschrift soll Luft sein | |
| Die Beschriftung im Knopf soll seitlich mehr Platz haben | |
| Die beiden Bereiche sollen weiter auseinander liegen | |
| Der Kasten soll insgesamt größer wirken, ohne mehr Text | |
""")

loesung("💡 Auflösung", r"""
| Vorhaben | Antwort |
|---|---|
| Text klebt am Rahmen | `padding` |
| Luft zwischen Karte und Überschrift | `margin` |
| Beschriftung im Knopf | `padding` |
| Bereiche weiter auseinander | `margin` |
| Kasten größer ohne mehr Text | `padding` |
""")

# ================================================================== 7
md(r"""
---
## 7 Flexbox: Dinge anordnen

Ziel ist genau ein Anwendungsfall: Dinge **untereinander** oder **nebeneinander** anordnen.

### Untereinander mit Abstand

Schauen Sie sich vorher den Eingabebereich an: Feld, Feld, Knopf kleben aneinander und sind unterschiedlich breit.
""")

css(BODY, BUTTON_P, KA, HOVER, ANZ5, KF, EINGABE, neu=[EINGABE])

md(r"""
| Zeile | Bedeutung |
|---|---|
| `display: flex` | „Ich kümmere mich um die Anordnung meiner Kinder.“ |
| `flex-direction: column` | untereinander. `row` heißt nebeneinander und ist die Voreinstellung. |
| `gap: 12px` | Abstand **zwischen** den Kindern, einmal gesetzt, gilt überall |

> **Warum `gap` besser ist als `margin`:** Mit `margin` müssten Sie jedem Element einzeln einen Abstand geben und beim letzten wieder wegnehmen. `gap` erledigt das in einer Zeile.

### Nebeneinander, und warum eine eigene Kiste nötig ist

Die beiden Knöpfe „Umdrehen“ und „Nächste“ sollen nebeneinander stehen. 🤔 Erster Versuch: Flexbox auf den ganzen Anzeigebereich, mit `row`. Was passiert?
""")

css(BODY, BUTTON_P, KA, HOVER, ANZ_ROW, KF, EINGABE)

md(r"""
Unbrauchbar: Frage, Antwort und beide Knöpfe stehen in **einer** Reihe. Ich will aber nicht **alles** nebeneinander, sondern nur die beiden Knöpfe. Dafür brauche ich eine **Kiste um genau diese beiden**.

In die `index.html`, die beiden Knöpfe umschließen. Führen Sie die Zelle aus:
""")

code(INDEX_K2)

md(r"""
> **Ins Heft:** `knopf-leiste` als **elfter** Eintrag Ihrer `id`-Liste.

Jetzt bekommt der Anzeigebereich `column` (untereinander) und die neue Knopfleiste Flexbox ohne Richtung, denn `row` ist die Voreinstellung:
""")

css(BODY, BUTTON_P, KA, HOVER, ANZ_COL, KF, EINGABE, LEISTE, neu=[ANZ_COL, LEISTE])

md(r"""
### Ausrichten

Zwei Wörter, die man dauernd verwechselt:

| Eigenschaft | arbeitet | bei einer Reihe also |
|---|---|---|
| `justify-content` | **in** Laufrichtung | links, mittig, rechts |
| `align-items` | **quer** dazu | oben, mittig, unten |

🖱️ Probieren Sie für `justify-content` nacheinander `flex-start`, `center`, `flex-end`, `space-between`. Nach jedem Wert ausführen und hinsehen.
""")

css(BODY, BUTTON_P, KA, HOVER, ANZ_COL, KF, EINGABE, LEISTE_AUS, neu=[LEISTE_AUS])

md(r"""
> **Wenn die Verwechslung bleibt:** Nicht bekämpfen. *„Ausprobieren ist schneller als merken. Schreiben Sie `center` hin und schauen Sie, ob es das war, was Sie wollten.“* Das ist ehrlich und genau das, was auch Profis tun.

So sieht `style.css` am Ende des gemeinsamen Teils aus:
""")

css(*ENDE)

# ================================================================== 8
md(r"""
---
## 8 Die eigene Gestaltung

Jetzt arbeiten Sie selbst. **Pflicht sind drei Aufgaben, danach freie Hand.** Nach jeder Änderung hinsehen, und wenn etwas nicht wirkt: den Namen laut vorlesen.

### ✏️ Pflicht

1. **Die Eingabefelder gestalten:** Rahmen, Innenabstand, Schriftgröße. Die Selektoren sind `input` und `textarea`.
2. **Ein `:hover`** für die Knöpfe, in Ihrer eigenen helleren oder dunkleren Farbe.
3. **Ihre eigenen drei Farben:** Hintergrund, Karte, Knöpfe. Prüfen Sie den Kontrast mit `kontrast(...)`.

> **Bewusst unterschiedliche Ergebnisse.** Am Ende sollen sich Ihre Anwendungen deutlich unterscheiden. Ab hier ist es **Ihre** Anwendung. Alles, was Sie brauchen, steht im Merkblatt. Was Sie aus dem Internet kopieren, können Sie später nicht reparieren.
""")

css(*ENDE, "/* Ihre Gestaltung: */\n")

code(r"""
// Ihre Farben prüfen: erst die Schrift, dann der Hintergrund
kontrast("#222222", "#f4f4f4");
""")

loesung("💡 Ein Vorschlag für Pflicht 1", r"""
```css
input {
  border: 1px solid #cccccc;
  border-radius: 6px;
  padding: 8px;
  font-size: 16px;
}

textarea {
  border: 1px solid #cccccc;
  border-radius: 6px;
  padding: 8px;
  font-size: 16px;
}
```

Die Eigenschaften dieses Kurses: `color`, `background-color`, `font-family`, `font-size`, `font-weight`, `padding`, `margin`, `border`, `border-radius`, `max-width`, `display: flex`, `flex-direction`, `gap`, `justify-content`, `align-items`, `cursor`.
""")

# ================================================================== 9
md(r"""
---
## 9 Absichtlicher Fehler: Semikolon und Klammer

### Die erste Variante: das fehlende Semikolon

Hinter `background-color: #ffffff` fehlt das Semikolon. 🤔 Was fehlt im Fenster?
""")

css(BODY, BUTTON_P, KA, HOVER, ANZ_COL.replace("background-color: #ffffff;", "background-color: #ffffff"), KF, EINGABE, LEISTE)

md(r"""
Der weiße Hintergrund **und** der Rahmen fehlen. `padding` und der Rest wirken noch.

Es fehlt nicht nur eine Zeile, sondern zwei. Ohne Semikolon weiß der Browser nicht, wo die eine Erklärung aufhört, und liest die nächste Zeile als Teil derselben: `background-color: #ffffff border: 2px solid #cccccc`. Das ergibt keinen Sinn, also wirft er beides weg und macht danach normal weiter.

Klappen Sie **🔎** auf: Bei `#anzeige` steht eine Zeile mit ❌. Dort sehen Sie genau, wie der Browser die beiden Erklärungen zu einer zusammengeklebt und dann verworfen hat. Reparieren Sie das Semikolon.

### Die zweite Variante: die fehlende Klammer

Jetzt fehlt bei `#anzeige` die schließende Klammer `}`. 🤔 Was passiert mit den Regeln darunter?
""")

css(BODY, BUTTON_P, KA, HOVER, ANZ_COL[:-1].rstrip("\n") + "\n", KF, EINGABE, LEISTE)

md(r"""
Das ist die schlimmere Sorte. Die Regel `#anzeige` hört nie auf, und **was darunter steht, wirkt nicht mehr richtig**: Der Eingabebereich verliert seine Anordnung, obwohl Sie an `#eingabe` nichts geändert haben.

> **Wenn Ihre letzten fünf Änderungen alle nicht wirken, suchen Sie nicht bei den fünf Änderungen. Suchen Sie darüber.**

Klappen Sie **🔎** auf: Bei `#anzeige` steht die Warnung, dass die Klammer fehlt, und dahinter kommt keine einzige weitere Regel mehr. Alles Folgende ist **in** `#anzeige` gerutscht.

Manches darunter scheint trotzdem noch zu wirken, etwa die große Frage oder die Knopfleiste. Das liegt daran, dass diese Elemente zufällig **innerhalb** von `#anzeige` stehen. Verlassen Sie sich nicht darauf: Gerade dieses „teils, teils“ macht die Suche so verwirrend.

Bauen Sie beide Fehler auch in eine eigene Fassung ein, sehen Sie hin, und reparieren Sie sie.
""")

# ================================================================== 10
md(r"""
---
## 10 Diagnosefragen, Checkliste und Ausblick

### Die zwei Diagnosefragen

```
Eine Regel wirkt nicht      → Namen laut vorlesen, # und . prüfen
ALLE Regeln ab hier nicht   → darüber suchen: Semikolon oder Klammer
```

### 🤔 Welche Ursache passt?

| Fehlerbild | Ursache |
|---|---|
| Nichts passiert, keine Fehlermeldung | |
| Falsches Element ändert sich | |
| Zwei Regeln, die erwartete gewinnt nicht | |
| Kasten wird beim Verkleinern abgeschnitten | |
| Zu viel steht nebeneinander | |
| Abstand innen gewünscht, außen entstanden | |
""")

loesung("💡 Auflösung", r"""
| Fehlerbild | Ursache |
|---|---|
| Nichts passiert, keine Fehlermeldung | Selektorname stimmt nicht mit der `id` überein |
| Falsches Element ändert sich | `#` und `.` vertauscht |
| Die erwartete Regel gewinnt nicht | Genauigkeit: `#id` schlägt `.klasse` schlägt `element` |
| Kasten wird abgeschnitten | `width` statt `max-width` |
| Zu viel steht nebeneinander | `display: flex` sitzt auf dem falschen Bereich |
| Abstand außen statt innen | `margin` statt `padding` |
""")

md(r"""
### ✅ Checkliste

Haken Sie ab (Doppelklick auf diese Zelle, dann `[ ]` zu `[x]` ändern):

- [ ] Die erste Regel geschrieben und die Teile einer Regel benannt
- [ ] Alle Knöpfe über den Typselektor gestaltet, eine Gruppe über die Klasse, einzelne über die `id`
- [ ] Den Merksatz erklären können: `#id` schlägt `.klasse` schlägt `element`
- [ ] Das Boxmodell am eigenen Element durchgespielt, `padding` und `margin` unterschieden
- [ ] Den Eingabebereich mit Flexbox angeordnet, `knopf-leiste` als elften Eintrag im Heft
- [ ] Eigene Farben gewählt, aus zwei Metern lesbar
- [ ] Beide Fehlerarten eingebaut, erkannt und repariert

### Wie geht es weiter?

Ihre App sieht jetzt aus wie eine Anwendung, aber sie **tut** noch nichts. In **K3 „JavaScript – die Bausteine“** lernen Sie die Sprache, mit der die App denkt. Achtung, Ansage: Dort passiert im Fenster erst einmal **nichts**, alles läuft in der Konsole. Das Begleit-Notebook dazu ist [M3](M03_JavaScript_Bausteine.ipynb).

> **Übertragen Sie Ihre Gestaltung:** Kopieren Sie Ihre fertige `style.css` aus Abschnitt 8 in Ihr Projekt. Sie gehört ab jetzt zu Ihrer App, bis zur Auslieferung in K7.

**Zum Nachschlagen:** K2 Merkblatt · K2 Übungsblatt
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
    c["id"] = f"m02-{i:03d}"
    c["source"] = c["source"].splitlines(keepends=True)

with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(len(cells), "Zellen geschrieben")
