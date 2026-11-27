#!/usr/bin/env bash
# Erzeugt alle Begleit-Notebooks M00–M07 neu nach content/.
# Aufruf aus dem Wurzelverzeichnis des Repos:  bash tools/lernkarten-notebooks/alle_erzeugen.sh
set -euo pipefail

hier="$(cd "$(dirname "$0")" && pwd)"
ziel="$(cd "$hier/../.." && pwd)/content"

python3 "$hier/gen_m00.py" "$ziel/M00_Ankommen.ipynb"
python3 "$hier/gen_m01.py" "$ziel/M01_HTML_die_Struktur.ipynb"
python3 "$hier/gen_m02.py" "$ziel/M02_CSS_das_Aussehen.ipynb"
python3 "$hier/gen_m03.py" "$ziel/M03_JavaScript_Bausteine.ipynb"
python3 "$hier/gen_m04.py" "$ziel/M04_JavaScript_im_Fenster.ipynb"
python3 "$hier/gen_m05.py" "$ziel/M05_Daten_behalten.ipynb"
python3 "$hier/gen_m06.py" "$ziel/M06_Feinschliff.ipynb"
python3 "$hier/gen_m07.py" "$ziel/M07_Als_Anwendung_ausliefern.ipynb"
