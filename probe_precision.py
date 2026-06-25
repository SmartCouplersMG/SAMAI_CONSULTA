"""Verifica si las comillas y el AND realmente acotan con terminos menos comunes."""
import json, urllib.parse, time, requests, re

URL = ("https://samai.consejodeestado.gov.co/TitulacionRelatoria/"
       "ResultadoBuscadorProvidenciasTituladas.aspx")
HEADERS = {"User-Agent": "Mozilla/5.0"}

def npag(busqueda, sm="all"):
    d = {"corporacion": "1100103", "modo": "2", "filtro": "", "busqueda": busqueda,
         "searchMode": sm, "orderby": "FechaProvidencia desc", "PaginaActual": "0"}
    qs = urllib.parse.quote(json.dumps(d, ensure_ascii=False))
    for _ in range(4):
        try:
            r = requests.get(f"{URL}?BusquedaDictionary={qs}", headers=HEADERS, timeout=60)
            m = re.search(r"P[\wá&#;]*gina\s+\d+\s+de\s+([\d.]+)", r.text)
            return m.group(1) if m else "0"
        except requests.exceptions.ConnectionError:
            time.sleep(1.5)
    return "ERR"

pruebas = [
    ('comillas vs sin comillas:', None),
    ('  "falla del servicio"', '"falla del servicio"'),
    ('  falla del servicio (sin comillas)', 'falla del servicio'),
    ('termino raro solo vs AND:', None),
    ('  "privación injusta de la libertad"', '"privación injusta de la libertad"'),
    ('  "privación injusta de la libertad" AND "error judicial"',
     '"privación injusta de la libertad" AND "error judicial"'),
    ('  "privación injusta de la libertad" AND NOT "absolución"',
     '"privación injusta de la libertad" AND NOT "absolución"'),
]
for etiqueta, q in pruebas:
    if q is None:
        print("\n" + etiqueta)
    else:
        print(f"{etiqueta:<55} paginas = {npag(q)}")
