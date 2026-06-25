# Buscador de Jurisprudencia SAMAI → herramienta para GPT

Consulta providencias del **Consejo de Estado** (sistema SAMAI) y expone los
resultados como una API que un GPT de ChatGPT consume vía **Action**.

## Cómo funciona (hallazgo clave)

La página de resultados de SAMAI responde por **GET directo** con el parámetro
`BusquedaDictionary` (un JSON en el query string). No hace falta Playwright,
navegador, ViewState ni postbacks: basta `requests` + `BeautifulSoup`.

```
GET .../ResultadoBuscadorProvidenciasTituladas.aspx?BusquedaDictionary={...JSON...}
```

## Archivos

| Archivo | Qué es |
|---------|--------|
| `samai.py` | Cliente/scraper. Función `buscar(consulta, pagina, orderby)` → JSON |
| `api.py` | API FastAPI que envuelve `buscar()` en `GET /buscar` |
| `openapi.yaml` | Esquema para pegar como Action en el GPT (cambiar `servers.url`) |
| `requirements.txt` | Dependencias (ligeras, sin navegador) |
| `probe_samai.py`, `test_*.py` | Scripts de reconocimiento/validación |

## Probar en local

```bash
pip install -r requirements.txt
python samai.py '"contrato estatal" AND nulidad'   # prueba el scraper
uvicorn api:app --reload                            # levanta la API en :8000
# luego: http://localhost:8000/buscar?consulta="contrato estatal"
```

## Desplegar gratis (elige uno)

- **Render** (free web service): conecta el repo, build `pip install -r requirements.txt`,
  start `uvicorn api:app --host 0.0.0.0 --port $PORT`.
- **Hugging Face Spaces** (free, SDK Docker o FastAPI): sube los archivos, expón el puerto.

Tras desplegar, copia la URL pública en `openapi.yaml` (`servers.url`).

## Conectar al GPT

1. En ChatGPT → *Editar GPT* → *Crear nueva acción*.
2. Pega el contenido de `openapi.yaml` (con la URL real).
3. Guarda. El GPT ya puede llamar `buscarJurisprudencia`.

## Flujo del GPT (dos herramientas)

1. `buscarJurisprudencia` → 10 resultados/página con metadatos + `url_documento`.
2. `obtenerTextoProvidencia(url_documento)` → **texto completo** del fallo.
   Cadena interna: visor `VerProvidencia.aspx` → URL firmada del PDF en Azure
   Blob → descarga → extracción de texto con `pypdf`.

El GPT busca, elige la providencia relevante y pide su texto. Los enlaces
(`url_documento` y el SAS del blob) son de **vida corta**: usarlos enseguida.

## Pendientes / afinación

- Ajustar sintaxis de conectores `AND/OR/AND NOT` (validar contra SAMAI).
- OCR opcional para providencias escaneadas (PDF sin capa de texto).
- Respetar *rate limiting* y términos de uso del portal.
