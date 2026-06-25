"""
api.py — Envuelve samai.buscar() en un endpoint HTTP (FastAPI) para que un
GPT de ChatGPT lo consuma como Action. Ligero: sin navegador, solo requests.

Local:   uvicorn api:app --reload
Deploy:  cualquier host de Python (Render, Hugging Face Spaces, Vercel, etc.)
"""
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import samai

app = FastAPI(
    title="API Jurisprudencia SAMAI - Consejo de Estado",
    description="Busca providencias tituladas del Consejo de Estado (SAMAI).",
    version="1.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/buscar", operation_id="buscarJurisprudencia")
def buscar(
    consulta: str = Query(..., description='Texto a buscar. Admite frases entre '
                          'comillas y conectores AND/OR/AND NOT. '
                          'Ej: "contrato estatal"'),
    pagina: int = Query(0, ge=0, description="Pagina de resultados (0 = primera). "
                        "10 resultados por pagina."),
    orden: str = Query("FechaProvidencia desc",
                       description="Orden: 'FechaProvidencia desc' (reciente), "
                       "'FechaProvidencia' (antiguo), '' (ranking)."),
):
    """Devuelve providencias del Consejo de Estado que coinciden con la consulta."""
    try:
        return samai.buscar(consulta, pagina=pagina, orderby=orden)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error consultando SAMAI: {e}")


@app.get("/documento", operation_id="obtenerTextoProvidencia")
def documento(
    url_documento: str = Query(..., description="El campo 'url_documento' de un "
                              "resultado de /buscar. Devuelve el texto completo "
                              "de la providencia. Llamar poco despues de buscar "
                              "(el enlace caduca)."),
):
    """Descarga y extrae el texto completo (PDF) de una providencia."""
    try:
        return samai.obtener_texto(url_documento)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"No se pudo obtener el texto: {e}")


@app.get("/")
def health():
    return {"status": "ok", "servicio": "SAMAI jurisprudencia"}
