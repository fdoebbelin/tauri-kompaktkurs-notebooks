# Tauri-Kompaktkurs: Begleit-Notebooks

Interaktive Notebooks zum Kompaktkurs **„Vom Web zur Desktop-App mit Tauri“**. Im Kurs bauen drei Teilnehmende ohne Vorkenntnisse eine **Lernkarten-App** aus HTML, CSS und JavaScript und liefern sie als Flatpak aus. Zu jedem Modul gibt es ein Notebook, das im Browser läuft. Installiert werden muss nichts.

➡️ **Im Browser öffnen: https://fdoebbelin.github.io/tauri-kompaktkurs-notebooks/**

## Die Module

| Notebook | Modul | Worum es geht |
|---|---|---|
| [M00 Ankommen](content/M00_Ankommen.ipynb) | K0 | die fertige App, die drei Dateien, App starten, erste eigene Änderung |
| [M01 HTML](content/M01_HTML_die_Struktur.ipynb) | K1 | Elemente, Verschachtelung, `id` und `class`, die Oberfläche in vier Etappen |
| [M02 CSS](content/M02_CSS_das_Aussehen.ipynb) | K2 | Regeln, Hex-Farben, Selektoren, Boxmodell, Flexbox |
| [M03 JavaScript – die Bausteine](content/M03_JavaScript_Bausteine.ipynb) | K3 | Variablen, Funktionen, `if`, Listen, Objekte, der Datenbestand |
| [M04 JavaScript im Fenster](content/M04_JavaScript_im_Fenster.ipynb) | K4 | `querySelector`, Klicks, `listeAnzeigen()`, die drei Knöpfe |
| [M05 Daten behalten](content/M05_Daten_behalten.ipynb) | K5 | Programmkern, `invoke`/`await`/`async`, speichern und laden |
| [M06 Feinschliff](content/M06_Feinschliff.ipynb) | K6 | eigene Gestaltung, Kontrast, genau eine Verbesserung, Löschknopf |
| [M07 Als Anwendung ausliefern](content/M07_Als_Anwendung_ausliefern.ipynb) | K7 | Flatpak bauen, installieren, eigener Datenbereich, Berechtigungen |

Die Links oben zeigen die Dateien auf GitHub. **Ausführen** lassen sich die Notebooks nur auf der JupyterLite-Seite.

## So benutzen Sie ein Notebook

1. Die Seite öffnen und das Notebook im Dateibrowser links anklicken.
2. **Zuerst die eingeklappte Vorbereitungszelle ausführen** (anklicken, dann Umschalt + Enter). Sie enthält die Werkzeuge des Notebooks: App-Fenster, Konsole, Übungs-Terminal und Prüfhilfen.
3. Danach die Zellen der Reihe nach ausführen.

Was Sie in einem Notebook ändern, wird nur in Ihrem Browser gespeichert. Die Karten der Lernkarten-App liegen im Speicher des Browsers (`localStorage`). Programmkern, Container und Flatpak werden im Browser nachgebildet; die Notebooks sagen das jeweils dazu.

## Aufbau des Repos

| Pfad | Inhalt |
|---|---|
| `content/` | die acht Notebooks, erzeugt aus den Skripten in `tools/` |
| `tools/lernkarten-notebooks/` | Generator-Skripte, Werkzeugkisten und Testhilfe, siehe [README dort](tools/lernkarten-notebooks/README.md) |
| `requirements.txt` | JupyterLite mit dem JavaScript-Kernel |
| `.github/workflows/deploy.yml` | baut die Seite und veröffentlicht sie auf GitHub Pages |

**Die Notebooks nicht von Hand bearbeiten**, sondern die Skripte in `tools/` ändern und neu erzeugen:

```bash
bash tools/lernkarten-notebooks/alle_erzeugen.sh
```

## Lokal bauen

```bash
python -m pip install -r requirements.txt
jupyter lite build --contents content --output-dir dist
python -m http.server 8000 --directory dist
```

Danach http://localhost:8000 im Browser öffnen.

## Herkunft

Die Notebooks sind im Repo `fdoebbelin/jupyterlite` entstanden und von dort samt Historie hierher umgezogen. Die Merge-Commits verweisen deshalb auf Pull Requests in `fdoebbelin/jupyterlite`.

Das Kursmaterial selbst (Leitfäden, Merkblätter, Übungsblätter) liegt im Knowledge-Repo unter `01-Courses/Programming/Tauri-Kompaktkurs`.
