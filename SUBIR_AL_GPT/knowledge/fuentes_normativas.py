"""
fuentes_normativas.py
---------------------
Consulta de normas colombianas (Constitución, CPACA y CUALQUIER ley/decreto) desde fuentes
oficiales: Gestor Normativo de la Función Pública y SUIN-Juriscol (MinJusticia, preferente para
VIGENCIA y afectaciones).

NOTA: la extracción depende de la estructura HTML de los sitios oficiales; si cambia, ajusta los
parsers. Es un punto de partida robusto, no una garantía absoluta. La VIGENCIA siempre debe
confirmarse en fuente oficial (SUIN-Juriscol o Corte Constitucional para inexequibilidades).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, asdict, field

import requests
from bs4 import BeautifulSoup

CPACA_URL = "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=41249"
CONSTITUCION_URL = "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=4125"

GESTOR_BASE = "https://www.funcionpublica.gov.co/eva/gestornormativo"
SUIN_BASE = "https://www.suin-juriscol.gov.co"

HEADERS = {"User-Agent": "Mozilla/5.0 GPT-Orquestador-Juridico/1.0"}

# Catálogo de normas frecuentes ya resueltas al Gestor Normativo (id verificado).
# Amplíalo cuando confirmes el id de otras normas en el Gestor Normativo.
CATALOGO_NORMAS = {
    ("constitucion", None, None): {"nombre": "Constitución Política de Colombia", "url": CONSTITUCION_URL},
    ("ley", "1437", "2011"): {"nombre": "Ley 1437 de 2011 - CPACA", "url": CPACA_URL},
}

# Marcadores heurísticos de afectación de vigencia en el texto descargado.
_MARCADORES_VIGENCIA = [
    "derogad", "deroga el", "deroga la", "inexequible", "modificad por", "modificado por",
    "subrogad", "sustituid", "declarado inexequible", "exequible condicional",
]


@dataclass
class FuenteNormativa:
    norma: str
    articulo: str
    texto: str
    url: str


@dataclass
class NormaResultado:
    """Resultado de la búsqueda de una ley/decreto en fuentes oficiales."""
    consulta: str
    tipo: str
    numero: str
    anio: str
    vigencia: str = "POR VERIFICAR EN FUENTE OFICIAL"
    fuentes_oficiales: list = field(default_factory=list)
    consultas_web: list = field(default_factory=list)
    candidatos: list = field(default_factory=list)
    texto: str = ""
    nota: str = ""


def descargar_texto(url: str, timeout: int = 30) -> str:
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    r.encoding = r.apparent_encoding or "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    texto = soup.get_text("\n", strip=True)
    texto = re.sub(r"\n{2,}", "\n", texto)
    return texto


def extraer_articulo(texto: str, articulo: int) -> str:
    """Extrae desde 'ARTÍCULO X' hasta antes de 'ARTÍCULO X+1'."""
    patron_inicio = rf"(ART[IÍ]CULO\s+{articulo}\.?\b.*?)"
    patron_fin = rf"ART[IÍ]CULO\s+{articulo + 1}\.?\b"

    match_inicio = re.search(patron_inicio, texto, flags=re.IGNORECASE | re.DOTALL)
    if not match_inicio:
        return ""

    inicio = match_inicio.start()
    match_fin = re.search(patron_fin, texto[inicio + 1:], flags=re.IGNORECASE | re.DOTALL)
    if match_fin:
        fin = inicio + 1 + match_fin.start()
        return texto[inicio:fin].strip()
    return texto[inicio:inicio + 3000].strip()


def buscar_cpaca(articulo: int) -> FuenteNormativa:
    texto = descargar_texto(CPACA_URL)
    return FuenteNormativa(
        norma="Ley 1437 de 2011 - CPACA",
        articulo=f"Artículo {articulo}",
        texto=extraer_articulo(texto, articulo),
        url=CPACA_URL,
    )


def buscar_constitucion(articulo: int) -> FuenteNormativa:
    texto = descargar_texto(CONSTITUCION_URL)
    return FuenteNormativa(
        norma="Constitución Política de Colombia",
        articulo=f"Artículo {articulo}",
        texto=extraer_articulo(texto, articulo),
        url=CONSTITUCION_URL,
    )


def _norm(s: str) -> str:
    """Minúsculas sin tildes para comparar tipos de norma."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return s.lower().strip()


def detectar_vigencia(texto: str) -> str:
    """Heurística: busca marcadores de derogatoria/modificación/inexequibilidad en el texto.

    NO sustituye la verificación oficial; solo levanta una alerta para que el GPT/usuario
    confirme en SUIN-Juriscol o en la Relatoría de la Corte Constitucional.
    """
    bajo = texto.lower()
    hallazgos = sorted({m for m in _MARCADORES_VIGENCIA if m in bajo})
    if not hallazgos:
        return "Sin marcadores de derogatoria en el texto (CONFIRMAR vigencia en SUIN-Juriscol)."
    return ("POSIBLE AFECTACIÓN DE VIGENCIA: se hallaron marcadores "
            f"{hallazgos}. CONFIRMAR en SUIN-Juriscol / Corte Constitucional antes de citar.")


def fuentes_oficiales_norma(tipo: str, numero: str, anio: str) -> list[dict]:
    """Devuelve los portales oficiales y las URLs/consultas para hallar y verificar la norma."""
    etiqueta = f"{tipo} {numero} de {anio}".strip()
    q = requests.utils.quote(etiqueta)
    return [
        {"nombre": "SUIN-Juriscol (preferente para VIGENCIA)",
         "url": f"{SUIN_BASE}/", "busqueda": f"{SUIN_BASE}/legislacion/normatividad.html ({etiqueta})"},
        {"nombre": "Gestor Normativo - Función Pública",
         "url": f"{GESTOR_BASE}/", "busqueda": f"{GESTOR_BASE}/ (buscar: {etiqueta})"},
        {"nombre": "Secretaría del Senado (basedoc)",
         "url": "http://www.secretariasenado.gov.co/", "busqueda": etiqueta},
        {"nombre": "DAPRE - Presidencia (leyes y decretos)",
         "url": "https://dapre.presidencia.gov.co/normativa/", "busqueda": etiqueta},
        {"nombre": "Corte Constitucional - Relatoría (inexequibilidades)",
         "url": "https://www.corteconstitucional.gov.co/relatoria/", "busqueda": etiqueta},
        {"nombre": "Búsqueda web (site oficial)",
         "url": f"https://www.google.com/search?q={q}+site:suin-juriscol.gov.co", "busqueda": etiqueta},
    ]


def consultas_web_norma(tipo: str, numero: str, anio: str, tema: str = "") -> list[str]:
    """Plantillas de búsqueda listas para usar con Web Search del GPT."""
    base = f"{tipo} {numero} de {anio}".strip()
    return [
        f"site:suin-juriscol.gov.co {base} {tema}".strip(),
        f"site:funcionpublica.gov.co/eva/gestornormativo {base}".strip(),
        f'"{base}" Colombia vigencia derogada Diario Oficial'.strip(),
        f"{base} Colombia texto oficial {tema}".strip(),
    ]


def _suin_candidatos(etiqueta: str, timeout: int = 20) -> list[dict]:
    """Best-effort: intenta listar enlaces de resultados en SUIN. Puede requerir ajuste.

    SUIN-Juriscol usa búsqueda dinámica; este intento es tolerante a fallos y nunca lanza
    excepción hacia afuera. Si no halla nada, el GPT debe usar `consultas_web` con Web Search.
    """
    candidatos: list[dict] = []
    try:
        url = f"{SUIN_BASE}/legislacion/normatividad.html"
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            txt = (a.get_text() or "").strip()
            if txt and any(k in txt.lower() for k in ["ley", "decreto", "constitu", "acto legislativo"]):
                href = a["href"]
                if href.startswith("/"):
                    href = SUIN_BASE + href
                candidatos.append({"titulo": txt[:160], "url": href})
            if len(candidatos) >= 25:
                break
    except Exception:
        pass
    return candidatos


def buscar_norma(tipo: str, numero: str = "", anio: str = "", articulo: int | None = None,
                 tema: str = "") -> NormaResultado:
    """Resuelve cualquier norma colombiana.

    1) Si está en el catálogo (CPACA/Constitución), descarga el texto del Gestor Normativo y, si se
       pide, extrae el artículo, con chequeo heurístico de vigencia.
    2) Si no, devuelve las fuentes oficiales y las consultas web para que el GPT la coteje y
       verifique su VIGENCIA (regla 1-QUATER del protocolo).
    """
    t = _norm(tipo)
    clave = (t, numero or None, anio or None)
    etiqueta = f"{tipo} {numero} de {anio}".strip()

    res = NormaResultado(
        consulta=etiqueta, tipo=tipo, numero=numero, anio=anio,
        fuentes_oficiales=fuentes_oficiales_norma(tipo, numero, anio),
        consultas_web=consultas_web_norma(tipo, numero, anio, tema),
    )

    catalogada = CATALOGO_NORMAS.get(clave) or CATALOGO_NORMAS.get((t, None, None))
    if catalogada:
        try:
            texto = descargar_texto(catalogada["url"])
            cuerpo = extraer_articulo(texto, articulo) if articulo else texto[:4000]
            res.texto = cuerpo
            # Vigencia: si se pidió un artículo, analizar solo ese artículo (menos falsos positivos).
            res.vigencia = detectar_vigencia(cuerpo if articulo else texto)
            res.fuentes_oficiales.insert(
                0, {"nombre": catalogada["nombre"], "url": catalogada["url"], "busqueda": "directo"})
            res.nota = "Norma resuelta desde el Gestor Normativo (catálogo)."
            return res
        except Exception as e:  # pragma: no cover
            res.nota = f"No se pudo descargar del catálogo ({e}). Usa las fuentes y consultas web."

    res.candidatos = _suin_candidatos(etiqueta)
    if not res.nota:
        res.nota = ("Norma no catalogada: coteja en las fuentes oficiales y verifica VIGENCIA "
                    "(SUIN-Juriscol / Corte Constitucional) antes de citarla como VERIFICADA.")
    return res


if __name__ == "__main__":
    import json

    print(json.dumps(asdict(buscar_constitucion(90)), ensure_ascii=False, indent=2)[:1200])

    for art in [164, 187, 188]:  # caducidad, contenido de la sentencia, costas
        f = buscar_cpaca(art)
        print(f"\n=== {f.norma} - {f.articulo} ===")
        print(f.texto[:800])

    print("\n=== buscar_norma: Ley 1437 de 2011, art. 140 (catálogo) ===")
    r = buscar_norma("Ley", "1437", "2011", articulo=140)
    print("Vigencia:", r.vigencia)
    print(r.texto[:500])

    print("\n=== buscar_norma: Ley 640 de 2001 (no catalogada) ===")
    r2 = buscar_norma("Ley", "640", "2001", tema="conciliación")
    print("Vigencia:", r2.vigencia)
    print("Fuentes oficiales:", len(r2.fuentes_oficiales), "| Consultas web:", len(r2.consultas_web))
    print("Ejemplo de consulta:", r2.consultas_web[0])
    print("Nota:", r2.nota)
