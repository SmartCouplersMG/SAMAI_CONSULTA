"""Prueba: ¿la pagina de resultados de SAMAI responde por GET directo
con el BusquedaDictionary en el query string? Si si, evitamos Playwright."""
import json, urllib.parse, urllib.request, re

dict_busqueda = {
    "corporacion": "1100103",
    "modo": "2",
    "filtro": "",
    "busqueda": '("contrato estatal")',
    "searchMode": "all",
    "orderby": "FechaProvidencia desc",
    "PaginaActual": "0",
}
qs = urllib.parse.quote(json.dumps(dict_busqueda, ensure_ascii=False))
url = ("https://samai.consejodeestado.gov.co/TitulacionRelatoria/"
       "ResultadoBuscadorProvidenciasTituladas.aspx?BusquedaDictionary=" + qs)
print("URL:", url[:130], "...\n")

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        html = resp.read().decode("utf-8", "ignore")
    print("STATUS:", resp.status, " LEN:", len(html))
    with open("samai_get_directo.html", "w", encoding="utf-8") as f:
        f.write(html)
    pag = re.search(r"P[aá&#;\d]*gina\s+\d+\s+de\s+\d+", html)
    print("Paginacion:", pag.group(0) if pag else "NO encontrada")
    print("Ocurrencias 'VerProvidencia':", html.count("VerProvidencia"))
    print("Filas 'Interno:':", html.count("Interno:"))
    print("Filas 'del proceso':", html.count("del proceso"))
    # radicados visibles
    rads = re.findall(r"list_procesos\.aspx\?guid=(\d+)", html)
    print("Radicados/guids encontrados:", len(rads), rads[:5])
except Exception as e:
    print("ERROR:", repr(e))
