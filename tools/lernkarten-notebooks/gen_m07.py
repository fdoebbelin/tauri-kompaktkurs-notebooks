"""Erzeugt content/M07_Als_Anwendung_ausliefern.ipynb für die JupyterLite-Seite."""
import json
import pathlib
import sys

HIER = pathlib.Path(__file__).parent

# Helfer, Dateien und Bausteine aus K4 und K5 übernehmen
_m05 = (HIER / "gen_m05.py").read_text(encoding="utf-8")
exec(_m05.split("\n# ================================================================== Einstieg\n")[0])

K5_TEILE = [DATEN_LEER, LISTE, SPEICHERN, LADEN, NEU_K5, UMDREHEN, WEITER, START_LADEN]
STANDARD_JS = "// app.js\n" + "\n\n".join(t.strip("\n") for t in K5_TEILE)

DESKTOP = """[Desktop Entry]
Name=Lernkarten
Comment=Karteikarten zum Lernen, selbst gebaut im Kompaktkurs
Exec=lernkarten
Icon=de.metarow.Lernkarten
Terminal=false
Type=Application
Categories=Education;"""

METAINFO = """<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>de.metarow.Lernkarten</id>
  <name>Lernkarten</name>
  <summary>Karteikarten zum Lernen, selbst gebaut im Kompaktkurs</summary>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>MIT</project_license>
  <description>
    <p>Karten mit Frage und Antwort anlegen, durchblättern und umdrehen.
       Die Karten bleiben in einer Datei gespeichert.</p>
  </description>
  <launchable type="desktop-id">de.metarow.Lernkarten.desktop</launchable>
  <releases>
    <release version="0.1.0" date="2026-11-27"/>
  </releases>
</component>"""

YML = """id: de.metarow.Lernkarten
runtime: org.gnome.Platform
runtime-version: '50'
sdk: org.gnome.Sdk
sdk-extensions:
  - org.freedesktop.Sdk.Extension.rust-stable
command: lernkarten

finish-args:
  - --socket=wayland
  - --socket=fallback-x11
  - --share=ipc
  - --device=dri

build-options:
  append-path: /usr/lib/sdk/rust-stable/bin
  build-args:
    - --share=network          # nur lokal: cargo lädt beim Bauen Bausteine aus dem Netz
  env:
    CARGO_HOME: /run/build/lernkarten/cargo

modules:
  - name: lernkarten
    buildsystem: simple
    sources:
      - type: dir
        path: .
    build-commands:
      - cargo build --release --manifest-path src-tauri/Cargo.toml
      - install -Dm755 src-tauri/target/release/lernkarten /app/bin/lernkarten
      - install -Dm644 de.metarow.Lernkarten.desktop /app/share/applications/de.metarow.Lernkarten.desktop
      - install -Dm644 de.metarow.Lernkarten.metainfo.xml /app/share/metainfo/de.metarow.Lernkarten.metainfo.xml
      - install -Dm644 src-tauri/icons/128x128.png /app/share/icons/hicolor/128x128/apps/de.metarow.Lernkarten.png"""

SETUP = (HIER / "m07_setup.js").read_text(encoding="utf-8")
SETUP = SETUP.replace("__HTML__", json.dumps(INDEX_HTML, ensure_ascii=False))
SETUP = SETUP.replace("__CSS__", json.dumps(STYLE_CSS, ensure_ascii=False))
SETUP = SETUP.replace("__JS__", json.dumps(STANDARD_JS, ensure_ascii=False))
SETUP = SETUP.replace("__DESKTOP__", json.dumps(DESKTOP, ensure_ascii=False))

BAUEN = "flatpak run org.flatpak.Builder --force-clean --repo=repo build-dir de.metarow.Lernkarten.yml"
WO_BIN_ICH = 'if ("/run/.toolboxenv" | path exists) { print "im Container" } else { print "auf dem Host" }'


def terminal(*zeilen):
    code("# Terminal\n" + "\n".join(zeilen))


# ================================================================== Einstieg
md(r"""
# M7 – Als Anwendung ausliefern

*Begleit-Notebook zu Modul **K7 „Als Anwendung ausliefern“** im Kompaktkurs „Vom Web zur Desktop-App mit Tauri“*

Am Ende steht **Ihre eigene Anwendung im Anwendungsmenü** und startet ohne Editor und ohne Terminal. Das ist der Abschluss des Kurses.

Im Kurs ist K7 eine **Mitmach-Vorführung**: Alle Dateien sind vorbereitet, Sie tippen die Befehle mit und schauen zu, was passiert. Dieses Notebook ist die **Generalprobe** davor oder die **Wiederholung** danach. Hier können Sie jeden Befehl gefahrlos ausprobieren, auch die falschen.

## 🎯 Das können Sie am Ende

- den Unterschied zwischen **Entwicklungslauf** und **installierter Anwendung** benennen
- die drei Zusatzdateien in je einem Satz erklären und den eigenen Anzeigenamen eintragen
- das Flatpak **auf dem Host** bauen, installieren und aus dem Menü starten
- erklären, warum die installierte App ihre **eigenen Daten** hat, und das nicht für einen Fehler halten
- die Berechtigungen anzeigen und vorlesen
- den Weg von Ihrer `index.html` bis zum Eintrag im Anwendungsmenü beschreiben

## 🧭 Inhalt

0. Vorbereitung
1. Was bisher lief: der Entwicklungslauf
2. Die drei Zusatzdateien
3. Bauen
4. Installieren und starten
5. Was jetzt anders ist
6. Eine neue Fassung ausliefern
7. Ein Bundle zum Mitnehmen
8. Fehlerjagd
9. Abschluss: der ganze Weg, Rückblick und Checkliste
""")

md(r"""
## So funktioniert dieses Notebook

> **📌 Ehrlicher Hinweis: Hier wird nichts wirklich gebaut.**
> Flatpak, Container und Anwendungsmenü gibt es nur auf Ihrem Rechner. Die Vorbereitungszelle bildet sie nach, so gut es im Browser geht. Die Befehle sind **genau die aus dem Kurs**, die Antworten sind den echten nachempfunden.

| Zelle beginnt mit | Was passiert |
|---|---|
| `# Terminal` | ein **Übungs-Terminal** (Nushell). Jede weitere Zeile ist ein Befehl. Es merkt sich, ob Sie im Container oder auf dem Host sind, und was schon gebaut und installiert ist. |
| `# Anwendungsmenü` | zeigt das **Anwendungsmenü**. Ist Ihre App installiert, startet ein Klick sie. |
| `[Desktop Entry]` | speichert Ihre `.desktop`-Datei |

| | Im Notebook | In echt |
|---|---|---|
| Bauen | eine Sekunde | mehrere Minuten, mit sehr viel Text |
| Menüeintrag | sofort da | erscheint manchmal erst nach kurzer Verzögerung |
| Befehle | nur die aus dem Kurs | alles, was Nushell kann |
| Daten des Entwicklungslaufs | Ihre Karten aus M5 und M6 | Ihre Karten aus dem Kurs |

Das Übungs-Terminal startet, wo Sie im Kurs stehen: **im Container `tauri-dev`, im Projektordner**. Führen Sie die Zellen der Reihe nach aus. Nach einem Neustart des Kernels beginnt alles von vorn.
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
## 1 Was bisher lief: der Entwicklungslauf

So haben Sie Ihre App bisher gestartet: im Container, mit `cargo tauri dev`. Führen Sie die Zelle aus.
""")

terminal("cargo tauri dev")

md(r"""
Das ist ein **Entwicklungslauf** (oranger Balken). Ihre Karten aus M5 und M6 sind da. Das Programm existiert aber nur, solange das Terminal offen ist. Eine echte Anwendung soll ohne das auskommen.

| | Entwicklungslauf | Installierte Anwendung |
|---|---|---|
| Start | `cargo tauri dev` | Anwendungsmenü |
| Terminal | muss offen sein | wird nicht gebraucht |
| Code | wird bei jeder Änderung neu übersetzt | bleibt, wie er gebaut wurde |
| Daten | im Entwicklungsordner | im eigenen Anwendungsbereich |

> „Sie haben die ganze Zeit eine Anwendung in Entwicklung gebaut. Jetzt wird daraus eine Anwendung.“
""")

# ================================================================== 2
md(r"""
---
## 2 Die drei Zusatzdateien

Im Projektordner liegen drei Dateien, die Sie noch nicht angefasst haben. Sie werden gemeinsam angesehen, nicht geschrieben.

| Datei | Zweck, in einem Satz |
|---|---|
| `de.metarow.Lernkarten.desktop` | der **Eintrag im Anwendungsmenü**: Name, Symbol, was gestartet wird |
| `de.metarow.Lernkarten.metainfo.xml` | der **Beschreibungstext**, wie man ihn in einem App-Store sieht |
| `de.metarow.Lernkarten.yml` | die **Bauanleitung**: was gebraucht wird und wohin es installiert wird |

> **Warum drei Dateien für ein kleines Programm?** Weil das Format für alle gilt. Jede Anwendung, die als Flatpak ausgeliefert wird, braucht diese drei Dateien, egal wie groß sie ist. Sie sind Eintrittskarten, keine Eigenheiten dieses Projekts.

> So oder sehr ähnlich sehen die vorbereiteten Dateien aus. Ihre Kursleitung hat die echten.

### Der Menüeintrag: `de.metarow.Lernkarten.desktop`

### ✏️ Ihre Aufgabe 2

Diese eine Änderung ist erlaubt und macht das Ergebnis persönlich: Tragen Sie hinter `Name=` **Ihren eigenen Anzeigenamen** ein, zum Beispiel `Annas Lernkarten`. Führen Sie die Zelle dann aus. Alles andere bleibt, wie es ist.
""")

code(DESKTOP)

md(r"""
| Zeile | Bedeutung |
|---|---|
| `Name=` | so heißt die App im Menü, **die eine erlaubte Änderung** |
| `Comment=` | kurzer Untertitel |
| `Exec=lernkarten` | welches Programm gestartet wird, der Name aus der Bauanleitung |
| `Icon=de.metarow.Lernkarten` | welches Symbol angezeigt wird |
| `Terminal=false` | **kein** Terminal öffnen |
| `Categories=Education;` | in welcher Gruppe im Menü sie erscheint |

### Der Beschreibungstext: `de.metarow.Lernkarten.metainfo.xml`

```xml
""" + METAINFO + r"""
```

Das ist der Text, den eine Software-Verwaltung wie GNOME Software zur App anzeigt: Name, Zusammenfassung, Beschreibung, Lizenz, Version.

### Die Bauanleitung: `de.metarow.Lernkarten.yml`

```yaml
""" + YML + r"""
```

| Teil | Bedeutung |
|---|---|
| `id` | der eindeutige Name der App, überall gleich geschrieben |
| `runtime`, `sdk` | die Unterlage, auf der die App läuft und gebaut wird (hier GNOME 50) |
| `sdk-extensions: rust-stable` | bringt `cargo` in die Bauumgebung. Der Rust aus dem Container ist dort nicht erreichbar, und das ist gewollt. |
| `finish-args` | die **Berechtigungen**: Was die App später darf. Mehr dazu in Abschnitt 5. |
| `build-commands` | die Schritte: übersetzen, dann Programm, Menüeintrag, Beschreibung und Symbol an ihren Platz legen |

### 🤔 Zuordnen

Welche Datei ist gemeint?

| Beschreibung | Datei |
|---|---|
| Der Text, der in einem App-Store neben dem Symbol steht | |
| Was gebraucht wird und wohin es installiert wird | |
| Der Name und das Symbol im Anwendungsmenü | |
""")

loesung("💡 Auflösung", r"""
| Beschreibung | Datei |
|---|---|
| Text im App-Store | `.metainfo.xml` |
| was gebraucht wird, wohin es kommt | `.yml` (Bauanleitung) |
| Name und Symbol im Menü | `.desktop` |
""")

# ================================================================== 3
md(r"""
---
## 3 Bauen

### 🐞 Der erste Versuch

Sie sind noch im Container, so wie den ganzen Kurs über. 🤔 Was passiert, wenn Sie direkt bauen?
""")

terminal(BAUEN)

md(r"""
`executable was not found`: Im Container gibt es kein `flatpak`. Die Meldung hat mit dem eigentlichen Problem scheinbar nichts zu tun. Sie sagt nicht „Sie sind im falschen Raum“, sondern nur „kenne ich nicht“.

> **Der Bau läuft auf dem Host, nicht im Container.** Zuerst `exit`.

Wo bin ich gerade? Die Zeile aus der Befehlskarte verrät es, und die Eingabeaufforderung auch: Im Container beginnt sie mit **⬢ tauri-dev**.

### Der richtige Weg
""")

terminal("# Wo bin ich?", WO_BIN_ICH, "", "# Raus aus dem Container", "exit", WO_BIN_ICH,
         "", "# In den Projektordner und bauen", "cd ~/Projekte/lernkarten", BAUEN, "", "# Was ist neu im Projektordner?", "ls")

md(r"""
Während der Bau läuft, passiert Folgendes: Das Programm wird **noch einmal übersetzt**, diesmal in einer abgeschlossenen Umgebung, damit es auf jedem Rechner gleich läuft. Danach liegen zwei neue Ordner im Projekt: `build-dir` (das Zwischenergebnis) und `repo` (das fertige Paket).

> **Der echte Bau dauert spürbar länger.** Es läuft sehr viel Text durch das Terminal. Das ist kein Absturz.

### 🤔 Was macht welcher Teil des Befehls?

```nu
flatpak run org.flatpak.Builder --force-clean --repo=repo build-dir de.metarow.Lernkarten.yml
```

| Teil | Bedeutung |
|---|---|
| `flatpak run` | |
| `org.flatpak.Builder` | |
| `--force-clean` | |
| `--repo=repo` | |
| `build-dir` | |
| `de.metarow.Lernkarten.yml` | |
""")

loesung("💡 Auflösung", r"""
| Teil | Bedeutung |
|---|---|
| `flatpak run` | ein Flatpak-Werkzeug starten |
| `org.flatpak.Builder` | das Werkzeug, das aus der Bauanleitung ein Programm baut |
| `--force-clean` | alten Bauvorgang verwerfen und neu anfangen |
| `--repo=repo` | das fertige Paket in das Verzeichnis `repo` legen |
| `build-dir` | der Ordner mit dem Zwischenergebnis |
| `de.metarow.Lernkarten.yml` | die Bauanleitung, die gelesen wird |
""")

# ================================================================== 4
md(r"""
---
## 4 Installieren und starten

Zwei Befehle: Zuerst wird `repo` als **Paketquelle** eingetragen, dann wird daraus **installiert**.
""")

terminal('flatpak remote-add --user --no-gpg-verify --if-not-exists lernkarten-lokal $"($env.PWD)/repo"',
         "flatpak install --user lernkarten-lokal de.metarow.Lernkarten")

md(r"""
| Befehl | Was er tut |
|---|---|
| `flatpak remote-add` | das lokale Verzeichnis `repo` als Paketquelle eintragen |
| `flatpak install` | die Anwendung aus dieser Quelle installieren |

Und jetzt: **Editor schließen. Terminal schließen.** Öffnen Sie das Anwendungsmenü und starten Sie Ihre App mit einem Klick. 🖱️
""")

code("# Anwendungsmenü")

md(r"""
> ## 🎉 Das ist der Moment.
> Ihre App startet **ohne Terminal, ohne Editor, ohne eine einzige getippte Zeile**. Mit Ihrem Namen im Menü. Bleiben Sie kurz stehen und lassen Sie das wirken: Vor ein paar Tagen war das eine leere `index.html`.
""")

# ================================================================== 5
md(r"""
---
## 5 Was jetzt anders ist

🤔 Schauen Sie in das Fenster, das Sie gerade aus dem Menü gestartet haben. **Wo sind Ihre Karten?**

Fragen wir das Terminal. Nushell zeigt mit `open` den Inhalt einer JSON-Datei gleich als Tabelle.
""")

terminal('ls ~/.local/share | where name =~ "Lernkarten"',
         "ls ~/.var/app/de.metarow.Lernkarten/data",
         "", "# Die Karten des Entwicklungslaufs",
         "open ~/.local/share/de.metarow.Lernkarten/lernkarten.json",
         "", "# Die Karten der installierten App",
         "open ~/.var/app/de.metarow.Lernkarten/data/de.metarow.Lernkarten/lernkarten.json")

md(r"""
Es gibt **zwei** Datenordner:

| | Entwicklungslauf | Installierte Anwendung |
|---|---|---|
| Ordner | `~/.local/share/de.metarow.Lernkarten` | `~/.var/app/de.metarow.Lernkarten/data` |
| Datei | `lernkarten.json` | `lernkarten.json` |

Die installierte App hat einen **eigenen, abgetrennten Bereich**. Dort gibt es die Datei erst, wenn die App zum ersten Mal speichert. 🖱️ Legen Sie im installierten Fenster eine Karte an und führen Sie die Zelle oben erneut aus.

> **Das ist kein Fehler.** Das ist der Preis der Trennung, und die Trennung ist der Grund, warum die Anwendung sicher ist. Eine installierte Anwendung darf nicht einfach in die Dateien des Benutzers schreiben. Deshalb hat sie ihren eigenen Bereich.
>
> Der eigene Bereich ist kein Verlust, sondern der Grund, warum Flatpak-Apps funktionieren.

### Die Berechtigungen
""")

terminal("flatpak info --show-permissions de.metarow.Lernkarten")

md(r"""
> „Die Anwendung darf nur das, was hier steht. Sie kommt nicht an Ihre übrigen Dateien.“

| Zeile | Bedeutung |
|---|---|
| `shared=ipc` | darf mit dem Fenstersystem Daten austauschen |
| `sockets=wayland;fallback-x11` | darf ein Fenster auf dem Bildschirm öffnen |
| `devices=dri` | darf die Grafikkarte zum Zeichnen benutzen |

Was **nicht** dasteht: kein Zugriff auf Ihr Home-Verzeichnis, kein Netzwerk. Diese Zeilen stammen aus `finish-args` in der Bauanleitung.

### 🤔 Was folgt daraus?

Was bedeutet es, wenn die App nur auf das zugreifen darf, was in den Berechtigungen steht?
""")

loesung("💡 Antwort", r"""
Die App kann **nicht** in Ihren Dokumenten lesen oder schreiben, nicht ins Netz und nicht an andere Programme. Selbst wenn in ihrem Code ein Fehler steckt oder jemand Böses hineingeschrieben hätte, bleibt der Schaden in ihrem eigenen Bereich.

Daraus folgt auch: Die Karten des Entwicklungslaufs in `~/.local/share` sind für sie unerreichbar. Das ist genau die Trennung, die Sie in Abschnitt 5 gesehen haben.

Erinnern Sie sich an K5? *Eine Webseite ist ein Gast, eine installierte Anwendung hat einen Schlüssel.* Jetzt sehen Sie: Der Schlüssel passt nur zu **ihrem** Schrank.
""")

# ================================================================== 6
md(r"""
---
## 6 Eine neue Fassung ausliefern

*Code bleibt, wie er gebaut wurde.* Was heißt das?

### ✏️ Ihre Aufgabe 6

1. Ändern Sie in der `.desktop`-Zelle in Abschnitt 2 den Namen noch einmal und führen Sie sie aus.
2. Führen Sie das Anwendungsmenü unten aus. 🤔 Welcher Name steht dort?
""")

code("# Anwendungsmenü")

md(r"""
Noch der **alte** Name. Die installierte App ist ein fertiges Paket. Was Sie danach im Projekt ändern, kommt erst mit einem neuen Bau und einem **Update** an:
""")

terminal(BAUEN, "flatpak update --user de.metarow.Lernkarten")

code("# Anwendungsmenü")

md(r"""
Jetzt steht der neue Name im Menü. Dasselbe gilt für jede Änderung an `index.html`, `style.css` oder `app.js`: **ändern, bauen, aktualisieren.** Im Entwicklungslauf dagegen wirkt jede Änderung sofort.

> Und die Karten der installierten App? Die sind bei einem Update **noch da**. Daten und Programm liegen an verschiedenen Orten.
""")

# ================================================================== 7
md(r"""
---
## 7 Ein Bundle zum Mitnehmen

Aus dem Paket in `repo` lässt sich **eine einzelne Datei** machen, die auf einen anderen Rechner mitgenommen werden kann:
""")

terminal("flatpak build-bundle repo lernkarten.flatpak de.metarow.Lernkarten --runtime-repo=https://flathub.org/repo/flathub.flatpakrepo", "ls")

md(r"""
Die Datei `lernkarten.flatpak` können Sie auf einen USB-Stick kopieren. Auf einem anderen Rechner mit Flatpak installieren Sie sie so:

```nu
flatpak install --user lernkarten.flatpak
```

Die `--runtime-repo`-Angabe sorgt dafür, dass der andere Rechner die GNOME-Unterlage selbst von Flathub holen kann.
""")

# ================================================================== 8
md(r"""
---
## 8 Fehlerjagd

In jeder Zelle steckt **ein** Fehler. Führen Sie sie aus, lesen Sie die Meldung und überlegen Sie, was fehlt. Die Zellen laufen in der Reihenfolge, in der sie hier stehen.

**a)** Schnell noch einmal den Entwicklungslauf starten:
""")

terminal("cargo tauri dev")

md(r"""
**b)** Noch einmal bauen:
""")

terminal("flatpak run org.flatpak.Builder --force-clean --repo=repo build-dir de.metarow.lernkarten.yml")

md(r"""
**c)** Die neue Fassung installieren:
""")

terminal("flatpak install --user lernkarten-lokal de.metarow.Lernkarten")

md(r"""
**d)** Nach einem Blick ins Home-Verzeichnis bauen:
""")

terminal("cd ~", "ls", BAUEN)

md(r"""
**e)** Zurück in den Container und dort die Berechtigungen anzeigen:
""")

terminal("toolbox enter tauri-dev", "flatpak info --show-permissions de.metarow.Lernkarten")

loesung("💡 Lösungen zur Fehlerjagd", r"""
| | Meldung | Ursache | Abhilfe |
|---|---|---|---|
| a) | `executable was not found` | `cargo` gibt es nur im Container, Sie sind auf dem Host | `toolbox enter tauri-dev`, dann `cargo tauri dev` |
| b) | `Failed to open file … de.metarow.lernkarten.yml` | Name der Bauanleitung falsch geschrieben (klein statt groß) | `de.metarow.Lernkarten.yml`, `ls` zeigt den genauen Namen |
| c) | `already installed` | `install` gilt nur für das erste Mal | `flatpak update --user de.metarow.Lernkarten` |
| d) | `Failed to open file …` | nicht im Projektordner | `cd ~/Projekte/lernkarten` |
| e) | `executable was not found` | `flatpak` gibt es nur auf dem Host | `exit` |

a) und e) sind Spiegelbilder: **Entwickeln im Container, Ausliefern auf dem Host.**

Wer weiterarbeiten will, bringt das Übungs-Terminal mit `exit` und `cd ~/Projekte/lernkarten` zurück an den richtigen Ort.
""")

md(r"""
### Die Diagnosetabelle für K7

| Beobachtung | Ursache |
|---|---|
| `flatpak … executable was not found` | noch im Container: erst `exit` |
| `cargo … executable was not found` | auf dem Host: Entwickeln geht nur im Container |
| `Failed to open file … .yml` | falscher Ordner oder Name der Bauanleitung falsch |
| Der Bau läuft, es passiert lange nichts | normal, der Bau dauert spürbar länger |
| `already installed` | `flatpak update` statt `install` |
| Die App erscheint im Menü erst spät | das Menü braucht einen Moment |
| Die Karten aus dem Entwicklungslauf fehlen | eigener Datenbereich der installierten App, kein Fehler |
| Änderung ist in der installierten App nicht zu sehen | neu bauen und `flatpak update` |
| Zugriffsfehler beim Bauen | `flatpak override --user --filesystem=home org.flatpak.Builder` |
""")

# ================================================================== 9
md(r"""
---
## 9 Abschluss: der ganze Weg, Rückblick und Checkliste

### 🤔 Der Weg von der `index.html` bis zum Menüeintrag

Das ist die Frage aus dem Lernstandsgespräch nach K7. Beantworten Sie sie in eigenen Worten, bevor Sie aufklappen:

> **„Beschreiben Sie den Weg von Ihrer `index.html` bis zum Eintrag im Anwendungsmenü.“**

| Schritt | Was entsteht |
|---|---|
| Ihre drei Dateien `index.html`, `style.css`, `app.js` und der Programmkern | |
| Die drei Zusatzdateien | |
| Der Build-Befehl | |
| `flatpak remote-add` | |
| `flatpak install` | |
""")

loesung("💡 Eine mögliche Antwort", r"""
| Schritt | Was entsteht |
|---|---|
| `index.html`, `style.css`, `app.js`, `main.rs` | die Anwendung selbst: Fenster und Programmkern |
| die drei Zusatzdateien | die Beschreibung drumherum: Menüeintrag, Beschreibungstext, Bauanleitung |
| der Build-Befehl | aus der Bauanleitung wird ein fertiges Paket in `repo`; die `index.html` wird dabei mit hineingelegt |
| `flatpak remote-add` | `repo` wird als Paketquelle eingetragen |
| `flatpak install` | die App ist installiert und steht im Anwendungsmenü |

Und der letzte Schritt: Die App startet **ohne Terminal**. Das ist der Punkt, an dem aus einem Projekt eine Anwendung wird.
""")

md(r"""
### Rückblick

| Station | Was dort entstand | Notebook |
|---|---|---|
| K0 | die drei Dateien: was da ist, wie es aussieht, was passiert | |
| K1 | die Oberfläche, jedes Element mit einem Namen | |
| K2 | der Sprung von einer Sammlung von Feldern zu etwas, das man zeigen möchte | |
| K3 | die Sprache, mit der die Anwendung denkt | [M3](M03_JavaScript_Bausteine.ipynb) |
| K4 | die Verbindung zwischen Daten und Fenster | [M4](M04_JavaScript_im_Fenster.ipynb) |
| K5 | die Brücke zum Programmkern, die Datei auf der Platte | [M5](M05_Daten_behalten.ipynb) |
| K6 | die eigene Gestaltung, die eigene Verbesserung | [M6](M06_Feinschliff.ipynb) |
| K7 | der Eintrag im Anwendungsmenü | dieses Notebook |

### ✏️ Eine Sache, die mich überrascht hat

Doppelklicken Sie auf diese Zelle und ergänzen Sie, für die Abschlussrunde:

> **Überrascht hat mich:** …

### ✅ Checkliste

Haken Sie ab (Doppelklick auf diese Zelle, dann `[ ]` zu `[x]` ändern):

- [ ] Den Anzeigenamen in der `.desktop`-Datei angepasst
- [ ] Das Flatpak gebaut und installiert, auf dem Host
- [ ] Die App ohne Terminal aus dem Menü gestartet
- [ ] Beide Datenordner aufgesucht und den Unterschied benannt
- [ ] Die Berechtigungen angezeigt und vorgelesen
- [ ] Den Weg von der `index.html` bis zum Menüeintrag beschrieben

### Wie geht es weiter?

Sie haben eine eigene Desktop-Anwendung gebaut und ausgeliefert. Wer weitermachen möchte: Empfohlen ist zuerst ein vertiefender **Web-Grundlagenkurs** mit CSS Grid, Formularverarbeitung, Funktionen höherer Ordnung und asynchroner Programmierung. Danach ist der Übergang in den ausführlichen Tauri-Kurs mit Vue möglich.

**Zum Nachschlagen:** K7 Merkblatt · K7 Übungsblatt · Anhang Befehlskarte
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
    c["id"] = f"m07-{i:03d}"
    c["source"] = c["source"].splitlines(keepends=True)

with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(len(cells), "Zellen geschrieben")
