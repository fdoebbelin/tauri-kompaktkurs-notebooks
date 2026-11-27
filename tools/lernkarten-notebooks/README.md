# Begleit-Notebooks zum Tauri-Kompaktkurs

Mit diesen Skripten werden die Notebooks `content/M00_…` bis `content/M07_…` erzeugt. Jedes Notebook begleitet ein Modul (K0 bis K7) des Kompaktkurses „Vom Web zur Desktop-App mit Tauri“, in dem eine Lernkarten-App gebaut wird.

**Die Notebooks nicht von Hand bearbeiten**, sondern das passende Skript ändern und neu erzeugen. Sonst geht die Änderung beim nächsten Erzeugen verloren.

## Neu erzeugen

Aus dem Wurzelverzeichnis des Repos, alle auf einmal:

```bash
bash tools/lernkarten-notebooks/alle_erzeugen.sh
```

Oder einzeln:

```bash
python3 tools/lernkarten-notebooks/gen_m04.py content/M04_JavaScript_im_Fenster.ipynb
```

Es wird nur die Python-Standardbibliothek gebraucht. Die Skripte erzeugen immer dieselbe Datei, Byte für Byte. Ein `git diff` nach dem Erzeugen zeigt also genau die gewollte Änderung.

## Dateien

| Datei | erzeugt | Werkzeugkiste |
|---|---|---|
| `gen_m00.py` | `M00_Ankommen.ipynb` | `m00_setup.js`: fertige App, Ebenen, Übungs-Terminal, Projektfenster |
| `gen_m01.py` | `M01_HTML_die_Struktur.ipynb` | `m01_setup.js`: HTML-Vorschau, Spielwiese, Element-Baum, `idListe`, `idRegeln` |
| `gen_m02.py` | `M02_CSS_das_Aussehen.ipynb` | `m02_setup.js`: CSS-Vorschau, Fensterbreite, Kisten, CSS-Prüfer, `farbe`, `kontrast` |
| `gen_m03.py` | `M03_JavaScript_Bausteine.ipynb` | im Skript selbst: Konsolen-Ausgabe wie im Browser, `pruefe` |
| `gen_m04.py` | `M04_JavaScript_im_Fenster.ipynb` | `m04_setup.js`: App-Fenster mit Konsole für `// app.js`-Zellen |
| `gen_m05.py` | `M05_Daten_behalten.ipynb` | `m05_setup.js`: zusätzlich nachgebildeter Programmkern (`invoke`) und `lernkarten.json` |
| `gen_m06.py` | `M06_Feinschliff.ipynb` | `m06_setup.js`: zusätzlich Live-Vorschau für `style.css`, Kursliste-Hinweise, `kontrast` |
| `gen_m07.py` | `M07_Als_Anwendung_ausliefern.ipynb` | `m07_setup.js`: Übungs-Terminal, Anwendungsmenü, getrennte Datenbereiche |
| `alle_erzeugen.sh` | alle acht | |
| `notebook_pruefen.js` | – | führt ein Notebook im Browser aus und gibt die Ausgaben aus |

**Abhängigkeiten zwischen den Skripten:** Die Skripte teilen sich Bausteine, indem sie den Kopf eines anderen Skripts ausführen, also alles vor der Zeile `# ===… Einstieg`.

- `gen_m04.py` liefert die Helfer (`md`, `code`, `loesung`, `app`), `index.html`, `style.css` und die `app.js`-Bausteine aus K4. Genutzt von M00, M01, M02, M05, M06 und M07.
- `gen_m05.py` liefert die K5-Bausteine (`speichern`, `laden`, …). Genutzt von M00, M06 und M07.

Wer dort etwas ändert, erzeugt am besten alle Notebooks neu und prüft den `git diff`.

**Platzhalter:** In den `m0X_setup.js`-Dateien stehen Platzhalter wie `__HTML__`, `__CSS__` oder `__JS__`. Die Skripte ersetzen sie beim Erzeugen durch die Kursdateien. Die Werkzeugkiste landet als eingeklappte erste Code-Zelle im Notebook.

## Wie die Werkzeugkisten funktionieren

Die Notebooks laufen im JavaScript-Kernel von JupyterLite (`jupyterlite-javascript-kernel`). Er führt Code in einem **Web Worker** aus, also ohne Fenster und ohne `document`. Die Werkzeugkisten umgehen das:

- Sie ersetzen `self.eval` im Worker. Zellen mit einer Kennung in der ersten Zeile (`// app.js`, `/* style.css */`, `<!-- index.html -->`, `# Terminal` …) werden deshalb nicht im Worker ausgeführt. Stattdessen schickt die Werkzeugkiste ein `display_data` mit einem `<iframe srcdoc>`, und darin läuft die App.
- Ein kleines Skript im iframe leitet `console.log` und Fehler in die Konsole unter dem Fenster um und rechnet die Zeilennummern auf die Zelle um. Es passt außerdem die Höhe an und bedient die Knöpfe im Rahmen.
- `lernkarten.json` liegt im `localStorage` des Browsers, unter Schlüsseln, die mit `tauri-kompaktkurs/` beginnen.

Eigenheiten des Kernels, die man kennen sollte:

- `const` und `let` gelten nur in der eigenen Zelle (indirektes `eval`). Funktionsdeklarationen bleiben dagegen global.
- Ohne Werkzeugkiste zeigt `console.log` `undefined` als leere Zeile und Objekte als `[object Object]`. M03 ersetzt deshalb `console.log`.

## Testen

1. Eine Testseite bauen. Dafür müssen die Pakete aus `requirements.txt` installiert sein, mindestens `jupyterlite-core` und `jupyterlite-javascript-kernel`. Die Testseite braucht `overrides.json`, damit JupyterLab alle Zellen rendert und nicht nur die sichtbaren:

   ```bash
   mkdir -p /tmp/lite/content
   cp content/M0*.ipynb /tmp/lite/content/
   echo '{"@jupyterlab/notebook-extension:tracker": {"windowingMode": "none"}}' > /tmp/lite/overrides.json
   cd /tmp/lite
   jupyter lite build --contents content --output-dir dist
   ```

2. Die Seite ausliefern:

   ```bash
   python3 -m http.server 8000 --directory /tmp/lite/dist
   ```

3. Ein Notebook prüfen. Das braucht Playwright mit Chromium:

   ```bash
   node tools/lernkarten-notebooks/notebook_pruefen.js http://localhost:8000 M04_JavaScript_im_Fenster.ipynb
   ```

Das Skript führt alle Zellen der Reihe nach aus. Klicks in den App-Fenstern ersetzt es nicht: Interaktionen wie „Karte anlegen“ oder „Neu starten“ müssen von Hand oder mit eigenen Playwright-Schritten geprüft werden.
