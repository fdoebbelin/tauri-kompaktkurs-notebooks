"""Erzeugt content/M01_HTML_die_Struktur.ipynb für die JupyterLite-Seite."""
import json
import pathlib
import sys

HIER = pathlib.Path(__file__).parent
_m04 = (HIER / "gen_m04.py").read_text(encoding="utf-8")
exec(_m04.split("\n# ================================================================== Einstieg\n")[0])

KOPF = """<!-- index.html -->
<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <title>Lernkarten</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <h1>Lernkarten von Anna</h1>
"""
FUSS = """
    <script src="app.js"></script>
  </body>
</html>"""

EINGABE = """
    <div id="eingabe">
      <h2>Neue Karte</h2>
      <input id="frage-feld" type="text" placeholder="Frage" />
      <textarea id="antwort-feld" placeholder="Antwort"></textarea>
      <button id="knopf-neu">Karte anlegen</button>
    </div>
"""
ANZEIGE = """
    <div id="anzeige">
      <p id="karte-frage">Noch keine Karte</p>
      <p id="karte-antwort"></p>
      <button id="knopf-umdrehen" class="knopf-anzeige">Umdrehen</button>
      <button id="knopf-weiter" class="knopf-anzeige">Nächste</button>
    </div>
"""
LISTE_HTML = """
    <h2>Alle Karten</h2>
    <ul id="karten-liste"></ul>
"""


def neu_html(block):
    return "\n    <!-- ★ NEU -->" + block


K0 = KOPF + FUSS
E1 = KOPF + neu_html(EINGABE) + FUSS
E2 = KOPF + EINGABE + neu_html(ANZEIGE) + FUSS
E3 = KOPF + EINGABE + ANZEIGE + neu_html(LISTE_HTML) + FUSS
FERTIG = KOPF + EINGABE + ANZEIGE + LISTE_HTML + FUSS
OHNE_DIV = FERTIG.replace("""      <button id="knopf-neu">Karte anlegen</button>
    </div>
""", """      <button id="knopf-neu">Karte anlegen</button>
""")
assert OHNE_DIV != FERTIG
DOPPELT = FERTIG.replace('<p id="karte-antwort"></p>', '<p id="karte-frage"></p>')
assert DOPPELT != FERTIG

SETUP = (HIER / "m01_setup.js").read_text(encoding="utf-8")
SETUP = SETUP.replace("__HTML__", json.dumps(K0, ensure_ascii=False))


def wiese(text):
    code("<!-- spielwiese -->\n" + text.strip("\n"))


# ================================================================== Einstieg
md(r"""
# M1 – HTML: die Struktur

*Begleit-Notebook zu Modul **K1 „HTML – die Struktur“** im Kompaktkurs „Vom Web zur Desktop-App mit Tauri“*

In K0 haben Sie Ihre erste eigene Änderung gemacht: einen Namen in die Überschrift geschrieben. Jetzt bauen Sie die **vollständige Oberfläche** der Lernkarten-App. Sie sieht am Ende noch schlicht aus und tut noch nichts, aber **alle Bestandteile sind da, und jeder hat einen Namen.**

## 🎯 Das können Sie am Ende

- ein Element in seine Teile zerlegen: **Start-Tag, Inhalt, Ende-Tag**
- Elemente richtig verschachteln und sauber einrücken
- die **acht Elemente** dieses Kurses einsetzen
- Attribute schreiben, vor allem **`id`** und **`class`**, nach den Kursregeln
- die Oberfläche der Lernkarten-App in vier Etappen bauen
- Ihre **`id`-Liste** führen und gegen die Datei prüfen. Sie ist das eigentliche Ergebnis dieses Moduls.
- ein fehlendes `</div>` an der Einrückung erkennen

## 🧭 Inhalt

0. Vorbereitung
1. Wie ein Element aufgebaut ist
2. Verschachtelung und Einrückung
3. Die acht Elemente dieses Kurses
4. Attribute
5. `id` und `class`
6. Die Oberfläche der Lernkarten-App
7. Absichtlicher Fehler und Fehlerjagd
8. Stolperstellen, Checkliste und Ausblick auf K2
""")

md(r"""
## So funktioniert dieses Notebook

| Zelle beginnt mit | Was passiert |
|---|---|
| `<!-- index.html -->` | die ganze Datei, wie sie im Projekt steht. Darunter erscheint das Fenster. |
| `<!-- spielwiese -->` | nur ein Stück HTML. Es erscheint in der **Spielwiese** unter Ihrer Überschrift, so wie im Kurs. |

Beim Ausführen (**Umschalt + Enter**) zeigt ein kleines Fenster das Ergebnis. Dazu zwei Hilfen im Fenster:

| Hilfe | Wozu |
|---|---|
| **▣ Kisten zeigen** | zeigt den Rand jedes Elements gestrichelt, auch der unsichtbaren und leeren |
| **🔎 So hat der Browser Ihre index.html verstanden** | zum Aufklappen. Zeigt als Baum, **was in was** steckt, und alle `id`s. Hier sehen Sie, wenn etwas falsch verschachtelt ist. |

Und zwei Funktionen für normale Zellen: `idListe(...)` prüft Ihre Heftliste gegen die Datei, `idRegeln(...)` prüft Namen gegen die Kursregeln.

> **Halten Sie Heft und Stift bereit.** Die `id`-Liste wird von Hand mitgeschrieben. Was man einmal geschrieben hat, findet man wieder.

Die Zeichen: 🤔 **Vorhersage** · ✏️ **Ihre Aufgabe** · 🐞 **Absichtlicher Fehler** · 📓 **Ins Heft** · 💡 **Lösung**.
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
## 1 Wie ein Element aufgebaut ist

Das ist Ihre `index.html` vom Ende von K0:
""")

code(K0)

md(r"""
In K0 haben Sie einen Text zwischen zwei Marken geschrieben, ohne dass geklärt wurde, was die Marken bedeuten:

```
<h1>Lernkarten von Anna</h1>
 │   │                   │
 │   │                   └─ Ende-Tag: derselbe Name mit Schrägstrich
 │   └───────────────────── Inhalt: was im Fenster erscheint
 └───────────────────────── Start-Tag: sagt, was für ein Ding das ist
```

> **Element = Start-Tag + Inhalt + Ende-Tag.**

Eine Marke sagt: Hier fängt eine Überschrift an. Die andere sagt: Hier hört sie auf.

### 🐞 Erinnern Sie sich an den Fehler aus K0?

Fehlt das Ende-Tag, weiß der Browser nicht, wo das Element aufhört, und nimmt an, **es hört nie auf**. 🤔 Hier fehlt das Ende-Tag der Unterüberschrift. Wie sieht der Absatz darunter aus?
""")

wiese("""
<h2>Eine Unterüberschrift
<p>Dieser Absatz sollte ganz normal aussehen.</p>
""")

md(r"""
Der Absatz ist groß und fett geworden. Klappen Sie **🔎** auf: Der Absatz `p` steckt **in** der `h2`. Für den Browser ist er Teil der Überschrift.

Ergänzen Sie `</h2>` hinter „Unterüberschrift“ und führen Sie die Zelle erneut aus.
""")

# ================================================================== 2
md(r"""
---
## 2 Verschachtelung und Einrückung

Elemente dürfen **ineinander** liegen. 🤔 Was ändert sich im Fenster durch das `<div>` drumherum?
""")

wiese("""
<div>
  <p>Erster Absatz.</p>
  <p>Zweiter Absatz.</p>
</div>
""")

md(r"""
**Nichts.** Das ist beabsichtigt. Ein `<div>` ist ein **unsichtbarer Bereich**, eine Kiste, in die man Sachen legt. Klicken Sie auf **▣ Kisten zeigen**: Jetzt sehen Sie die Kiste um die beiden Absätze.

Wozu das gut ist, zeigt K2: Dann bekommt die ganze Kiste auf einmal einen Rahmen, und nicht jeder Absatz einzeln.

> ## Die Verschachtelungsregel
> **Was zuletzt aufgemacht wurde, wird zuerst wieder zugemacht.**
>
> ```
> richtig:  <div><p>Text</p></div>
> falsch:   <div><p>Text</div></p>
> ```
>
> Wie beim Anziehen: Das Hemd kommt vor der Jacke an und nach der Jacke aus.

**Einrückung** ist dem Rechner völlig egal. Sie ist ausschließlich für den Menschen da. Jede Verschachtelungsebene rückt **zwei Leerzeichen** weiter ein. Wer nicht einrückt, findet später seine eigenen Fehler nicht mehr. Deshalb ist die Einrückung Kursregel.

### 🤔 Was macht der Browser aus der falschen Reihenfolge?
""")

wiese("""
<div><p>Text</div></p>
<p>Ein Absatz danach.</p>
""")

md(r"""
Im Fenster sieht man kaum etwas. Klappen Sie **🔎** auf: Der Browser **repariert still**, so gut er kann, und baut sogar einen zusätzlichen, leeren Absatz. Er rät. Manchmal richtig, oft nicht. Verlassen Sie sich nicht darauf, sondern schreiben Sie es richtig.

> **Nicht vertiefen:** `<!DOCTYPE>`, `<head>` gegen `<body>`, `<meta charset>`, `<link>`: Das ist der Rahmen, den jede solche Datei braucht. Er ist vorbereitet und wird nicht angefasst.
""")

# ================================================================== 3
md(r"""
---
## 3 Die acht Elemente dieses Kurses

Mehr als diese acht braucht die App nicht:

| Element | Wofür |
|---|---|
| `<h1>`, `<h2>` | Überschriften |
| `<p>` | Textabsatz |
| `<div>` | unsichtbarer Bereich zum Gruppieren |
| `<button>` | Knopf |
| `<input>` | einzeiliges Eingabefeld |
| `<textarea>` | mehrzeiliges Eingabefeld |
| `<ul>`, `<li>` | Liste und Listeneintrag |
| `<span>` | kleiner Bereich mitten im Text |

Im Kurs wird jedes einmal in die Spielwiese eingebaut, angesehen und **wieder entfernt**. Hier hat jedes seine eigene Zelle. Verändern Sie die Texte ruhig.

> **Kommentare:** Die Zeile `<!-- … -->` ist eine **Notiz für Menschen**. Der Browser überliest sie. Kommentare sind eine gute Gewohnheit.

**1 · Überschriften**
""")

wiese("""
<!-- Die Zahl ist keine Größe, sondern eine Rangfolge -->
<h1>Hauptüberschrift</h1>
<h2>Unterüberschrift</h2>
""")

md(r"""
`h1` ist die Hauptüberschrift, `h2` eine Unterüberschrift. Dass `h2` kleiner aussieht, ist nur die Voreinstellung.

**2 · Absätze**
""")

wiese("""
<p>Erster Absatz.</p>
<p>Zweiter Absatz. Zwei Absätze stehen automatisch untereinander, mit Abstand.</p>
""")

md(r"""
**3 · Bereich:** siehe Abschnitt 2, das `<div>`.

**4 · Knopf**
""")

wiese("""
<button>Umdrehen</button>
""")

md(r"""
Der Knopf ist da und lässt sich drücken. Es passiert nur nichts. Das kommt in K4.

**5 · Einzeiliges Eingabefeld**
""")

wiese("""
<input placeholder="Frage" />
""")

md(r"""
Der graue Text ist nur ein **Hinweis** und verschwindet beim Tippen. Tippen Sie etwas hinein und löschen Sie es wieder: Der Hinweis kommt zurück.

**6 · Mehrzeiliges Eingabefeld**
""")

wiese("""
<textarea placeholder="Antwort"></textarea>
""")

md(r"""
### Die eine Ausnahme

```html
<input placeholder="Frage" />
<textarea placeholder="Antwort"></textarea>
```

> **Unlogisch, aber so ist es:** Das einzeilige Feld hat **kein** Ende-Tag, das mehrzeilige **schon**. Der Grund ist historisch. Das muss nicht verstanden, nur gewusst werden. Bei `<textarea>` stehen Start- und Ende-Tag direkt hintereinander, wenn das Feld leer sein soll.

🐞 Was passiert, wenn das Ende-Tag der `textarea` fehlt? 🤔 Vorhersage, dann ausführen:
""")

wiese("""
<textarea placeholder="Antwort">
<p>Dieser Absatz steht unter dem Feld.</p>
<button>Ein Knopf</button>
""")

md(r"""
Alles, was danach kommt, landet **als Text im Feld**: der Absatz, der Knopf, mit spitzen Klammern. Die `textarea` hört nie auf und verschluckt den Rest der Seite. Ergänzen Sie `</textarea>` und führen Sie erneut aus.

**7 · Liste**
""")

wiese("""
<ul>
  <li>Erster Eintrag</li>
  <li>Zweiter Eintrag</li>
  <li>Dritter Eintrag</li>
</ul>
""")

md(r"""
Die Liste `ul` ist der **Rahmen**, jeder Eintrag ein `li`. Beides gehört zusammen.

> **Merken:** In der App ist die `<ul>` beim Bau der Oberfläche **leer**. In K4 füllt das Programm sie selbst, für jede Karte einen Eintrag.

**8 · Kleiner Bereich im Text**
""")

wiese("""
<p>Das ist Karte <span>3</span> von 10.</p>
""")

md(r"""
Wie ein `div`, nur für ein einzelnes Wort mitten im Text. Im Fenster ist es unsichtbar. Schalten Sie **▣ Kisten zeigen** ein.

### 🤔 Welche zwei der acht Elemente sind im Fenster unsichtbar, obwohl sie da sind?
""")

loesung("💡 Antwort", r"""
**`<div>` und `<span>`.** Beide sind reine Bereiche ohne eigenes Aussehen. Sie werden erst in K2 nützlich, wenn ein ganzer Bereich auf einmal Rahmen oder Farbe bekommt.

Ebenfalls richtig: ein **leeres** `<p></p>` oder eine leere `<ul></ul>`. Sie sind da, aber ohne Inhalt nicht zu sehen.
""")

# ================================================================== 4
md(r"""
---
## 4 Attribute

Ein Attribut beschreibt ein Element näher. Es steht **im Start-Tag**, niemals im Ende-Tag.

```
<button id="knopf-umdrehen">Umdrehen</button>
        └┬┘ └──────┬──────┘
         │         └─ Wert, immer in Anführungszeichen
         └─ Attributname
```

Im Kurs werden vier Attribute benutzt:

| Attribut | Wofür |
|---|---|
| `id` | Name eines **einzelnen** Elements. Damit wird es ab K4 angesprochen. |
| `class` | **Gruppenname.** Mehrere Elemente dürfen dieselbe Klasse haben. |
| `placeholder` | grauer Hinweistext in einem Eingabefeld |
| `type` | Sorte des Eingabefelds. Im Kurs nur `type="text"`. |

### 🐞 Warum immer Anführungszeichen?

🤔 Beim ersten Feld fehlen die Anführungszeichen. Was steht als Hinweis darin?
""")

wiese("""
<input placeholder=Ihre Frage />
<input placeholder="Ihre Frage" />
""")

md(r"""
Im ersten Feld steht nur **„Ihre“**. Ohne Anführungszeichen endet der Wert beim ersten Leerzeichen, und „Frage“ wird für ein eigenes, sinnloses Attribut gehalten. Bei einem einzelnen Wort geht es zufällig gut. Deshalb gilt im Kurs: **immer** Anführungszeichen.
""")

# ================================================================== 5
md(r"""
---
## 5 `id` und `class`

> **Der Unterschied in einem Bild**
> Die **`id`** ist der eigene Name: den gibt es nur einmal.
> Die **`class`** ist die Schulklasse: die wird mit anderen geteilt.

Warum braucht es überhaupt Namen? *„Können Sie mir bitte das Blatt geben?“* in einem Raum mit drei Personen: Es passiert nichts, oder alle drei reagieren gleichzeitig. Deshalb bekommt jedes Element, das später angesprochen werden soll, einen Namen, das Attribut `id`.

### Regeln für `id`-Namen in diesem Kurs

1. **Alles klein:** `frage-feld`, nicht `Frage-Feld`
2. **Kein Leerzeichen**, stattdessen Bindestrich: `karten-liste`
3. **Auf Deutsch:** `knopf-neu`, nicht `new-button`
4. **Jede `id` nur einmal im ganzen Dokument**

Regeln 1 bis 3 sind **Kursregeln**, damit alle dasselbe schreiben. Regel 4 ist eine **echte Vorschrift**: Ein Name, der zweimal vergeben ist, ist kein Name mehr.

### 🤔 Welche Namen entsprechen den Kursregeln?

Entscheiden Sie selbst, dann führen Sie die Prüfung aus:

| Name | in Ordnung? |
|---|---|
| `frage-feld` | |
| `Karten-Liste` | |
| `knopf neu` | |
| `deleteButton` | |
| `karte-antwort` | |
| `eingabe` | |
""")

code(r"""
idRegeln("frage-feld", "Karten-Liste", "knopf neu", "deleteButton", "karte-antwort", "eingabe");
""")

md(r"""
`deleteButton` verstößt sogar gegen zwei Regeln: Großbuchstabe (Regel 1) **und** Englisch (Regel 3). Regel 3 kann die Prüfung nicht erkennen, die prüfen Sie selbst.

### 🐞 Regel 4 bricht erst in K4

In dieser Fassung ist eine `id` doppelt vergeben. 🤔 Sehen Sie im Fenster etwas Ungewöhnliches?
""")

code(DOPPELT)

md(r"""
**Nein.** Das Fenster sieht ganz normal aus. Genau das ist das Gefährliche: Eine doppelte `id` fällt beim Bauen der Oberfläche nicht auf. In K4 wird dann **stumm das falsche Element** angesprochen, ein Fehler ohne Fehlermeldung, der teuer zu suchen ist.

Klappen Sie **🔎** auf: Unten steht `karte-frage ⚠️ kommt 2-mal vor`. Im Kurs gibt es diese Warnung nicht. Deshalb: **sofort sauber vergeben.**

### `class` wird hier nur gesetzt

```html
<button id="knopf-umdrehen" class="knopf-anzeige">Umdrehen</button>
<button id="knopf-weiter" class="knopf-anzeige">Nächste</button>
```

Benutzt wird die Klasse in K2: Wenn zwei Knöpfe gleich aussehen sollen, wird die Klasse angesprochen und nicht jeder Knopf einzeln.

### 📓 Die eigene `id`-Liste

Legen Sie **jetzt** im Heft eine zweispaltige Tabelle an:

| `id` | wofür |
|---|---|
| | |

Jedes Mal, wenn eine `id` vergeben wird, tragen Sie sie dort ein.

> **Diese Liste ist das eigentliche Ergebnis dieses Moduls.** In K4 wird jedes dieser Elemente im Programm angesprochen. Wer die Liste dann nicht hat, sucht die Namen einzeln in der Datei zusammen.
""")

# ================================================================== 6
md(r"""
---
## 6 Die Oberfläche der Lernkarten-App

Gebaut wird in **vier Etappen**. Nach jeder Etappe: ausführen, hinsehen, die `id`s ins Heft eintragen, kurz durchatmen. Was neu ist, ist mit `<!-- ★ NEU -->` markiert.

### Etappe 1: Eingabebereich
""")

code(E1)

md(r"""
`type="text"` sagt, welche Sorte Feld es ist. Es gibt auch Zahlenfelder und Ankreuzfelder; im Kurs wird nur `text` benutzt.

> 📓 **Ins Heft:** `eingabe`, `frage-feld`, `antwort-feld`, `knopf-neu`

### Etappe 2: Anzeigebereich
""")

code(E2)

md(r"""
Zwei Dinge fallen auf und sind Absicht:

- In `karte-frage` steht ein Text, in `karte-antwort` steht **nichts**. Der Text kommt später vom Programm.
- Der leere Absatz ist unsichtbar, aber trotzdem da, **wie ein reservierter Stuhl**. Mit **▣ Kisten zeigen** sehen Sie ihn als dünne Linie.

> 📓 **Ins Heft:** `anzeige`, `karte-frage`, `karte-antwort`, `knopf-umdrehen`, `knopf-weiter`

### Etappe 3: Kartenliste
""")

code(E3)

md(r"""
Die Liste ist im Fenster unsichtbar. Genau so soll es sein: Es gibt noch keine Karten.

Es fühlt sich falsch an, etwas Leeres hinzuschreiben. Aber genau das ist der Unterschied zwischen einer Webseite und einer Anwendung: **Es wird der Platz gebaut, die Inhalte kommen später von selbst.**

> 📓 **Ins Heft:** `karten-liste`

### Etappe 4: Aufräumen und Gegenlesen

- Spielwiese entfernen, falls im Projekt noch Reste darin stehen
- Einrückung durchgehen und sauber machen
- **`id`-Liste gegen die Datei prüfen**

Im Kurs liest jede Person ihre Heftliste vor, und die Nachbarperson sucht die Namen in der Datei. Hier macht das `idListe`.

### ✏️ Ihre Aufgabe 6

Tragen Sie **alle zehn `id`s aus Ihrem Heft** ein, in Anführungszeichen, durch Komma getrennt, und führen Sie die Zelle aus. Fertig sind Sie, wenn jede Zeile ✅ zeigt und keine ⚠️ übrig ist.
""")

code(r"""
idListe("eingabe", "frage-feld");
""")

loesung("💡 Die zehn `id`s", r"""
```js
idListe("eingabe", "frage-feld", "antwort-feld", "knopf-neu",
        "anzeige", "karte-frage", "karte-antwort", "knopf-umdrehen", "knopf-weiter",
        "karten-liste");
```

> **Der Gegenlese-Schritt ist der Kern.** Er ersetzt in K4 eine lange Fehlersuche.
""")

md(r"""
### Die fertige Datei

Schalten Sie **▣ Kisten zeigen** ein und klappen Sie **🔎** auf: drei Bereiche, zehn `id`s, zwei leere Plätze.
""")

code(FERTIG)

md(r"""
| Stelle | Warum leer |
|---|---|
| `<p id="karte-antwort"></p>` | Der Text kommt später vom Programm. Der leere Absatz ist ein reservierter Platz. |
| `<ul id="karten-liste"></ul>` | Das Programm erzeugt für jede Karte einen Eintrag. Gebaut wird nur der Rahmen. |
| `style.css` | kommt in K2 dran |
| `app.js` | kommt ab K3 dran |
""")

# ================================================================== 7
md(r"""
---
## 7 Absichtlicher Fehler und Fehlerjagd

### 🐞 Ein nicht geschlossenes `<div>`

Hier fehlt das `</div>` von `#eingabe`. 🤔 Was verändert sich im Fenster?
""")

code(OHNE_DIV)

md(r"""
**Fast nichts.** Optisch ist der Unterschied klein, weil noch keine Rahmen und Farben gesetzt sind. Aber klappen Sie **🔎** auf: `div#anzeige`, die Überschrift „Alle Karten“ und die Liste stecken jetzt **in** `div#eingabe`.

> **Dieser Fehler tut jetzt kaum weh.** Sobald die Bereiche in K2 einen Rahmen bekommen, sitzt plötzlich der halbe Bildschirm im falschen Kasten, und der Fehler wurde hier gemacht.

**Zwei Handgriffe, die fast immer helfen:**

1. **Einrückung ansehen.** Wo die Einrückung nach rechts wandert und nicht zurückkommt, fehlt ein Ende-Tag. Hier: Nach `<button id="knopf-neu">` müsste die Einrückung zurückgehen. Sie tut es nicht.
2. **Im Editor auf eine spitze Klammer klicken:** Der Editor im Kurs zeigt die zugehörige an. Findet er keine, ist das der Beweis. (Hier im Notebook übernimmt das **🔎**.)

Reparieren Sie die Zelle: `</div>` hinter den Knopf „Karte anlegen“.

### Fehlerjagd

In jedem Schnipsel steckt **genau ein** Fehler. Führen Sie ihn aus, schauen Sie ins Fenster und in **🔎**, und reparieren Sie ihn.

**a)**
""")

wiese("<p>Das ist ein Absatz.</div>")

md("**b)**")

wiese("""
<div>
  <p>Text im Bereich.
</div>
<p>Absatz danach.</p>
""")

md("**c)**")

wiese("""
<textarea placeholder="Antwort" />
<button>Karte anlegen</button>
""")

md("**d)**")

wiese("""
<button id=knopf neu>Karte anlegen</button>
""")

md("**e)**")

wiese("""
<ul>
  Erster Eintrag
  Zweiter Eintrag
</ul>
""")

md("**f)**")

wiese("""
<div>
  <p>Erster</p>
  <p>Zweiter</p>
""")

loesung("💡 Lösungen zur Fehlerjagd", r"""
| | Fehler | Richtig |
|---|---|---|
| a) | Ende-Tag passt nicht zum Start-Tag | `<p>Das ist ein Absatz.</p>` |
| b) | dem Absatz fehlt das Ende-Tag; der Bereich schließt vorher | `<p>Text im Bereich.</p>` |
| c) | `<textarea>` braucht ein Ende-Tag, sonst verschluckt sie den Knopf | `<textarea placeholder="Antwort"></textarea>` |
| d) | Attributwert ohne Anführungszeichen, und dazu ein Leerzeichen im Namen | `id="knopf-neu"` |
| e) | Einträge einer Liste gehören in `<li>` | `<li>Erster Eintrag</li>` … |
| f) | dem `<div>` fehlt das Ende-Tag; die Einrückung kommt nicht zurück | `</div>` am Ende |

b) und f) sind **derselbe Fehlertyp** auf zwei Ebenen. Wer beide findet, hat das Prinzip verstanden.

Bei e) zeigt **🔎** den Fehler: loser Text direkt in der `ul`, kein einziges `li`.

Bei b) und f) dagegen repariert der Browser so still, dass Fenster **und** **🔎** völlig normal aussehen. Nur die **Einrückung** verrät den Fehler. Genau deshalb ist der Einrückungs-Handgriff so wichtig: Verlassen Sie sich nicht darauf, dass der Browser richtig rät. In einer größeren Datei rät er falsch, wie beim `</div>` von `#eingabe` oben.
""")

# ================================================================== 8
md(r"""
---
## 8 Stolperstellen, Checkliste und Ausblick

### Typische Stolperstellen

| Was zu sehen ist | Was das meistens heißt |
|---|---|
| Ab einer Stelle ist alles verrutscht | ein `</div>` oder `</textarea>` fehlt |
| Alles ist plötzlich riesig | ein `</h1>` oder `</h2>` fehlt |
| Der Rest der Seite steht als Text in einem Feld | `</textarea>` fehlt |
| Ein Attributwert ist abgeschnitten | Anführungszeichen vergessen |
| Der graue Hinweistext ist weg | es wurde ins Feld getippt; Feld leeren, er kommt zurück |
| Die Liste ist unsichtbar | sie ist leer, das ist richtig so |
| Alles sieht normal aus, aber eine `id` ist doppelt | fällt erst in K4 auf: Heftliste gegenlesen |

### ✅ Checkliste

Haken Sie ab (Doppelklick auf diese Zelle, dann `[ ]` zu `[x]` ändern):

- [ ] Alle acht Elemente einmal ausprobiert
- [ ] Die Oberfläche vollständig nachgebaut, sauber eingerückt, alle Bereiche geschlossen
- [ ] Zehn `id`-Namen im Heft, mit `idListe` gegen die Datei geprüft
- [ ] Die beiden Anzeige-Knöpfe tragen `class="knopf-anzeige"`
- [ ] Den `</div>`-Fehler an der Einrückung erkannt und repariert
- [ ] `style.css` und `app.js` sind weiterhin leer

### Wie geht es weiter?

Ihre Oberfläche ist vollständig, aber sie sieht aus wie ein Formular von 1995. In **K2 „CSS – das Aussehen“** wird daraus etwas, das man jemandem zeigen möchte. Dort brauchen Sie Ihre **`id`-Liste** zum ersten Mal: Jeder Name darin ist eine Adresse, an die Sie ein Aussehen schicken können. Das Begleit-Notebook dazu ist [M2](M02_CSS_das_Aussehen.ipynb).

**Zum Nachschlagen:** K1 Merkblatt · K1 Übungsblatt
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
    c["id"] = f"m01-{i:03d}"
    c["source"] = c["source"].splitlines(keepends=True)

with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(len(cells), "Zellen geschrieben")
