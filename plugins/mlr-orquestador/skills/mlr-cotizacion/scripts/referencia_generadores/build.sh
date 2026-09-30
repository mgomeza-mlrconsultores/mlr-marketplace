#!/bin/bash
# Build, export and verify one quotation set. Usage: PROY=<key> ./build.sh
set -e
cd "$(dirname "$0")"
python3 genera_propuesta.py && python3 genera_plan.py && python3 genera_xlsx.py
cd out
N=$(cd .. && python3 -c "import comun;print(comun.SUF)")
soffice --headless --convert-to pdf "1. Propuesta Económica - $N.docx" "2. Plan de Trabajo y Alcance Detallado - $N.docx" >/dev/null 2>&1
mkdir -p rec && soffice --headless --convert-to xlsx --outdir rec "3. Anexo de Ruta y Horas - $N.xlsx" >/dev/null 2>&1
cd .. && python3 verifica.py
