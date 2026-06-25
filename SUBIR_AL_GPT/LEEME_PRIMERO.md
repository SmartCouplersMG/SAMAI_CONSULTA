# LÉEME PRIMERO — Cómo cargar este GPT (respetando límites)

Carpeta lista para subir directamente al **GPT Builder** (ChatGPT → Explore GPTs → Create → Configure).

## Paso a paso

| Campo del GPT | Qué hacer | Archivo | Límite | Usado |
|---|---|---|---|---|
| **Name** | Copiar y pegar | `01_TITULO.txt` | 50 | **43** ✅ |
| **Description** | Copiar y pegar | `02_DESCRIPCION.txt` | 300 | **≤300** ✅ |
| **Instructions** | Copiar y pegar todo | `03_INSTRUCCIONES.txt` | 8000 | **7977** ✅ |
| **Knowledge** | Subir los 10 archivos de la carpeta `knowledge/` | ver abajo | 10 archivos | **10** ✅ |
| **Capabilities** | Activar **Web Search**. Activar **Code Interpreter** si quieres generar el Word dentro del chat | — | — | — |
| **Actions** (opcional) | Pegar `openapi_action.yaml` y poner tu URL pública | `knowledge/openapi_action.yaml` | — | — |

## Archivos de conocimiento a subir (carpeta `knowledge/`, 10 de 10)

1. `PROTOCOLO_ESTRICTO.md` — **norma vinculante**: paso a paso estricto del análisis y la sentencia, con **3 gates** infranqueables, checklists ítem por ítem, **método de búsqueda de jurisprudencia (1-TER)**, formatos exactos, autoauditoría y conductas prohibidas. Es el archivo que hace el flujo "a prueba de saltos".
2. `CONTEXTO_METODOLOGIA_AGENTES.md` — flujo completo, agentes, fases, tablas y plantillas (el detalle que no cabe en Instructions).
3. `FUENTES_NORMATIVAS_GUIA.md` — jerarquía de fuentes, enlaces oficiales, matrices y regla anti-alucinación.
4. `JURISPRUDENCIA_UNIFICACION_PERJUICIOS.md` — **lista verificada** de sentencias de unificación de perjuicios (morales, daño a la salud, bienes constitucionales) con radicados y enlaces oficiales, y tabla de topes en SMLMV.
5. `fuentes_normativas.py` — descarga artículos de Constitución y CPACA.
6. `samai_busqueda.py` — búsqueda en SAMAI + **fuentes oficiales alternas** + lista curada de unificación de perjuicios.
7. `generar_documento.py` — genera Word y PDF (sin membrete).
8. `app.py` — API FastAPI para usar vía Actions.
9. `openapi_action.yaml` — esquema de la Action.
10. `requirements.txt` — dependencias.

Knowledge **al tope (10/10)**. Si quieres subir la Constitución o el CPACA en PDF, deberás liberar un espacio (p. ej. fusionar los scripts o no subir `requirements.txt` como conocimiento).

## Notas

- Las **Instrucciones** son el resumen operativo y remiten a los dos `.md` de conocimiento para el
  detalle. Así se respeta el límite de 8000 caracteres sin perder metodología.
- El GPT se detiene en **3 puntos de control humano (GATES)**: GATE 1 tras la decisión de
  admisibilidad, GATE 2 tras el análisis del daño antijurídico, y GATE 3 antes de generar Word/PDF.
- Es una herramienta de **apoyo**: no reemplaza al juez ni a la asesoría jurídica. Verifica cada
  radicado y cada cifra.
- Para montar la API (Actions) y endurecer SAMAI, revisa los comentarios dentro de los scripts.
