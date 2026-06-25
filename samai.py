"""
samai.py — Cliente de busqueda de jurisprudencia del Consejo de Estado (SAMAI).

Descubrimiento clave: la pagina de resultados responde por GET directo con el
parametro `BusquedaDictionary` (un JSON en el query string). No se necesita
Playwright, ViewState ni postbacks. Solo requests + BeautifulSoup.

Funcion principal: buscar(...) -> dict con paginacion y lista de providencias.
"""
import io
import json
import re
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup

BASE = "https://samai.consejodeestado.gov.co"
RESULTADOS_URL = f"{BASE}/TitulacionRelatoria/ResultadoBuscadorProvidenciasTituladas.aspx"

# Corporaciones (codigo interno SAMAI). Consejo de Estado = 1100103.
CORPORACIONES = {
    "consejo_estado": "1100103",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0 Safari/537.36"}


def _get(url, intentos=4, timeout=90):
    """GET con reintentos (el DNS del portal/Azure a veces falla transitoriamente)."""
    ultima = None
    for n in range(intentos):
        try:
            return requests.get(url, headers=HEADERS, timeout=timeout)
        except requests.exceptions.ConnectionError as e:
            ultima = e
            time.sleep(1.5)
    raise ultima


def _txt(node):
    return node.get_text(strip=True) if node else None


def _por_indice(soup, sufijo, i):
    """Busca un span/control cuyo id termine en `sufijo_{i}`."""
    el = soup.find(id=re.compile(rf"{re.escape(sufijo)}_{i}$"))
    return _txt(el)


def buscar(busqueda, pagina=0, orderby="FechaProvidencia desc",
           corporacion="consejo_estado", search_mode="all", timeout=60):
    """
    Ejecuta una busqueda en SAMAI y devuelve resultados estructurados.

    busqueda: texto libre. Soporta conectores AND/OR/AND NOT y frases entre
              comillas, p.ej. '"contrato estatal" AND nulidad'.
    pagina:   indice de pagina (0 = primera).
    Devuelve: {"total_paginas": int, "pagina": int, "resultados": [ ... ]}
    """
    cod_corp = CORPORACIONES.get(corporacion, corporacion)
    dict_busqueda = {
        "corporacion": cod_corp,
        "modo": "2",
        "filtro": "",
        "busqueda": busqueda,
        "searchMode": search_mode,
        "orderby": orderby,
        "PaginaActual": str(pagina),
    }
    qs = urllib.parse.quote(json.dumps(dict_busqueda, ensure_ascii=False))
    url = f"{RESULTADOS_URL}?BusquedaDictionary={qs}"

    resp = _get(url, timeout=timeout)
    resp.raise_for_status()
    return _parsear(resp.text)


def _parsear(html):
    soup = BeautifulSoup(html, "html.parser")

    # total de paginas
    total_paginas = None
    lbl_pag = soup.find(id=re.compile(r"PaginaActualLabel$"))
    if lbl_pag:
        m = re.search(r"de\s+([\d.]+)", lbl_pag.get_text())
        if m:
            total_paginas = int(m.group(1).replace(".", ""))

    resultados = []
    # cada providencia tiene un HypRadicado_{i}
    radicados = soup.find_all(id=re.compile(r"_HypRadicado_\d+$"))
    for hyp in radicados:
        i = int(re.search(r"_(\d+)$", hyp["id"]).group(1))

        # enlace al documento (JWT en VerProvidencia.aspx)
        url_doc = None
        doclink = soup.find(id=re.compile(rf"_documentlink_{i}$"))
        if doclink and doclink.has_attr("onclick"):
            m = re.search(r"CargarVentana\('([^']+)'\)", doclink["onclick"])
            if m:
                url_doc = m.group(1)

        # problema juridico (puede haber varios sub-bloques; tomamos el primero)
        pj = soup.find(id=re.compile(rf"_ProblemaJuridicoLabel_0$".replace(
            "ProblemaJuridicoLabel", f"{i}_TitulacionRepeater_{i}_ProblemaJuridicoLabel")))

        resultados.append({
            "radicado": _txt(hyp),
            "guid": (re.search(r"guid=(\w+)", hyp.get("href", "")) or [None, None])[1]
                     if hyp.get("href") else None,
            "url_proceso": urllib.parse.urljoin(BASE + "/TitulacionRelatoria/",
                                                hyp["href"]) if hyp.get("href") else None,
            "interno": _por_indice(soup, "_LblInterno", i),
            "clase_proceso": _por_indice(soup, "_LblClaseProceso", i),
            "fecha_proceso": _por_indice(soup, "_LblFECHAPROC", i),
            "fecha_providencia": _por_indice(soup, "_Label1", i),
            "ponente": _por_indice(soup, "_LblPonente", i),
            "sala": _por_indice(soup, "_LbNombreSalaDecision", i),
            "actor": _por_indice(soup, "_LblActor", i),
            "demandado": _por_indice(soup, "_LblDemandado", i),
            "tipo_providencia": _por_indice(soup, "_LblTIPOPROVIDENCIA", i),
            "descripcion_actuacion": _por_indice(soup, "_LblA110DESCACTU", i),
            "problema_juridico": _txt(pj),
            "url_documento": url_doc,
        })

    return {"total_paginas": total_paginas,
            "resultados_en_pagina": len(resultados),
            "resultados": resultados}


def obtener_texto(url_documento, con_texto=True):
    """
    Dada la `url_documento` de un resultado (VerProvidencia.aspx?tokenDocumento=...),
    sigue la cadena hasta el PDF en Azure Blob y devuelve el texto completo.

    Devuelve: {"url_pdf": str, "paginas": int, "texto": str}
    El token JWT del visor y el SAS del blob son de vida corta: llamar poco
    despues de la busqueda.
    """
    vp = _get(url_documento)
    vp.raise_for_status()
    soup = BeautifulSoup(vp.text, "html.parser")
    btn = soup.find(id=re.compile(r"DescargarProvideciaLinkButton$"))
    blob = btn["href"] if btn and btn.has_attr("href") else None
    if not blob:
        raise RuntimeError("No se encontro la URL del PDF en el visor "
                           "(token expirado o documento no disponible).")
    if not con_texto:
        return {"url_pdf": blob, "paginas": None, "texto": None}

    from pypdf import PdfReader
    pdf = _get(blob)
    pdf.raise_for_status()
    reader = PdfReader(io.BytesIO(pdf.content))
    texto = "\n".join((p.extract_text() or "") for p in reader.pages)
    return {"url_pdf": blob, "paginas": len(reader.pages), "texto": texto}


if __name__ == "__main__":
    import sys
    termino = sys.argv[1] if len(sys.argv) > 1 else '"contrato estatal"'
    data = buscar(termino, pagina=0)
    print(f"Total paginas: {data['total_paginas']}  "
          f"En esta pagina: {data['resultados_en_pagina']}\n")
    for r in data["resultados"][:3]:
        print("-" * 70)
        print("Radicado :", r["radicado"], "| Interno:", r["interno"])
        print("Fecha    :", r["fecha_providencia"])
        print("Tipo     :", r["tipo_providencia"], "|", r["clase_proceso"])
        print("Ponente  :", r["ponente"])
        print("Sala     :", r["sala"])
        print("Problema :", (r["problema_juridico"] or "")[:120])
        print("Doc URL  :", (r["url_documento"] or "")[:90], "...")
