"""Erzeugt content/M03_JavaScript_Bausteine.ipynb für die JupyterLite-Seite."""
import json
import sys

cells = []


def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": text.strip("\n")})


def code(text, error=False, hidden=False):
    meta = {}
    if error:
        meta["tags"] = ["raises-exception"]
    if hidden:
        meta["jupyter"] = {"source_hidden": True}
    cells.append({
        "cell_type": "code",
        "metadata": meta,
        "execution_count": None,
        "outputs": [],
        "source": text.strip("\n"),
    })


def loesung(titel, inhalt):
    """Aufklappbare Lösung als Markdown-Zelle."""
    md(f"<details>\n<summary><b>{titel}</b> (zum Aufklappen anklicken)</summary>\n\n{inhalt.strip()}\n\n</details>")


# ---------------------------------------------------------------- Einstieg
md(r"""
# M3 – JavaScript: die Bausteine

*Begleit-Notebook zu Modul **K3 „JavaScript – die Bausteine“** im Kompaktkurs „Vom Web zur Desktop-App mit Tauri“*

Ihre Lernkarten-App hat schon eine **Struktur** (HTML, K1) und ein **Aussehen** (CSS, K2). Jetzt lernen Sie die Sprache, mit der die App **denkt**: JavaScript. In diesem Notebook probieren Sie jeden Baustein sofort aus, ohne die App neu zu starten. Alles, was Sie hier üben, landet in K4 in Ihrer `app.js`.

> **⚠️ Die Ansage vorweg: In diesem Modul passiert im Fenster nichts.**
> Alle Ergebnisse erscheinen als Text: hier im Notebook direkt unter der Zelle, in der App in der **Konsole**.
> Nach HTML und CSS mit sofort sichtbarem Ergebnis ist das ungewohnt. Halten Sie durch: In K4 werden aus diesen Bausteinen Knöpfe, die funktionieren.

## 🎯 Das können Sie am Ende

- Werte in Variablen ablegen und wissen, wann `const` und wann `let` passt
- Zahl, Text und Wahrheitswert unterscheiden, Texte verbinden und mit `.trim()` säubern
- eigene **Funktionen** schreiben **und aufrufen**, und den Unterschied zwischen `return` und `console.log` erklären
- mit `if` und `else` Entscheidungen treffen
- **Listen** und **Objekte** anlegen, lesen, ändern und durchlaufen
- den Datenbestand der Lernkarten-App lesen: `karten[0].frage` in Worten erklären
- `undefined` und rote Fehlermeldungen mit der **Diagnosetabelle** deuten

## 🧭 Inhalt

0. Vorbereitung
1. Die Konsole
2. Variablen
3. Die Datentypen
4. Funktionen
5. Entscheidungen mit `if`
6. Listen
7. Objekte
8. Beides zusammen: der Datenbestand
9. Absichtlicher Fehler: `undefined` und die rote Meldung
10. Fehlerjagd
11. Die Diagnosetabelle
12. Lernkarten-Werkstatt
13. Checkliste und Ausblick auf K4
""")

md(r"""
## So arbeiten Sie mit diesem Notebook

| Was | Wie |
|---|---|
| Zelle ausführen | Zelle anklicken, dann **Umschalt + Enter** |
| Ausgabe ansehen | erscheint direkt unter der Zelle. Das ist Ihre **Konsole**. |
| Zeilennummern einschalten | **Esc**, dann **Umschalt + L**. Für Fehlermeldungen sehr hilfreich. |
| Alles durcheinander? | Menü **Kernel → Restart Kernel**, dann die Vorbereitungszelle (Abschnitt 0) erneut ausführen |

Die Zeichen im Notebook:

| Zeichen | Bedeutung |
|---|---|
| 🤔 **Vorhersage** | Erst überlegen und laut sagen oder aufschreiben, **dann** ausführen. Hier lernen Sie am meisten. |
| ✏️ **Ihre Aufgabe** | Code ergänzen. Eine Prüfung meldet ✅ oder ❌. |
| 🐞 **Absichtlicher Fehler** | Hier **soll** etwas schiefgehen. Lesen Sie die Meldung, statt sie wegzuklicken. |
| 💡 **Lösung** | aufklappbar. Erst selbst versuchen! |

### Notebook und App im Vergleich

| | Hier im Notebook | In der Lernkarten-App |
|---|---|---|
| Wo steht der Code? | in den Zellen | in `src/app.js` |
| Wie wird er ausgeführt? | Umschalt + Enter | speichern, dann Rechtsklick ins Fenster → **Neu laden** |
| Wo erscheint die Ausgabe? | unter der Zelle | Rechtsklick → **Element untersuchen** → Reiter **Konsole** |

> **📌 Eine Besonderheit des Notebooks**
> Was Sie mit `const` oder `let` anlegen, kennt **nur die eigene Zelle**. Funktionen dagegen bleiben bekannt, sobald ihre Zelle einmal ausgeführt wurde.
> In `app.js` ist das anders: Dort steht alles in **einer** Datei, und jede Zeile kennt, was darüber steht.
> Deshalb bringt hier jede Zelle die Daten, die sie braucht, selbst mit.
""")

# ---------------------------------------------------------------- 0 Vorbereitung
md(r"""
---
## 0 Vorbereitung

Führen Sie die folgende Zelle **als Erstes** aus. Sie ist eingeklappt, weil Sie sie nicht lesen müssen, genau wie den vorbereiteten Rust-Teil Ihrer App. Sie sorgt für zwei Dinge:

- Die Ausgaben sehen aus wie in der echten Konsole. Ohne sie würde das Notebook zum Beispiel `undefined` als leere Zeile anzeigen.
- Sie bringt die Prüffunktion `pruefe(...)` mit, die Ihre Aufgaben mit ✅ oder ❌ bewertet.

Wenn darunter **🧰 Werkzeugkiste bereit** steht, kann es losgehen.
""")

code(r"""
// Vorbereitete Werkzeugkiste: nur ausführen, nicht lesen müssen.
// Sie verwendet Schreibweisen, die im Kurs bewusst NICHT vorkommen.
(function () {
  function zeige(wert, tiefe) {
    if (wert === undefined) { return "undefined"; }
    if (wert === null) { return "null"; }
    if (typeof wert === "string") { return tiefe === 0 ? wert : '"' + wert + '"'; }
    if (typeof wert === "function") { return "ƒ " + (wert.name || "anonym") + "()"; }
    if (Array.isArray(wert)) {
      if (wert.length === 0) { return "[]"; }
      const teile = wert.map(function (w) { return zeige(w, tiefe + 1); });
      const mitObjekten = wert.some(function (w) { return w !== null && typeof w === "object"; });
      if (mitObjekten) {
        const einzug = "  ".repeat(tiefe + 1);
        return "[\n" + einzug + teile.join(",\n" + einzug) + "\n" + "  ".repeat(tiefe) + "]";
      }
      return "[" + teile.join(", ") + "]";
    }
    if (typeof wert === "object") {
      const felder = Object.keys(wert);
      if (felder.length === 0) { return "{}"; }
      return "{ " + felder.map(function (f) { return f + ": " + zeige(wert[f], tiefe + 1); }).join(", ") + " }";
    }
    return String(wert);
  }
  function ausgabe(kanal, werte) {
    const text = Array.prototype.map.call(werte, function (w) { return zeige(w, 0); }).join(" ");
    postMessage({ type: "stream", bundle: { name: kanal, text: text + "\n" } });
  }
  console.log = function () { ausgabe("stdout", arguments); };
  console.info = console.log;
  console.error = function () { ausgabe("stderr", arguments); };
  console.warn = console.error;
})();

// Die Prüffunktion. Ab Abschnitt 5 können Sie sie selbst lesen.
function pruefe(beschreibung, ergebnis, erwartet) {
  if (ergebnis === erwartet) {
    console.log("✅ " + beschreibung);
  } else {
    console.log("❌ " + beschreibung);
    console.log("     erwartet: " + erwartet);
    console.log("     bekommen: " + ergebnis);
  }
}

console.log("🧰 Werkzeugkiste bereit.");
""", hidden=True)

# ---------------------------------------------------------------- 1 Konsole
md(r"""
---
## 1 Die Konsole

In der App öffnen Sie die Konsole mit Rechtsklick ins Fenster → **Element untersuchen** → Reiter **Konsole**. Sie ist ab jetzt Ihr wichtigstes Werkzeug: Alles, was Ihr Programm ausgibt, erscheint dort, und alle Fehlermeldungen auch.

Hier im Notebook ist die Konsole der Bereich unter der Zelle. Die erste Zeile Ihrer `app.js`:
""")

code(r"""
console.log("Hallo Konsole");
""")

md(r"""
Ändern Sie den Text zwischen den Anführungszeichen und führen Sie die Zelle erneut aus.

> **Zwei Ausgabeorte auseinanderhalten**
> In der App gibt es zwei Stellen, an denen Text erscheint:
>
> | Ort | zeigt |
> |---|---|
> | **Terminal** | Meldungen des Programmkerns (Rust) |
> | **Konsole** | alles aus `app.js` |
>
> Wer eine Ausgabe aus `app.js` im Terminal sucht, findet nichts.

**Selbst eintippen.** Unten in der Konsole der App können Sie Befehle direkt eintippen und sofort das Ergebnis sehen. Das Notebook verhält sich ähnlich: Steht in der **letzten Zeile** einer Zelle ein Wert ohne `console.log`, wird er angezeigt.
""")

code(r"""
// Kein console.log: Das Notebook zeigt den Wert der letzten Zeile trotzdem an,
// so wie die Konsole, wenn Sie dort etwas eintippen.
3 + 4
""")

md(r"""
> **Das ständige `undefined` in der App-Konsole**
> In der echten Konsole erscheint nach jedem eingetippten Befehl zusätzlich eine Zeile `undefined`. Das ist die Antwort auf die Frage „Was ist dabei herausgekommen?“. Bei `console.log` kommt nichts heraus, es wird nur ausgegeben. Diese Zeile können Sie ignorieren. Das Notebook lässt sie weg.
""")

# ---------------------------------------------------------------- 2 Variablen
md(r"""
---
## 2 Variablen

> Eine Variable ist eine **beschriftete Schublade**. Sie legen etwas hinein und holen es später über die Beschriftung wieder heraus. Links steht der Name, rechts der Inhalt, das Gleichheitszeichen legt hinein.
""")

code(r"""
const name = "Anna";
let punkte = 0;
console.log(name);
console.log(punkte);
""")

md(r"""
| | Bedeutung |
|---|---|
| `const` | Diese Schublade wird **einmal** gefüllt und danach nicht mehr. |
| `let` | Der Inhalt **darf wechseln**. |

### 🐞 Absichtlicher Fehler: eine `const` überschreiben

🤔 **Vorhersage:** Welche Zeile wird Probleme machen? Wird `punkte` noch ausgegeben?
""")

code(r"""
const name = "Anna";
let punkte = 0;
punkte = 10;
console.log(punkte);
name = "Bernd";
console.log(name);
""", error=True)

md(r"""
**So lesen Sie die rote Meldung:**

1. **Nur die erste Zeile lesen:** `TypeError: Assignment to constant variable.` heißt übersetzt: *Zuweisung an eine unveränderliche Variable.* Die Meldung sagt genau, was los ist.
2. **Die Zeilennummer finden:** In der zweiten Zeile steht `<anonymous>:5:6`. Das bedeutet **Zeile 5**, Zeichen 6. Genau dort steht `name = "Bernd";`.
3. Alles darunter ist für Leute, die den Browser gebaut haben.

Beachten Sie auch: Die `10` wurde noch ausgegeben. Das Programm läuft Zeile für Zeile **bis zum Fehler** und bricht dort ab.

> **Kursregel: Im Zweifel `const`.**
> Das Programm sagt Ihnen, wenn es nicht geht. Dann ändern Sie es in `let`. Andersherum merkt es niemand.

> **`var` kommt nicht vor.** Sie werden es beim Nachschlagen im Netz finden. Das ist die alte, dritte Form. Wir nehmen die zwei aktuellen.

### ✏️ Ihre Aufgabe 2

1. Legen Sie **drei Variablen** an, die etwas über Sie erzählen, zum Beispiel Vorname, Wohnort, Lieblingszahl.
2. Geben Sie alle drei mit `console.log` aus.
3. Versuchen Sie, eine `const` zu überschreiben, und lesen Sie die Meldung.
4. Ändern Sie die Variable dann in `let`, und die Meldung verschwindet.
""")

code(r"""
// Ihre drei Variablen:


// ausgeben:

""")

# ---------------------------------------------------------------- 3 Datentypen
md(r"""
---
## 3 Die Datentypen

Drei Sorten von Werten. Der Unterschied steckt in den **Anführungszeichen**.
""")

code(r"""
const anzahl = 3;                 // Zahl, ohne Anführungszeichen
const frage = "Was ist HTML?";    // Text, mit Anführungszeichen
const umgedreht = false;          // Wahrheitswert: nur true oder false

console.log(anzahl);
console.log(frage);
console.log(umgedreht);
""")

md(r"""
`3` ist eine Zahl, mit der man rechnen kann. `"3"` ist ein Text, der zufällig aus einer Ziffer besteht.

### 🤔 Vorhersage: Was kommt heraus?

Schreiben Sie Ihre Antworten **vorher** auf. Danach ausführen und vergleichen.

| Ausdruck | Ihre Vorhersage |
|---|---|
| `3 + 4` | |
| `"3" + "4"` | |
| `"Hallo" + "Welt"` | |
| `"Hallo " + "Welt"` | |
| `3 + "4"` | |
""")

code(r"""
console.log(3 + 4);
console.log("3" + "4");
console.log("Hallo" + "Welt");
console.log("Hallo " + "Welt");
console.log(3 + "4");
""")

loesung("💡 Auflösung", r"""
| Ausdruck | Ergebnis | Warum |
|---|---|---|
| `3 + 4` | `7` | zwei Zahlen: es wird gerechnet |
| `"3" + "4"` | `34` | zwei Texte: sie werden aneinandergehängt |
| `"Hallo" + "Welt"` | `HalloWelt` | ohne Leerzeichen |
| `"Hallo " + "Welt"` | `Hallo Welt` | das Leerzeichen steht **im** ersten Text |
| `3 + "4"` | `34` | sobald ein Text beteiligt ist, wird angehängt |

**Kursregel:** Sobald Anführungszeichen im Spiel sind, heißt das Plus nicht mehr „rechne“, sondern „häng aneinander“.
""")

md(r"""
### Texte verbinden

Das brauchen Sie in der App dauernd. 🐞 In dieser Zelle steckt ein kleiner Fehler, der beim ersten Versuch fast immer passiert. Führen Sie sie aus, finden Sie ihn und reparieren Sie ihn.
""")

code(r"""
const name = "Anna";
const gruss = "Hallo" + name + "!";
console.log(gruss);
""")

loesung("💡 Lösung", r"""
Es fehlt das Leerzeichen. Die Ausgabe lautet `HalloAnna!`. Das Leerzeichen muss **innerhalb** der Anführungszeichen stehen:

```js
const gruss = "Hallo " + name + "!";
```
""")

md(r"""
### Leerzeichen entfernen mit `.trim()`

`.trim()` entfernt Leerzeichen am **Anfang** und am **Ende** eines Textes. Die eckigen Klammern in der Ausgabe machen sichtbar, wo der Text beginnt und endet.
""")

code(r"""
const eingabe = "  Anna  ";
console.log("[" + eingabe + "]");
console.log("[" + eingabe.trim() + "]");
""")

md(r"""
Klingt nach einer Kleinigkeit. Aber wenn jemand in Ihrer App versehentlich nur Leerzeichen eintippt, ist die Eingabe für das Programm **nicht leer**. In Abschnitt 5 bauen Sie damit eine Prüfung.

**Ausblick:** Es gibt noch zwei Sorten, und das sind die wichtigsten: eine für **viele Werte auf einmal** (Liste) und eine für **zusammengehörige Werte** (Objekt). Sie kommen in Abschnitt 6 und 7.
""")

# ---------------------------------------------------------------- 4 Funktionen
md(r"""
---
## 4 Funktionen

> **🚩 Der wichtigste Abschnitt des Moduls.** Nehmen Sie sich hier Zeit. Wer hier stolpert, versteht den Rest des Kurses nicht.

### Das Bild

```
         ┌──────────────────────────┐
"Anna" ──┤  begruessung(name)       ├──→ "Hallo Anna"
 hinein  │  macht immer dasselbe    │    heraus
         └──────────────────────────┘
```

Eine Funktion ist eine **Maschine**. Oben kommt etwas hinein, unten kommt etwas heraus, und dazwischen passiert immer dasselbe. Wie ein Fleischwolf: Was Sie hineingeben, entscheiden Sie. Was die Maschine tut, steht ein für alle Mal fest.

### Die erste Funktion
""")

code(r"""
function begruessung(name) {
  return "Hallo " + name;
}

console.log(begruessung("Anna"));
""")

md(r"""
| Teil | Was es bedeutet |
|---|---|
| `function` | „Achtung, jetzt kommt eine Maschine“ |
| `begruessung` | ihr Name, frei gewählt wie bei einer Variablen |
| `(name)` | was hineingeht: der **Parameter** |
| `{ … }` | was drin passiert |
| `return` | was herauskommt |
| `begruessung("Anna")` | die Maschine **anwerfen**: der **Aufruf**. Ohne ihn passiert nichts. |

Probieren Sie es mit Ihrem eigenen Namen: Ändern Sie `"Anna"` und führen Sie die Zelle erneut aus.

### 🐞 Der häufigste Fehler des ganzen Kurses

Führen Sie diese Zelle aus und achten Sie genau darauf, was passiert.
""")

code(r"""
function verabschiedung(name) {
  return "Tschüss " + name;
}

// console.log(verabschiedung("Anna"));
""")

md(r"""
**Nichts.** Keine Ausgabe, **keine Fehlermeldung**. Die Funktion wurde zwar aufgeschrieben, aber nie aufgerufen. Die letzte Zeile ist durch `//` auskommentiert.

Entfernen Sie die beiden Schrägstriche `//` und führen Sie die Zelle erneut aus.

> ## Merksatz: Eine Funktion aufschreiben heißt nicht, sie zu benutzen.

### Die drei Fragen an jede Funktion

```
1. Was geht hinein?      → die Klammer hinter dem Namen
2. Was kommt heraus?     → was hinter return steht
3. Wann passiert etwas?  → beim Aufruf, nicht beim Aufschreiben
```

🤔 Beantworten Sie die drei Fragen für diese Funktion, **bevor** Sie die Zelle ausführen:
""")

code(r"""
function doppelt(zahl) {
  return zahl * 2;
}

console.log(doppelt(5));
console.log(doppelt(21));
""")

loesung("💡 Die drei Antworten", r"""
1. **Hinein** geht eine Zahl: der Parameter `zahl`.
2. **Heraus** kommt eine Zahl: das Doppelte.
3. Etwas **passiert** beim Aufruf `doppelt(5)`, nicht beim Aufschreiben.

Das `*` ist das Malzeichen.
""")

md(r"""
Funktionen bleiben im Notebook bekannt, sobald ihre Zelle einmal gelaufen ist. Deshalb funktioniert auch diese Zelle:
""")

code(r"""
console.log(doppelt(100));
console.log(begruessung("Bernd"));
""")

md(r"""
### `return` gegen `console.log`

Diese Verwechslung kommt garantiert. Deshalb nehmen wir sie vorweg.

🤔 **Vorhersage:** Was steht am Ende in der Ausgabe? Schreiben Sie **jede** Zeile auf, in der richtigen Reihenfolge.
""")

code(r"""
function variante1(zahl) {
  return zahl * 2;
}

function variante2(zahl) {
  console.log(zahl * 2);
}

const a = variante1(5);
const b = variante2(5);
console.log(a);
console.log(b);
""")

loesung("💡 Auflösung", r"""
```
10          ← aus dem console.log IN variante2, schon beim Aufruf
10          ← aus console.log(a)
undefined   ← aus console.log(b)
```

Beide Funktionen zeigen eine 10 an. Aber nur `variante1` **gibt** die 10 auch zurück. `variante2` sagt sie nur laut und behält nichts. Deshalb ist `b` leer: `undefined`.

> **`console.log` ist Reden. `return` ist Abliefern.**
> Wenn Sie mit dem Ergebnis weiterarbeiten wollen, brauchen Sie `return`.

Merken Sie sich das Wort **`undefined`**. Es heißt fast immer: *Da war nichts, wo etwas hätte sein sollen.*
""")

md(r"""
### ✏️ Ihre Aufgabe 4a

Schreiben Sie die Funktion `ausrufen`. Sie bekommt einen Text und liefert ihn mit einem Ausrufezeichen am Ende **zurück**.
Aus `"Hallo"` wird `"Hallo!"`.

Die Zeilen mit `pruefe` darunter testen Ihre Funktion. Solange dort ❌ steht, stimmt noch etwas nicht.
""")

code(r"""
function ausrufen(text) {
  // Ihr Code hier
}

pruefe('ausrufen("Hallo") ergibt "Hallo!"', ausrufen("Hallo"), "Hallo!");
pruefe('ausrufen("Gut gemacht") ergibt "Gut gemacht!"', ausrufen("Gut gemacht"), "Gut gemacht!");
""")

loesung("💡 Lösung 4a", r"""
```js
function ausrufen(text) {
  return text + "!";
}
```

Steht bei Ihnen `bekommen: undefined`? Dann fehlt das `return`.
""")

md(r"""
### ✏️ Ihre Aufgabe 4b: eine eigene Maschine

Schreiben Sie eine **eigene** Funktion mit **einem** Parameter und einem `return`. Was sie tut, entscheiden Sie. Ideen: `verdreifacht(zahl)`, `alsFrage(text)` (hängt ein `?` an), `minutenInSekunden(minuten)`.

Prüfen Sie zum Schluss genau eine Sache: **Wird Ihre Funktion auch aufgerufen?**
""")

code(r"""
// Ihre Funktion:


// Ihr Aufruf mit Ausgabe:

""")

md(r"""
### ✏️ Zusatzaufgabe 4c (für Schnellere)

Eine Funktion kann auch **zwei** Parameter haben, getrennt durch ein Komma. Schreiben Sie `kartenTitel(nummer, frage)`, die zum Beispiel aus `1` und `"Was ist HTML?"` den Text `"Karte 1: Was ist HTML?"` macht.
""")

code(r"""
function kartenTitel(nummer, frage) {
  // Ihr Code hier
}

pruefe("Karte 1", kartenTitel(1, "Was ist HTML?"), "Karte 1: Was ist HTML?");
pruefe("Karte 7", kartenTitel(7, "Was ist CSS?"), "Karte 7: Was ist CSS?");
""")

loesung("💡 Lösung 4c", r"""
```js
function kartenTitel(nummer, frage) {
  return "Karte " + nummer + ": " + frage;
}
```

Die Zahl `nummer` wird beim Verbinden automatisch zu Text, weil ein Text beteiligt ist. Erinnern Sie sich an `3 + "4"`?
""")

# ---------------------------------------------------------------- 5 if
md(r"""
---
## 5 Entscheidungen mit `if`

Wenn das in der runden Klammer stimmt, läuft der erste Block. Sonst der zweite. Der `else`-Teil ist freiwillig.
""")

code(r"""
let punkte = 12;

if (punkte > 10) {
  console.log("geschafft");
} else {
  console.log("weiter üben");
}
""")

md(r"""
Ändern Sie `12` in `5` und führen Sie die Zelle erneut aus. Sie sehen den anderen Zweig.

| Zeichen | Bedeutung |
|---|---|
| `>` | größer als |
| `<` | kleiner als |
| `===` | ist gleich |
| `!==` | ist ungleich |

> **Kursregel: Immer drei Gleichheitszeichen, nie zwei.**
> `===` vergleicht, `=` weist zu. Ohne Ausnahme. (Es gibt auch `==`, das arbeitet ungenauer und kommt im Kurs nicht vor.)

### 🐞 Absichtlicher Fehler: `=` statt `===`

🤔 **Vorhersage:** `punkte` ist 5. Erscheint „genau zehn“?
""")

code(r"""
let punkte = 5;

if (punkte = 10) {
  console.log("genau zehn");
}

console.log("punkte ist jetzt " + punkte);
""")

md(r"""
„genau zehn“ erscheint, und `punkte` ist plötzlich 10. **Ohne Fehlermeldung.**

Ein Gleichheitszeichen **legt in die Schublade**. Drei Gleichheitszeichen **fragen, was drin ist**. Reparieren Sie die Zelle: Schreiben Sie `===`, führen Sie sie erneut aus, und nichts erscheint mehr außer der letzten Zeile.

### `if` und `return` zusammen
""")

code(r"""
function bewertung(anzahl) {
  if (anzahl > 10) {
    return "schon ein guter Stapel";
  } else {
    return "da geht noch mehr";
  }
}

console.log(bewertung(3));
console.log(bewertung(25));
""")

md(r"""
### 🤔 Der Grenzfall

Was liefert `bewertung(10)`? Erst überlegen, dann ausführen.
""")

code(r"""
console.log(bewertung(10));
""")

loesung("💡 Auflösung", r"""
`"da geht noch mehr"`: Der `else`-Zweig greift, weil `>` **echt größer** bedeutet. 10 ist nicht größer als 10.

Wer die 10 einschließen will, schreibt die Bedingung anders, zum Beispiel `anzahl > 9`.

**Gewohnheit für immer:** Bei jeder Bedingung mit `>` oder `<` einmal fragen, was **am Rand** passiert.
""")

md(r"""
### Vorgeschmack auf K4: Ist die Eingabe leer?

In K4 tippen Sie Fragen in ein Eingabefeld. Eine Karte ohne Frage soll nicht angelegt werden. Hier kommen `.trim()`, `===` und `if` zusammen:
""")

code(r"""
function istLeer(text) {
  if (text.trim() === "") {
    return true;
  } else {
    return false;
  }
}

console.log(istLeer(""));
console.log(istLeer("     "));
console.log(istLeer("Was ist CSS?"));
""")

md(r"""
### 🔍 Blick hinter die Kulissen: die Prüffunktion

Erinnern Sie sich an `pruefe(...)` aus den Aufgaben? Sie stammt aus der Vorbereitungszelle. Jetzt können Sie sie lesen, denn sie besteht nur aus Dingen, die Sie kennen:

```js
function pruefe(beschreibung, ergebnis, erwartet) {
  if (ergebnis === erwartet) {
    console.log("✅ " + beschreibung);
  } else {
    console.log("❌ " + beschreibung);
    console.log("     erwartet: " + erwartet);
    console.log("     bekommen: " + ergebnis);
  }
}
```

Stellen Sie die drei Fragen: Was geht hinein? Was kommt heraus? (Achtung, Falle!) Wann passiert etwas?

### ✏️ Ihre Aufgabe 5

Schreiben Sie `antwortPruefen(eingabe, richtig)`. Sie liefert `"richtig"`, wenn die Eingabe **ohne Leerzeichen am Rand** genau der richtigen Antwort entspricht, sonst `"falsch"`.
""")

code(r"""
function antwortPruefen(eingabe, richtig) {
  // Ihr Code hier
}

pruefe("genau getroffen", antwortPruefen("HTML", "HTML"), "richtig");
pruefe("Leerzeichen am Rand zählen nicht", antwortPruefen("  HTML ", "HTML"), "richtig");
pruefe("falsche Antwort", antwortPruefen("CSS", "HTML"), "falsch");
""")

loesung("💡 Lösung 5", r"""
```js
function antwortPruefen(eingabe, richtig) {
  if (eingabe.trim() === richtig) {
    return "richtig";
  } else {
    return "falsch";
  }
}
```

Und die Falle aus dem Blick hinter die Kulissen: `pruefe` hat **kein** `return`. Sie redet nur (`console.log`), sie liefert nichts ab.
""")

# ---------------------------------------------------------------- 6 Listen
md(r"""
---
## 6 Listen

Eine Liste ist eine Schublade mit **mehreren Fächern** statt einem. Eckige Klammern, Werte mit Komma dazwischen.
""")

code(r"""
const farben = ["rot", "gruen", "blau"];

console.log(farben.length);
console.log(farben[0]);
""")

md(r"""
### Der Nullpunkt

Zählen Sie einmal laut mit: **null, eins, zwei**.

```
farben[0]      →  "rot"
farben[1]      →  "gruen"
farben[2]      →  "blau"
farben.length  →  3
```

Drei Einträge, aber der letzte hat die Nummer **zwei**. Die Nummer eines Fachs heißt **Index**.

🤔 **Vorhersage:** Was geben die drei Zeilen aus?
""")

code(r"""
const farben = ["rot", "gruen", "blau"];

console.log(farben[1]);
console.log(farben[2]);
console.log(farben[3]);
""")

loesung("💡 Auflösung", r"""
`gruen`, `blau`, `undefined`.

Ein Fach Nummer 3 gibt es nicht. Antwort: `undefined`, also *da ist nichts*. Das ist **kein** Fehler, nur eine leere Antwort.

Den letzten Eintrag einer Liste erreichen Sie immer so, auch wenn Sie die Anzahl nicht kennen:

```js
farben[farben.length - 1]
```
""")

md(r"""
### Ergänzen mit `.push()`

`push` hängt **hinten** an. Der Punkt heißt: *Diese Sache kann etwas*, wie ein Knopf an einem Gerät.
""")

code(r"""
const farben = ["rot", "gruen", "blau"];

farben.push("gelb");
console.log(farben.length);
console.log(farben);
""")

md(r"""
> **Warum geht `push` bei einer `const`?**
> Weil sich die Schublade nicht ändert, nur ihr Inhalt. `const` verbietet, eine **andere** Liste hineinzulegen, nicht, die vorhandene zu füllen. Merken reicht, begründen müssen Sie es nicht.

### Durchlaufen mit `for … of`
""")

code(r"""
const farben = ["rot", "gruen", "blau"];

for (const farbe of farben) {
  console.log(farbe);
}
""")

md(r"""
Lesen Sie das wörtlich: **„Für jede Farbe aus den Farben, tu Folgendes.“** Der Name `farbe` ist frei gewählt. Er gilt nur innerhalb der geschweiften Klammern und steht in jedem Durchgang für einen anderen Eintrag.

> **Namensregel: Einzahl aus der Mehrzahl.**
> `for (const farbe of farben)`, `for (const karte of karten)`. Wer das durchhält, liest den eigenen Code später noch.

> Die ältere Form `for (let i = 0; i < liste.length; i++)` werden Sie beim Nachschlagen finden. Sie kann mehr, das Mehr brauchen wir nicht.

### ✏️ Ihre Aufgabe 6

1. Füllen Sie die Liste `faecher` mit **drei** Fächern, die Sie gerade lernen oder lernen möchten.
2. Hängen Sie mit `push` ein **viertes** an.
3. Geben Sie mit einer `for … of`-Schleife jedes Fach so aus: `Ich lerne: Mathe`
""")

code(r"""
const faecher = [];

// push:


// Schleife:


pruefe("Die Liste hat 4 Einträge", faecher.length, 4);
""")

loesung("💡 Lösung 6 (ein Beispiel)", r"""
```js
const faecher = ["Mathe", "Englisch", "Netzwerke"];

faecher.push("JavaScript");

for (const fach of faecher) {
  console.log("Ich lerne: " + fach);
}
```
""")

# ---------------------------------------------------------------- 7 Objekte
md(r"""
---
## 7 Objekte

```
Liste:   Regal mit NUMMERIERTEN Fächern    farben[0]
Objekt:  Regal mit BESCHRIFTETEN Fächern   karte.frage
```

Geschweifte Klammern, innen Paare aus **Beschriftung** und **Wert**, getrennt durch einen Doppelpunkt. Ein beschriftetes Fach heißt **Feld**.
""")

code(r"""
const karte = {
  frage: "Was ist HTML?",
  antwort: "Die Struktur einer Seite"
};

console.log(karte.frage);
console.log(karte.antwort);
""")

md(r"""
### 🐞 Die Verwechslung

🤔 **Vorhersage:** Zwei Zeilen sind richtig, zwei sind vertauscht. Welche liefern etwas, welche nicht?
""")

code(r"""
const farben = ["rot", "gruen", "blau"];
const karte = { frage: "Was ist HTML?", antwort: "Die Struktur einer Seite" };

console.log(farben[0]);      // Liste:  eckige Klammer, Nummer
console.log(karte.frage);    // Objekt: Punkt, Name
console.log(karte[0]);       // vertauscht
console.log(farben.frage);   // vertauscht
""")

md(r"""
Eckige Klammer und Zahl bei der **Liste**. Punkt und Name beim **Objekt**. Vertauscht gibt es `undefined`, und Sie wissen inzwischen, was das heißt.

### Felder ändern und ergänzen
""")

code(r"""
const karte = {
  frage: "Was ist HTML?",
  antwort: "Die Struktur einer Seite"
};

karte.antwort = "Die Struktur";   // vorhandenes Feld ändern
karte.gezeigt = false;            // neues Feld anlegen

console.log(karte);
""")

md(r"""
Ein Feld ändern Sie mit dem Gleichheitszeichen, wie bei einer Variablen. Beschriften Sie ein Fach, das es noch nicht gibt, wird es angelegt. Auch das ist bei `const` erlaubt, genau wie `push` bei der Liste.

### Verschachtelt lesen

Objekte kann man ineinanderlegen. Sie müssen das heute nicht selbst schreiben, sollen es aber einmal **gelesen** haben:
""")

code(r"""
const stapel = {
  titel: "Webtechniken",
  karte: { frage: "Was ist CSS?", antwort: "Das Aussehen" }
};

console.log(stapel.titel);
console.log(stapel.karte.frage);
""")

md(r"""
### ✏️ Ihre Aufgabe 7

1. Legen Sie ein Objekt mit **drei Feldern** an, das etwas aus Ihrem Leben beschreibt: Ihr Fahrrad, Ihr Lieblingsessen, Ihr Haustier …
2. Geben Sie **zwei** Felder einzeln aus.
3. Ändern Sie ein Feld, legen Sie ein **viertes** an und geben Sie das ganze Objekt aus.
""")

code(r"""
// Ihr Objekt:


// zwei Felder ausgeben:


// ändern, ergänzen, ganz ausgeben:

""")

md(r"""
### 🤔 Liste oder Objekt?

Entscheiden Sie für jede Zeile, bevor Sie die Lösung aufklappen.

| Was gespeichert werden soll | Liste oder Objekt? |
|---|---|
| die Namen aller Wochentage | |
| Frage und Antwort einer Karte | |
| alle bisher angelegten Karten | |
| Name, Ort und Alter einer Person | |
| die letzten fünf Suchbegriffe | |
""")

loesung("💡 Auflösung", r"""
| Was gespeichert werden soll | Antwort | Begründung |
|---|---|---|
| Wochentage | Liste | gleichartige Dinge, Reihenfolge zählt |
| Frage und Antwort | Objekt | verschiedene Angaben, jede braucht einen Namen |
| alle Karten | Liste | viele gleichartige Dinge |
| Name, Ort, Alter | Objekt | verschiedene Angaben zu einer Sache |
| letzte fünf Suchbegriffe | Liste | gleichartig, Reihenfolge zählt |

**Faustregel:** Gleichartige Dinge in einer Reihe: **Liste**. Verschiedene Angaben zu einer Sache: **Objekt**.

Und jetzt kommt der Clou: „alle Karten“ ist eine Liste, „eine Karte“ ist ein Objekt. Zusammen ergibt das eine **Liste aus Objekten**.
""")

# ---------------------------------------------------------------- 8 Datenbestand
md(r"""
---
## 8 Beides zusammen: der Datenbestand

Listen und Objekte zusammen ergeben das, worauf der ganze Kurs hinausläuft: den **Datenbestand Ihrer Lernkarten-App**.
""")

code(r"""
const karten = [
  { frage: "Was ist HTML?", antwort: "Die Struktur einer Seite" },
  { frage: "Was ist CSS?", antwort: "Das Aussehen einer Seite" },
  { frage: "Was ist eine id?", antwort: "Der Name eines Elements" }
];

for (const karte of karten) {
  console.log(karte.frage);
}
""")

md(r"""
**Lesen Sie die Struktur laut vor:** „Eine Liste, darin drei Objekte, jedes mit den Feldern Frage und Antwort.“

```
karten            → die ganze Liste
karten.length     → wie viele
karten[0]         → die erste Karte (ein Objekt)
karten[0].frage   → deren Frage (ein Text)
```

### 🤔 Vorhersage: Was kommt heraus, und welche Sorte ist es?

| Ausdruck | Was kommt heraus? | Sorte |
|---|---|---|
| `karten.length` | | |
| `karten[1]` | | |
| `karten[1].antwort` | | |
""")

code(r"""
const karten = [
  { frage: "Was ist HTML?", antwort: "Die Struktur einer Seite" },
  { frage: "Was ist CSS?", antwort: "Das Aussehen einer Seite" },
  { frage: "Was ist eine id?", antwort: "Der Name eines Elements" }
];

console.log(karten.length);
console.log(karten[1]);
console.log(karten[1].antwort);
""")

loesung("💡 Auflösung", r"""
| Ausdruck | Ergebnis | Sorte |
|---|---|---|
| `karten.length` | `3` | Zahl |
| `karten[1]` | die **zweite** Karte, komplett | Objekt |
| `karten[1].antwort` | `Das Aussehen einer Seite` | Text |

**Die letzte Zeile ist der Verständnistest des ganzen Moduls.** In Worten:
*„Nimm aus der Liste das Fach mit der Nummer eins, das ist ein Objekt, und hole daraus das beschriftete Fach `antwort`.“*

Wer `karten[1]` für die erste Karte gehalten hat: zurück zum Nullpunkt in Abschnitt 6.
""")

md(r"""
### So sieht `app.js` am Ende von K3 aus

Die nächste Zelle enthält, was am Ende dieses Moduls in Ihrer `app.js` steht: den Datenbestand, eine Variable für die gerade angezeigte Karte und zwei Funktionen. Darunter wird alles getestet.

Jede Karte, die Sie später in der App anlegen, wird ein weiteres Objekt in dieser Liste.
""")

code(r"""
// ---------- So steht es am Ende von K3 in app.js ----------
const karten = [
  { frage: "Was ist HTML?", antwort: "Die Struktur einer Seite" },
  { frage: "Was ist CSS?", antwort: "Das Aussehen einer Seite" },
  { frage: "Was ist eine id?", antwort: "Der Name eines Elements" }
];

let aktuelleKarte = 0;

function anzahlKarten() {
  return karten.length;
}

function karteAnlegen(frage, antwort) {
  const neueKarte = { frage: frage, antwort: antwort };
  karten.push(neueKarte);
  return neueKarte;
}

// ---------- Ausprobieren ----------
console.log("Karten vorher: " + anzahlKarten());
karteAnlegen("Was ist eine Funktion?", "Eine Maschine mit rein und raus");
console.log("Karten nachher: " + anzahlKarten());

console.log("Angezeigt wird: " + karten[aktuelleKarte].frage);
aktuelleKarte = aktuelleKarte + 1;     // das wird in K4 der Knopf „Nächste“ tun
console.log("Angezeigt wird: " + karten[aktuelleKarte].frage);
""")

md(r"""
> **Warum ist `aktuelleKarte` ein `let`?**
> Weil sich die Nummer der angezeigten Karte dauernd ändert, sobald der Knopf „Nächste“ funktioniert. Genau für diesen Fall gibt es `let`.

**Probieren Sie selbst:** Legen Sie in der Zelle oben mit `karteAnlegen(...)` eine weitere, eigene Karte an und lassen Sie sich die neue Anzahl ausgeben.
""")

# ---------------------------------------------------------------- 9 Fehler
md(r"""
---
## 9 🐞 Absichtlicher Fehler: `undefined` und die rote Meldung

🤔 **Vorhersage:** Die Liste hat drei Karten. Was passiert in den beiden letzten Zeilen?
""")

code(r"""
const karten = [
  { frage: "Was ist HTML?", antwort: "Die Struktur einer Seite" },
  { frage: "Was ist CSS?", antwort: "Das Aussehen einer Seite" },
  { frage: "Was ist eine id?", antwort: "Der Name eines Elements" }
];

console.log(karten[5]);
console.log(karten[5].frage);
""", error=True)

md(r"""
**Erste Zeile:** `undefined`. Sie fragt nach einem Fach, das es nicht gibt. Antwort: *da ist nichts*. Kein Fehler, nur eine leere Antwort.

**Zweite Zeile:** eine **echte Fehlermeldung**. Sie fragt dieses Nichts nach seiner Frage, und da bricht das Programm ab, denn Nichts hat keine Frage.

**Lesen Sie die Meldung wie gelernt:**

1. Erste Zeile: `TypeError: Cannot read properties of undefined (reading 'frage')`, übersetzt: *Kann von `undefined` nichts lesen (gesucht war `frage`).* Firefox schreibt kürzer: `karten[5] is undefined`.
2. Zeilennummer: Suchen Sie in der zweiten Zeile `<anonymous>:` und die Zahl dahinter. Welche Zeile ist es? Schalten Sie mit **Esc** und **Umschalt + L** die Zeilennummern ein und zählen Sie nach.
3. **Reparieren:** Ändern Sie beide Male die `5` so, dass die **letzte** Karte ausgegeben wird.
""")

loesung("💡 Lösung", r"""
Die Meldung nennt **Zeile 8**. Der letzte Index bei drei Karten ist `2`:

```js
console.log(karten[2]);
console.log(karten[2].frage);
```

Oder, unabhängig von der Anzahl: `karten[karten.length - 1].frage`
""")

# ---------------------------------------------------------------- 10 Fehlerjagd
md(r"""
---
## 10 Fehlerjagd

In jeder der fünf Zellen steckt **genau ein** Fehler. Führen Sie die Zelle aus, beschreiben Sie, was Sie sehen, und reparieren Sie sie. Die Diagnosetabelle in Abschnitt 11 hilft, falls Sie nicht weiterkommen.

**a)** Erwartet wird die Ausgabe `10`.
""")

code(r"""
function doppelt(zahl) {
  zahl * 2;
}

console.log(doppelt(5));
""")

md(r"""
**b)** Erwartet wird die Ausgabe `10`.
""")

code(r"""
function doppelt(zahl) {
  return zahl * 2;
}
""")

md(r"""
**c)** Erwartet wird: keine Ausgabe, weil `punkte` 5 ist.
""")

code(r"""
let punkte = 5;

if (punkte = 10) {
  console.log("genau zehn");
}
""")

md(r"""
**d)** Erwartet wird die Ausgabe `Bernd`.
""")

code(r"""
const name = "Anna";
name = "Bernd";
console.log(name);
""", error=True)

md(r"""
**e)** Erwartet wird die Ausgabe `blau`.
""")

code(r"""
const farben = ["rot", "gruen", "blau"];
console.log(farben[3]);
""")

loesung("💡 Lösungen zur Fehlerjagd", r"""
| | Was Sie sehen | Ursache | Reparatur |
|---|---|---|---|
| a) | `undefined` | `return` fehlt | `return zahl * 2;` |
| b) | gar nichts | Funktion nie aufgerufen | `console.log(doppelt(5));` ergänzen |
| c) | „genau zehn“ | `=` statt `===` | `if (punkte === 10)` |
| d) | rote Meldung | Zuweisung an eine `const` | `let name = "Anna";` |
| e) | `undefined` | Index zu groß | `farben[2]` |

**Der Zusammenhang:** a), b) und e) enden in `undefined` oder Stille. Drei verschiedene Ursachen, fast dasselbe Erscheinungsbild. Und c) ist der gemeinste Fall: Das Programm läuft, tut aber etwas anderes. Genau deshalb gibt es die Diagnosetabelle.
""")

# ---------------------------------------------------------------- 11 Diagnosetabelle
md(r"""
---
## 11 Die Diagnosetabelle

Sie trägt bis zum Ende des Kurses. Drucken Sie sie aus oder halten Sie das Merkblatt bereit.

| Was zu sehen ist | Was das meistens heißt |
|---|---|
| **gar nichts**, keine Meldung | Funktion nie aufgerufen |
| **`undefined`** | da war nichts, wo etwas sein sollte: `return` vergessen? Index zu groß? Feldname falsch? |
| **rote Meldung** | erste Zeile lesen, Zeilennummer merken, dort anfangen |

| Weitere typische Fälle | Ursache |
|---|---|
| `if` verhält sich unlogisch | `=` statt `===` |
| Zugriff liefert nichts | `liste.feld` und `objekt[0]` verwechselt |
| Änderung wirkt nicht (App) | nach dem Speichern nicht neu geladen |
| Ausgabe nicht auffindbar (App) | im Terminal gesucht statt in der Konsole |
| Konsole zeigt nach jedem Befehl `undefined` (App) | normales Verhalten, ignorieren |

> **Bei einer Fehlermeldung nur die erste Zeile lesen.** Der Rest darunter ist für Leute, die den Browser gebaut haben.
""")

# ---------------------------------------------------------------- 12 Werkstatt
md(r"""
---
## 12 Lernkarten-Werkstatt

Zum Abschluss schreiben Sie vier kleine Funktionen, die Ihre App in K4 gut gebrauchen kann. Jede Zelle bringt den Datenbestand selbst mit.

### ✏️ Aufgabe A: eine Karte als Text

`karteAlsText(karte)` bekommt **ein Objekt** und liefert einen Text in dieser Form:
`Was ist HTML? → Die Struktur einer Seite`
""")

code(r"""
function karteAlsText(karte) {
  // Ihr Code hier
}

const testkarte = { frage: "Was ist HTML?", antwort: "Die Struktur einer Seite" };
pruefe("Karte als Text", karteAlsText(testkarte), "Was ist HTML? → Die Struktur einer Seite");
""")

loesung("💡 Lösung A", r"""
```js
function karteAlsText(karte) {
  return karte.frage + " → " + karte.antwort;
}
```
""")

md(r"""
### ✏️ Aufgabe B: alle Fragen nummeriert ausgeben

`alleFragenAusgeben(liste)` geht mit `for … of` durch die Liste und gibt jede Frage mit Nummer aus. Erwartete Ausgabe:

```
1. Was ist HTML?
2. Was ist CSS?
3. Was ist eine id?
```

Tipp: Sie brauchen eine Zählvariable, die vor der Schleife bei `1` beginnt und in jedem Durchgang um eins wächst. `const` oder `let`?
""")

code(r"""
const karten = [
  { frage: "Was ist HTML?", antwort: "Die Struktur einer Seite" },
  { frage: "Was ist CSS?", antwort: "Das Aussehen einer Seite" },
  { frage: "Was ist eine id?", antwort: "Der Name eines Elements" }
];

function alleFragenAusgeben(liste) {
  // Ihr Code hier
}

alleFragenAusgeben(karten);
""")

loesung("💡 Lösung B", r"""
```js
function alleFragenAusgeben(liste) {
  let nummer = 1;
  for (const karte of liste) {
    console.log(nummer + ". " + karte.frage);
    nummer = nummer + 1;
  }
}
```

`nummer` muss ein `let` sein, weil sich ihr Inhalt in jedem Durchgang ändert. Mit `const` gibt es die bekannte Meldung `Assignment to constant variable.`
""")

md(r"""
### ✏️ Aufgabe C: wie gut ist der Stapel?

`stapelBewertung(liste)` liefert `"schon ein guter Stapel"`, wenn die Liste **mehr als 10** Karten hat, sonst `"da geht noch mehr"`.
""")

code(r"""
const karten = [
  { frage: "Was ist HTML?", antwort: "Die Struktur einer Seite" },
  { frage: "Was ist CSS?", antwort: "Das Aussehen einer Seite" },
  { frage: "Was ist eine id?", antwort: "Der Name eines Elements" }
];

function stapelBewertung(liste) {
  // Ihr Code hier
}

pruefe("3 Karten", stapelBewertung(karten), "da geht noch mehr");
pruefe("leerer Stapel", stapelBewertung([]), "da geht noch mehr");
pruefe("12 Karten", stapelBewertung([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]), "schon ein guter Stapel");
""")

loesung("💡 Lösung C", r"""
```js
function stapelBewertung(liste) {
  if (liste.length > 10) {
    return "schon ein guter Stapel";
  } else {
    return "da geht noch mehr";
  }
}
```

Fällt Ihnen etwas auf? Das ist die Funktion `bewertung` aus Abschnitt 5, nur dass sie jetzt die **Liste** bekommt und selbst zählt.
""")

md(r"""
### ✏️ Aufgabe D (für Schnellere): der Knopf „Nächste“

In K4 soll ein Knopf zur nächsten Karte blättern. Nach der letzten Karte geht es wieder von vorn los.

`naechsteNummer(aktuelle, anzahl)` bekommt die Nummer der aktuellen Karte und die Anzahl aller Karten und liefert die Nummer der **nächsten** Karte. Bei 3 Karten: aus 0 wird 1, aus 1 wird 2, aus **2 wird wieder 0**.
""")

code(r"""
function naechsteNummer(aktuelle, anzahl) {
  // Ihr Code hier
}

pruefe("von 0 nach 1", naechsteNummer(0, 3), 1);
pruefe("von 1 nach 2", naechsteNummer(1, 3), 2);
pruefe("nach der letzten wieder von vorn", naechsteNummer(2, 3), 0);
pruefe("bei nur einer Karte bleibt es 0", naechsteNummer(0, 1), 0);
""")

loesung("💡 Lösung D", r"""
```js
function naechsteNummer(aktuelle, anzahl) {
  if (aktuelle === anzahl - 1) {
    return 0;
  } else {
    return aktuelle + 1;
  }
}
```

Die letzte Karte hat den Index `anzahl - 1`, das ist wieder der Nullpunkt. In K4 sehen Sie dafür eine kürzere Schreibweise, die dasselbe tut.
""")

# ---------------------------------------------------------------- 13 Abschluss
md(r"""
---
## 13 Checkliste und Ausblick auf K4

Haken Sie ab, was Sie geschafft haben (Doppelklick auf diese Zelle, dann `[ ]` zu `[x]` ändern):

- [ ] Ich weiß, wo in der App die Konsole ist und wo im Notebook die Ausgabe erscheint
- [ ] Ich habe Variablen mit `const` und `let` angelegt und die `const`-Fehlermeldung gelesen
- [ ] Ich unterscheide Zahl, Text und Wahrheitswert und habe `.trim()` benutzt
- [ ] Ich habe mindestens drei eigene Funktionen geschrieben **und aufgerufen**
- [ ] Ich kann den Unterschied zwischen `return` und `console.log` erklären
- [ ] Ich habe eine Funktion mit `if` und `return` geschrieben
- [ ] Ich habe eine Liste angelegt, ergänzt, gezählt und durchlaufen
- [ ] Ich habe ein Objekt angelegt, Felder geändert und ergänzt
- [ ] Ich kann `karten[0].frage` in Worten erklären
- [ ] Ich habe die Diagnosetabelle angewendet: `undefined` und rote Meldung gedeutet

### Wie geht es weiter?

In **K4 „JavaScript im Fenster“** bekommt Ihre App endlich wieder etwas Sichtbares: Sie holen Elemente aus der `index.html` ins JavaScript, reagieren auf Klicks und schreiben Karten ins Fenster. Alles, was Sie dafür brauchen, haben Sie hier geübt: Funktionen, `if`, die Liste `karten` und die Variable `aktuelleKarte`.

> **Vorbereitung für K4:** Legen Sie die Liste Ihrer `id`s aus K1 bereit. Die brauchen Sie dort in der ersten Viertelstunde.

**Zum Nachschlagen:** K3 Merkblatt · K3 Übungsblatt · Anhang Sprachumfang JavaScript
""")

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

# nbformat 4.5 verlangt eine id pro Zelle
for i, c in enumerate(nb["cells"]):
    c["id"] = f"m03-{i:03d}"
    c["source"] = c["source"].splitlines(keepends=True)

with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(len(cells), "Zellen geschrieben")
