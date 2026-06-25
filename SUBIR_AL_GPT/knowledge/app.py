"""
app.py
------
API FastAPI que el GPT consume vía "Actions". Expone:
- POST /norma                 -> artículo de Constitución o CPACA
- POST /jurisprudencia/samai  -> búsqueda en el Consejo de Estado (SAMAI)
- POST /documento             -> genera .docx (y opcional .pdf) de la providencia
- GET  /salud                 -> healthcheck

Ejecutar:
    uvicorn app:app --reload --port 8000

Para que el GPT lo use debe ser accesible por HTTPS público (ngrok, Render, Railway, etc.).
Ver docs/04_GUIA_DESPLIEGUE.md.
"""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from fuentes_normativas import buscar_constitucion, buscar_cpaca
from generar_documento import crear_word_providencia, convertir_a_pdf
from samai_busqueda import buscar_samai

app = FastAPI(
    title="Orquestador Jurídico Administrativo Colombia",
    version="1.0.0",
    description="Consulta de normas, jurisprudencia y generación de providencias.",
)


class NormaRequest(BaseModel):
    tipo: str  # "cpaca" | "constitucion"
    articulo: int


class JurisprudenciaRequest(BaseModel):
    texto_busqueda: str
    clase_proceso: Optional[str] = None
    tipo_providencia: Optional[str] = "Sentencia"


class DocumentoRequest(BaseModel):
    texto_providencia: str
    titulo: str = "PROYECTO DE PROVIDENCIA"
    generar_pdf: bool = False


@app.get("/salud")
def salud():
    return {"estado": "ok"}


@app.post("/norma")
def norma(req: NormaRequest):
    tipo = req.tipo.lower().strip()
    if tipo == "cpaca":
        return buscar_cpaca(req.articulo).__dict__
    if tipo == "constitucion":
        return buscar_constitucion(req.articulo).__dict__
    return {"error": "El campo 'tipo' debe ser 'cpaca' o 'constitucion'."}


@app.post("/jurisprudencia/samai")
def jurisprudencia_samai(req: JurisprudenciaRequest):
    return {
        "consulta": req.texto_busqueda,
        "aviso": "Resultados sin verificar. Confirme cada providencia en la fuente oficial.",
        "resultados": buscar_samai(
            texto_busqueda=req.texto_busqueda,
            clase_proceso=req.clase_proceso,
            tipo_providencia=req.tipo_providencia,
            headless=True,
        ),
    }


@app.post("/documento")
def documento(req: DocumentoRequest):
    docx = crear_word_providencia(req.texto_providencia, titulo=req.titulo)
    pdf = convertir_a_pdf(docx) if req.generar_pdf else None
    return {"docx": docx, "pdf": pdf}


@app.get("/descargar")
def descargar(path: str):
    return FileResponse(path, filename=path.split("/")[-1])
