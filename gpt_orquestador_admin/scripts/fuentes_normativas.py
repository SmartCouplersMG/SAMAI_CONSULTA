"""
fuentes_normativas.py
---------------------
Descarga y extrae artículos de la Constitución Política y del CPACA (Ley 1437 de 2011)
desde el Gestor Normativo de la Función Pública.

NOTA: la extracción depende de la estructura HTML del sitio oficial; si cambia, ajusta
`extraer_articulo`. El script es un punto de partida robusto, no una garantía absoluta.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict

import requests
from bs4 import BeautifulSoup

CPACA_URL = "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=41249"
CONSTITUCION_URL = "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=4125"

HEADERS = {"User-Agent": "Mozilla/5.0 GPT-Orquestador-Juridico/1.0"}


@dataclass
class FuenteNormativa:
    norma: str
    articulo: str
    texto: str
    url: str


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


if __name__ == "__main__":
    import json

    print(json.dumps(asdict(buscar_constitucion(90)), ensure_ascii=False, indent=2)[:1500])
    for art in [161, 162, 164, 166, 211, 212]:  # ejemplos: requisitos, caducidad, pruebas
        f = buscar_cpaca(art)
        print(f"\n=== {f.norma} - {f.articulo} ===")
        print(f.texto[:1200])
