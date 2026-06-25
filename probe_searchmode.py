"""Investiga searchMode y 'modo': busca el modo que haga que AND filtre de verdad.
Compara total_paginas de una frase vs dos frases bajo cada combinacion."""
import json, urllib.parse, time, requests, re

BASE = "https://samai.consejodeestado.gov.co"
URL = f"{BASE}/TitulacionRelatoria/ResultadoBuscadorProvidenciasTituladas.aspx"
HEADERS = {"User-Agent": "Mozilla/5.0"}

UNA = '"falla del servicio"'
DOS = '"falla del servicio" AND "reparación directa"'

def total_paginas(busqueda, search_mode, modo):
    d = {"corporacion": "1100103", "modo": str(modo), "filtro": "",
         "busqueda": busqueda, "searchMode": search_mode,
         "orderby": "FechaProvidencia desc", "PaginaActual": "0"}
    qs = urllib.parse.quote(json.dumps(d, ensure_ascii=False))
    for _ in range(4):
        try:
            r = requests.get(f"{URL}?BusquedaDictionary={qs}", headers=HEADERS, timeout=60)
            m = re.search(r"de\s+([\d.]+)\s*<", r.text) or re.search(r"de\s+([\d.]+)", r.text)
            # buscar etiqueta "Pagina X de N"
            m2 = re.search(r"P[\wá&#;]*gina\s+\d+\s+de\s+([\d.]+)", r.text)
            n = m2.group(1) if m2 else "?"
            # contar filas reales
            filas = r.text.count("_HypRadicado_")
            return n, filas
        except requests.exceptions.ConnectionError:
            time.sleep(1.5)
    return "ERR", 0

print(f"{'searchMode':<10} {'modo':<5} {'1 frase':<18} {'2 frases (AND)':<18}")
print("-" * 55)
for sm in ["all", "any", "exact", "phrase", "boolean", "exacta", "todas"]:
    for modo in [2]:
        n1, f1 = total_paginas(UNA, sm, modo)
        n2, f2 = total_paginas(DOS, sm, modo)
        print(f"{sm:<10} {modo:<5} pag={str(n1):<6} filas={f1:<5} pag={str(n2):<6} filas={f2}")
