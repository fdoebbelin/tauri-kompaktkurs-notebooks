"""Erzeugt content/M00_Ankommen.ipynb für die JupyterLite-Seite."""
import json
import pathlib
import sys

HIER = pathlib.Path(__file__).parent
_m05 = (HIER / "gen_m05.py").read_text(encoding="utf-8")
exec(_m05.split("\n# ================================================================== Einstieg\n")[0])

K5_TEILE = [DATEN_LEER, LISTE, SPEICHERN, LADEN, NEU_K5, UMDREHEN, WEITER, START_LADEN]
FERTIG_JS = "\n\n".join(t.strip("\n") for t in K5_TEILE)
FERTIG_HTML = INDEX_HTML
FERTIG_CSS = STYLE_CSS


def projekt(body, titel="Lernkarten"):
    return f"""<!-- index.html -->
<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <title>{titel}</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
{body}

    <script src="app.js"></script>
  </body>
</html>"""


START = projekt("    <h1>Lernkarten</h1>")

SETUP = (HIER / "m00_setup.js").read_text(encoding="utf-8")
for platz, wert in [("__HTML__", START), ("__CSS__", ""), ("__JS__", ""), ("__DESKTOP__", ""),
                    ("__FERTIG_HTML__", FERTIG_HTML), ("__FERTIG_CSS__", FERTIG_CSS), ("__FERTIG_JS__", FERTIG_JS)]:
    assert platz in SETUP, platz
    SETUP = SETUP.replace(platz, json.dumps(wert, ensure_ascii=False))

WO = 'if ("/run/.toolboxenv" | path exists) { print "im Container" } else { print "auf dem Host" }'


def terminal(*zeilen):
    code("# Terminal\n" + "\n".join(zeilen))


# ================================================================== Einstieg
md(r"""
# M0 – Ankommen und erste eigene Änderung

*Begleit-Notebook zu Modul **K0 „Ankommen und erste eigene Änderung“** im Kompaktkurs „Vom Web zur Desktop-App mit Tauri“*

Willkommen! In diesem Kurs bauen Sie Ihre **erste eigene Desktop-Anwendung**: eine Lernkarten-App mit Fragen und Antworten. Am Ende steht sie in Ihrem Anwendungsmenü und startet ohne Terminal.

Dieses Notebook begleitet die erste Kurseinheit. Sie sehen, wohin die Reise geht, lernen die drei Dateien kennen, aus denen die App besteht, und machen Ihre **erste eigene Änderung**.

## 🎯 Das können Sie am Ende

- beschreiben, was die fertige Lernkarten-App kann
- die drei Dateien `index.html`, `style.css` und `app.js` benennen und sagen, wofür jede zuständig ist
- die App mit drei Befehlen starten und prüfen, ob Sie im Container sind
- eine Änderung im Quelltext machen und im Fenster wiederfinden
- einen Fehler absichtlich einbauen, beschreiben und reparieren

## 🧭 Inhalt

0. Vorbereitung
1. Das Ziel des Kurses
2. Die drei Ebenen: Struktur, Aussehen, Verhalten
3. Die Anwendung starten
4. Die erste eigene Änderung
5. Absichtlicher Fehler: das fehlende Ende-Tag
6. Stolperstellen, Checkliste und Ausblick auf K1
""")

md(r"""
## So funktioniert dieses Notebook

Ein Notebook besteht aus **Zellen**. Textzellen wie diese lesen Sie einfach. Zellen mit grauem Hintergrund führen Sie aus: **anklicken, dann Umschalt + Enter**. Das Ergebnis erscheint darunter.

| Zelle beginnt mit | Was passiert |
|---|---|
| `# Fertige App` | die fertige Lernkarten-App, so wie sie am Ende des Kurses aussieht |
| `# Ebene 1`, `# Ebene 2`, `# Ebene 3` | die App Schicht für Schicht |
| `# Terminal` | ein **Übungs-Terminal**. Jede weitere Zeile ist ein Befehl. |
| `<!-- index.html -->` | **Ihr Projekt**: die Datei, die Sie ändern. Darunter erscheint das Fenster Ihrer App. |

> **📌 Ehrlicher Hinweis:** Container, Terminal und App-Fenster sind hier im Browser **nachgebildet**. Die Befehle sind genau die aus dem Kurs. Im Kurs tippen Sie sie auf Ihrem Rechner.

Die Zeichen im Notebook: 🤔 **Vorhersage** · ✏️ **Ihre Aufgabe** · 🐞 **Absichtlicher Fehler** · 🖱️ **Ausprobieren** · 💡 **Lösung** (zum Aufklappen).

> ## Drei Sätze für den ganzen Kurs
> 1. **Kaputtmachen ist erlaubt.** Es geht nichts verloren.
> 2. **Der Rechner sagt meistens, wo das Problem liegt.** Diese Meldungen zu lesen wird geübt.
> 3. **Jeder baut Fehler ein**, auch nach Jahren. Der Unterschied ist nur, wie schnell man sie findet.
""")

# ================================================================== 0
md(r"""
---
## 0 Vorbereitung

Führen Sie die eingeklappte Zelle **als Erstes** aus. Sie enthält die Werkzeuge für dieses Notebook. Wenn darunter **🧰 Werkzeugkiste bereit** steht, kann es losgehen.
""")

code(SETUP, hidden=True)

# ================================================================== 1
md(r"""
---
## 1 Das Ziel des Kurses

So sieht die App aus, die Sie bauen werden. Führen Sie die Zelle aus.
""")

code("# Fertige App")

md(r"""
🖱️ **Probieren Sie die fünf Schritte**, die Sie am Ende selbst können:

1. **Eine Karte anlegen:** Frage eintippen, Antwort eintippen, „Karte anlegen“ drücken.
2. Die Karte **erscheint in der Liste**.
3. **„Umdrehen“:** zuerst erscheint die Frage, beim zweiten Klick die Antwort.
4. **„Nächste“:** die nächste Karte.
5. Oben auf **⟳ Neu starten** klicken, also die App schließen und neu öffnen. **Die Karten sind noch da.**

Im Kurs stehen am Anfang zwei Fenster nebeneinander: diese fertige App und Ihr eigenes, noch leeres Projekt. **Der Abstand dazwischen ist das Kursprogramm.**

> **Was hier noch nicht erklärt wird:** kein Tauri, kein Rust, kein Container, kein Flatpak. Nichts davon wird jetzt gebraucht. Die Begriffe kommen dann, wenn sie gebraucht werden.

### 🤔 Was ist wohl der schwierigste Teil davon?

Überlegen Sie kurz, bevor Sie aufklappen.
""")

loesung("💡 Die ehrliche Vorwarnung", r"""
Das Schwierigste kommt mit **JavaScript in K3**: der Teil, der dafür sorgt, dass beim Klick etwas passiert. Alles davor ist leichter, als es aussieht.

Das wird **vorher** gesagt, damit es später als eingeplant erlebt wird und nicht als persönliches Scheitern.
""")

# ================================================================== 2
md(r"""
---
## 2 Die drei Ebenen: Struktur, Aussehen, Verhalten

Jede Anwendung dieser Art besteht aus **drei Sorten Text**. Sie liegen im Ordner `src/`:

| Datei | Vergleich | zuständig für |
|---|---|---|
| `index.html` | **Rohbau** eines Hauses | **was** da ist |
| `style.css` | **Anstrich und Möbel** | **wie** es aussieht |
| `app.js` | die **Bewohner** | **was passiert** |

- Der **Rohbau** legt fest, dass es einen Knopf gibt.
- Der **Anstrich** legt fest, dass der Knopf blau ist und runde Ecken hat.
- Die **Bewohner** legen fest, was passiert, wenn jemand daraufdrückt.

Sehen Sie sich die fertige App Schicht für Schicht an. Führen Sie die drei Zellen nacheinander aus.

**Ebene 1:** nur der Rohbau
""")

code("# Ebene 1")

md(r"""
Alles ist da: Überschriften, Felder, Knöpfe, aber in der Werkseinstellung des Browsers. 🖱️ Drücken Sie auf einen Knopf: **Nichts passiert.**

**Ebene 2:** Rohbau und Anstrich
""")

code("# Ebene 2")

md(r"""
Derselbe Rohbau, jetzt mit Farben, Abständen und Rahmen. Die Knöpfe tun aber immer noch nichts.

**Ebene 3:** Rohbau, Anstrich und Bewohner
""")

code("# Ebene 3")

md(r"""
🖱️ Jetzt funktionieren die Knöpfe. Die Karten, die Sie in Abschnitt 1 angelegt haben, sind auch hier. Es ist ja dieselbe App.

### Wann kommt welche Datei dran?

| Datei | gefüllt ab |
|---|---|
| `index.html` | **jetzt**, in K0 und K1 |
| `style.css` | K2 |
| `app.js` | K3 |

Zwei der drei Dateien in Ihrem Projekt sind am Anfang leer und bleiben es vorerst.

### 🤔 Welche Datei wird angefasst?

| Wunsch | Datei |
|---|---|
| „Ich möchte, dass die Überschrift grün wird.“ | |
| „Ich möchte einen zweiten Knopf hinzufügen.“ | |
| „Ich möchte, dass beim Klick eine Karte erscheint.“ | |
| „Ich möchte, dass die Knöpfe runde Ecken haben.“ | |
| „Ich möchte ein drittes Eingabefeld.“ | |
""")

loesung("💡 Auflösung", r"""
| Wunsch | Datei | weil |
|---|---|---|
| Überschrift grün | `style.css` | Aussehen |
| zweiter Knopf | `index.html` | etwas Neues ist **da** |
| beim Klick eine Karte | `app.js` | etwas **passiert** |
| runde Ecken | `style.css` | Aussehen |
| drittes Eingabefeld | `index.html` | etwas Neues ist **da** |

> **Die Grenze ist unscharf.** Farben lassen sich auch in HTML setzen, und Elemente auch aus JavaScript erzeugen. In K4 erzeugt das Programm tatsächlich Listeneinträge. Für den Einstieg gilt die einfache Zuordnung.
""")

# ================================================================== 3
md(r"""
---
## 3 Die Anwendung starten

Diese Befehle brauchen Sie, um überhaupt zu arbeiten. Sie stehen auch auf der **Befehlskarte**, die im Kurs ausgedruckt auf dem Tisch liegt. Im Kurs tippen alle mit.

Das Übungs-Terminal startet, wo Sie im Kurs stehen: **auf dem Host**, also auf Ihrem Rechner selbst, im Home-Ordner `~`.

### Schritt 1: in den Container und in den Projektordner
""")

terminal("# Wo bin ich?", WO, "", "# In den Container", "toolbox enter tauri-dev", WO,
         "", "# In den Projektordner", "cd ~/Projekte/lernkarten")

md(r"""
| Befehl | Was er tut |
|---|---|
| `toolbox enter tauri-dev` | in den **Container** wechseln: eine abgetrennte Umgebung in Ihrem Rechner, in der alle Werkzeuge zum Bauen liegen. Ihr eigentliches System bleibt unberührt. |
| `cd ~/Projekte/lernkarten` | *change directory*: in den Ordner mit dem Projekt wechseln |

**Woran sehen Sie, dass Sie im Container sind?** Vorne in der Eingabezeile steht ein Sechseck: **⬢ tauri-dev**. Und die lange Zeile mit `/run/.toolboxenv` beantwortet sicher die Frage *„Wo bin ich eigentlich?“*. Sie wird in K7 wieder gebraucht, weil dort bewusst **außerhalb** des Containers gearbeitet wird.

### Schritt 2: die Anwendung starten

> **⚠️ Ansage vorweg: Der erste Start dauert spürbar länger.** Dabei läuft sehr viel Text durch das Terminal. Das ist **kein Absturz**: Das Programm wird gerade übersetzt. Jeder weitere Start geht schnell.

Davor ordnet `swaymsg splith` die Fenster nebeneinander an: Editor links, Anwendung rechts. Dieser Aufbau bleibt den ganzen Kurs über.
""")

terminal("swaymsg splith", "cargo tauri dev")

md(r"""
Das ist **Ihr Projekt**, noch fast leer: nur eine Überschrift. Den Abstand zur fertigen App aus Abschnitt 1 schließen Sie in den nächsten Modulen.

**Anwendung beenden:** im Terminal `Strg` + `C`, danach `exit` für den Container. Das geht im Übungs-Terminal nicht, es läuft nichts wirklich.

> **Weißes Fenster?** Ein bekanntes Problem der Grafikausgabe. Es sollte durch die Vorbereitung erledigt sein. Falls doch, startet man so:
> ```nu
> with-env { WEBKIT_DISABLE_DMABUF_RENDERER: "1" } { cargo tauri dev }
> ```

### 🤔 Die drei Befehle

Welche drei Befehle starten die App, und was tut jeder? Antworten Sie, ohne nach oben zu schauen.
""")

loesung("💡 Antwort", r"""
```nu
toolbox enter tauri-dev     # in den Container wechseln
cd ~/Projekte/lernkarten    # in den Projektordner wechseln
cargo tauri dev             # bauen und das Fenster öffnen
```

Beendet wird mit `Strg` + `C`, danach `exit`.
""")

# ================================================================== 4
md(r"""
---
## 4 Die erste eigene Änderung

Das ist Ihre Datei `src/index.html`. Führen Sie die Zelle aus: Darunter erscheint das Fenster Ihrer App.
""")

code(START)

md(r"""
In der Datei steht diese Zeile:

```html
<h1>Lernkarten</h1>
```

Geändert wird **der Text zwischen den beiden Marken**. Was `<h1>` und `</h1>` genau bedeuten, klärt K1. Für jetzt genügt: Dazwischen steht der Text, der im Fenster erscheint.

### ✏️ Ihre Aufgabe 4

Schreiben Sie in der Zelle oben **Ihren eigenen Namen** dazu, zum Beispiel `Lernkarten von Anna`, und führen Sie die Zelle erneut aus. Schauen Sie ins Fenster.

> ## Der Ablauf, der den ganzen Kurs gilt
> **Ändern → Speichern → Hinsehen.** Nach jeder einzelnen Änderung.
>
> Wer fünf Dinge auf einmal ändert und dann hinschaut, weiß bei einem Fehler nicht mehr, welche der fünf Änderungen ihn verursacht hat.

Im Notebook ist „Speichern“ das Ausführen der Zelle. In der echten App speichern Sie im Editor. Erscheint die Änderung nicht sofort: Rechtsklick ins Anwendungsfenster → **Neu laden**.

### Weitere Änderungen, eine nach der anderen

Machen Sie in derselben Zelle eigene Änderungen, **mit Hinsehen dazwischen**. Vorschläge, falls nichts einfällt:

1. einen zweiten Satz unter der Überschrift einfügen
2. die Überschrift kleiner machen
3. einen eingefügten Satz wieder löschen
4. zwei Sätze untereinander einfügen und ihre Reihenfolge tauschen
""")

loesung("💡 So geht es", r"""
Ein Satz ist ein Absatz. Er steht zwischen `<p>` und `</p>`, unter der Überschrift:

```html
    <h1>Lernkarten von Anna</h1>
    <p>Hier lerne ich für meine Umschulung.</p>
```

**Kleiner machen:** Aus `<h1>` und `</h1>` wird `<h2>` und `</h2>`. Beide Marken ändern!

```html
    <h2>Lernkarten von Anna</h2>
```

**Reihenfolge tauschen:** die beiden `<p>`-Zeilen ausschneiden und in umgekehrter Reihenfolge wieder einfügen.
""")

md(r"""
> **⚠️ Farbe ändern gehört noch nicht hierher.** Naheliegend wäre, die Textfarbe zu ändern. Dafür braucht es CSS, und CSS hat seinen eigenen großen Moment in K2. Jetzt ändern wir nur, **was** dasteht, noch nicht, **wie** es aussieht.
>
> Sichtbare Änderung ohne CSS: `<h1>` in `<h2>` ändern. Der Text wird kleiner, ganz ohne Anstrich.

### 🤔 Wo steht der Fenstertitel?

Oben im Kopf der Datei steht noch ein Text: `<title>Lernkarten</title>`. Ändern Sie ihn in der Zelle unten. 🤔 Wo erscheint die Änderung?
""")

code(projekt("    <h1>Lernkarten von Anna</h1>", titel="Annas Lernkarten"))

md(r"""
**Nicht** im Fensterinhalt, sondern in der **Fensterleiste** oben (im Kurs in der Fensterliste von Sway). Nicht alles im Quelltext ist Inhalt des Fensters.
""")

# ================================================================== 5
md(r"""
---
## 5 Absichtlicher Fehler: das fehlende Ende-Tag

Jetzt wird absichtlich etwas kaputtgemacht. Hier fehlt das schließende `</h1>`. 🤔 **Vorhersage:** Wie sieht der Satz darunter aus?
""")

code(projekt("""    <h1>Lernkarten von Anna
    <p>Hier lerne ich für meine Umschulung.</p>
    <p>Und noch ein Satz.</p>"""))

md(r"""
Der gesamte folgende Inhalt wird **groß und fett**. Aber **nichts stürzt ab.**

**Was passiert ist:** Es wurde nicht gesagt, wo die Überschrift **aufhört**. Also nimmt das Programm an, sie hört nie auf: Alles danach ist jetzt Überschrift. Das Programm **rät, statt zu versagen**.

✏️ Reparieren Sie die Zelle: `</h1>` hinter „Anna“ ergänzen, ausführen, hinsehen. Bauen Sie den Fehler danach noch einmal selbst ein und reparieren Sie ihn wieder. Wer einmal absichtlich kaputt gemacht und selbst repariert hat, ruft beim nächsten unabsichtlichen Fehler seltener sofort nach Hilfe.

### 🐞 Noch eine Stolperstelle: der Name in der Marke

🤔 Hier ist der Text **in** die Marke gerutscht. Was erscheint im Fenster?
""")

code(projekt("    <h1 Lernkarten von Anna>"))

md(r"""
**Gar nichts.** Für den Browser ist `Lernkarten von Anna` jetzt Teil der Marke, keine Beschriftung. Richtig ist: `<h1>Lernkarten von Anna</h1>`, der Text steht **zwischen** den Marken.

### 🤔 Was unterscheidet so einen Fehler von einem abgestürzten Programm?
""")

loesung("💡 Antwort", r"""
**Nichts stürzt ab, nichts geht verloren.** Das Programm rät und arbeitet mit der wahrscheinlichsten Annahme weiter. Deshalb gilt: **Kaputtmachen ist erlaubt.** Reparieren lässt es sich immer.

Dieselbe Erfahrung kommt im Kurs bewusst wieder: in K1 mit einem nicht geschlossenen `<div>` und in K2 mit einem fehlenden Semikolon.
""")

# ================================================================== 6
md(r"""
---
## 6 Stolperstellen, Checkliste und Ausblick

### Typische Stolperstellen

| Was zu sehen ist | Was das meistens heißt |
|---|---|
| weißes Fenster | bekanntes Grafikproblem: Start mit `WEBKIT_DISABLE_DMABUF_RENDERER`, siehe Abschnitt 3 |
| nichts ändert sich | nicht gespeichert, oder die falsche Datei geändert. Im Notebook: Zelle nicht ausgeführt. |
| der erste Start dauert ewig | normal, das Programm wird übersetzt. Kein Absturz. |
| alles ist plötzlich riesig und fett | ein `</h1>` fehlt |
| der Text erscheint gar nicht | der Text ist in die Marke gerutscht: `<h1 Text>` statt `<h1>Text</h1>` |
| `toolbox: already inside a toolbox container` | Sie sind schon im Container |

### ✅ Checkliste

Haken Sie ab (Doppelklick auf diese Zelle, dann `[ ]` zu `[x]` ändern):

- [ ] Die fertige App ausprobiert: anlegen, umdrehen, blättern, neu starten
- [ ] Die drei Dateien benannt und ihre Zuständigkeit erklärt
- [ ] Die drei Startbefehle getippt und geprüft, ob ich im Container bin
- [ ] Eine Änderung im Quelltext gemacht und im Fenster wiedergefunden
- [ ] Einen Fehler eingebaut, beschrieben und behoben
- [ ] Ich kenne den Ablauf: **Ändern → Speichern → Hinsehen**

### Wie geht es weiter?

In **K1 „HTML – die Struktur“** erfahren Sie, was `<h1>` und `</h1>` genau bedeuten, und bauen die **vollständige Oberfläche** der Lernkarten-App: Eingabefelder, Knöpfe, Liste. Das Begleit-Notebook dazu ist [M1](M01_HTML_die_Struktur.ipynb).

**Zum Nachschlagen:** K0 Merkblatt · K0 Übungsblatt · Anhang Befehlskarte
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
    c["id"] = f"m00-{i:03d}"
    c["source"] = c["source"].splitlines(keepends=True)

with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(len(cells), "Zellen geschrieben")
