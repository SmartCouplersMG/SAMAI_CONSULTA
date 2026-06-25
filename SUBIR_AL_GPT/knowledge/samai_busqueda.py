"""
samai_busqueda.py
-----------------
Búsqueda de providencias en el Buscador de Providencias Tituladas del Consejo de Estado
(SAMAI / Mi Relatoría) usando Playwright.

IMPORTANTE
----------
- SAMAI es una página dinámica (ASP.NET WebForms) cuyos componentes y nombres internos pueden
  cambiar. Este script es un PUNTO DE PARTIDA: localiza un campo de búsqueda visible, escribe la
  consulta, lanza la búsqueda y captura enlaces/textos resultantes. Es probable que necesites
  afinar los selectores tras inspeccionar el sitio.
- Respeta los términos de uso del sitio. Usa headless=False para depurar selectores.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Optional

from playwright.sync_api import sync_playwright

SAMAI_URL = (
    "https://samai.consejodeestado.gov.co/"
    "TitulacionRelatoria/BuscadorProvidenciasTituladas.aspx"
)

# ---------------------------------------------------------------------------
# Fuentes oficiales ALTERNAS a SAMAI (útiles cuando SAMAI no responde).
# Todas son consultables públicamente; preferir siempre fuente oficial.
# ---------------------------------------------------------------------------
FUENTES_JURISPRUDENCIA = [
    {"nombre": "SAMAI - Buscador Providencias Tituladas (preferente)", "url": SAMAI_URL,
     "tipo": "buscador oficial"},
    {"nombre": "Índice oficial de Sentencias de Unificación", "tipo": "índice oficial",
     "url": "https://www.consejodeestado.gov.co/decisiones_u/"},
    {"nombre": "Boletines del Consejo de Estado (PDF oficiales)", "tipo": "repositorio oficial",
     "url": "https://www.consejodeestado.gov.co/documentos/boletines/"},
    {"nombre": "Relatoría / SIDN Rama Judicial", "tipo": "repositorio oficial",
     "url": "https://sidn.ramajudicial.gov.co/"},
    {"nombre": "Gestor Normativo CRA (reproduce providencias íntegras)", "tipo": "gestor normativo",
     "url": "https://normas.cra.gov.co/"},
    {"nombre": "Gestor Normativo CREG", "tipo": "gestor normativo",
     "url": "https://gestornormativo.creg.gov.co/"},
    {"nombre": "Jurinfo - JEP (compilación)", "tipo": "gestor normativo",
     "url": "https://jurinfo.jep.gov.co/normograma/"},
]

# Plantillas de búsqueda web para localizar providencias (adaptar <tema>).
PLANTILLAS_BUSQUEDA = [
    '"Consejo de Estado" "Sección Tercera" <tema> reparación directa radicado sentencia',
    "site:consejodeestado.gov.co <tema> boletín PDF",
    '"sentencia de unificación" <tema> Consejo de Estado radicado',
    "<tema> falla del servicio omisión radicado expediente Sección Tercera",
]

# ---------------------------------------------------------------------------
# Lista CURADA y VERIFICADA de sentencias de UNIFICACIÓN de perjuicios
# (Sección Tercera, 28/08/2014). Reconfirmar radicado/vigencia en fuente
# oficial antes de citar como VERIFICADA en la TVR.
# ---------------------------------------------------------------------------
UNIFICACION_PERJUICIOS = [
    {
        "exp": "26251",
        "tema": "Perjuicios morales (niveles de cercanía afectiva; tope 100 SMLMV)",
        "ponente": "Jaime Orlando Santofimio Gamboa",
        "radicado": "66001-23-31-000-2001-00731-01",
        "fecha": "2014-08-28",
        "url": "https://www.consejodeestado.gov.co/documentos/boletines/151/S3/"
               "66001-23-31-000-2001-00731-01(26251).pdf",
        "validacion": "verificada",
    },
    {
        "exp": "28832",
        "tema": "Perjuicios inmateriales por afectación a bienes/derechos constitucional "
                "y convencionalmente protegidos",
        "ponente": "(Sección Tercera, Sala Plena)",
        "radicado": "25000-23-26-000-2000-00340-01",
        "fecha": "2014-08-28",
        "url": "https://www.consejodeestado.gov.co/documentos/boletines/151/S3/"
               "25000-23-26-000-2000-00340-01(28832).pdf",
        "validacion": "verificada",
    },
    {
        "exp": "31170",
        "tema": "Daño a la salud (regla general)",
        "ponente": "Enrique Gil Botero",
        "radicado": "(por reconfirmar)",
        "fecha": "2014-08-28",
        "url": "https://www.consejodeestado.gov.co/decisiones_u/",
        "validacion": "verificada (tema/ponente); radicado por reconfirmar",
    },
    {
        "exp": "28804",
        "tema": "Daño a la salud temporal (regla de excepción; valoración cualitativa)",
        "ponente": "(Sección Tercera)",
        "radicado": "23001-23-31-000-2001-00278-01",
        "fecha": "2014-08-28",
        "url": "https://www.consejodeestado.gov.co/documentos/boletines/151/S3/"
               "23001-23-31-000-2001-00278-01(28804)%20(1).pdf",
        "validacion": "verificada",
    },
]

# Tope de perjuicios MORALES por nivel (Exp. 26251), en SMLMV. Máximos; graduar con la prueba.
TOPES_MORALES_SMLMV = {1: 100, 2: 50, 3: 35, 4: 25, 5: 15}


def fuentes_jurisprudencia() -> list[dict]:
    """Devuelve las fuentes oficiales (preferente + alternas) para verificar jurisprudencia."""
    return FUENTES_JURISPRUDENCIA


def listar_unificacion_perjuicios() -> list[dict]:
    """Devuelve la lista curada y verificada de unificación de perjuicios."""
    return UNIFICACION_PERJUICIOS


@dataclass
class Providencia:
    titulo: str
    texto_visible: str
    enlace: Optional[str] = None
    validacion: str = "no verificada"  # el GPT/usuario debe confirmar manualmente


def buscar_samai(
    texto_busqueda: str,
    clase_proceso: Optional[str] = None,
    tipo_providencia: Optional[str] = "Sentencia",
    headless: bool = True,
    timeout_ms: int = 60000,
    max_resultados: int = 30,
) -> list[dict]:
    resultados: list[Providencia] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(SAMAI_URL, wait_until="networkidle", timeout=timeout_ms)
        page.wait_for_timeout(3000)

        # 1) Localizar un campo de texto visible y escribir la consulta.
        inputs = page.locator("input:visible")
        filled = False
        for i in range(inputs.count()):
            try:
                inp = inputs.nth(i)
                box = inp.bounding_box()
                if box and box["width"] > 60:
                    inp.fill(texto_busqueda)
                    filled = True
                    break
            except Exception:
                continue

        if not filled:
            browser.close()
            raise RuntimeError(
                "No se encontró un campo de búsqueda visible en SAMAI. "
                "Inspecciona el sitio y ajusta los selectores."
            )

        # 2) Lanzar la búsqueda (botón 'Buscar' o Enter).
        botones = page.get_by_text("Buscar", exact=True)
        if botones.count() > 0:
            botones.first.click()
        else:
            page.keyboard.press("Enter")
        page.wait_for_timeout(6000)

        # 3) Capturar enlaces relevantes.
        links = page.locator("a")
        for i in range(min(links.count(), 200)):
            if len(resultados) >= max_resultados:
                break
            try:
                a = links.nth(i)
                txt = a.inner_text(timeout=1000).strip()
                href = a.get_attribute("href")
                if txt and any(
                    k in txt.lower()
                    for k in ["sentencia", "radicado", "proceso", "providencia", "consejo"]
                ):
                    resultados.append(Providencia(titulo=txt[:300], texto_visible=txt, enlace=href))
            except Exception:
                continue

        # 4) Fallback: bloques de texto si no hubo enlaces claros.
        if not resultados:
            try:
                cuerpo = page.locator("body").inner_text(timeout=10000)
                bloques = [b.strip() for b in cuerpo.split("\n") if len(b.strip()) > 40]
                for b in bloques[:max_resultados]:
                    resultados.append(Providencia(titulo=b[:120], texto_visible=b[:1000]))
            except Exception:
                pass

        browser.close()

    return [asdict(r) for r in resultados]


if __name__ == "__main__":
    data = buscar_samai(
        texto_busqueda='"daño antijurídico" "reparación directa"',
        headless=False,  # ponlo en True una vez afinados los selectores
    )
    print(json.dumps(data, ensure_ascii=False, indent=2))
