# Orquestador de Providencias Administrativas Colombia — Paquete del GPT

Este paquete contiene **todo lo que debes subir/configurar** para montar un GPT personalizado
(en ChatGPT → *Explore GPTs* → *Create*) que actúa como **orquestador jurídico** para redactar
proyectos de **autos interlocutorios** y **sentencias** en procesos contencioso-administrativos colombianos.

> ⚠️ **Aviso legal.** El GPT produce **borradores de apoyo** para revisión humana. No es un juez,
> no profiere providencias con efectos jurídicos y no sustituye asesoría profesional. Toda salida
> debe ser revisada y validada por un abogado o funcionario competente.

---

## 1. Qué subir a cada parte del GPT Builder

| Campo del GPT Builder | Archivo a usar |
|---|---|
| **Name (Título)** | `docs/01_TITULO_DESCRIPCION.md` |
| **Description (Descripción)** | `docs/01_TITULO_DESCRIPCION.md` |
| **Instructions (Prompt maestro)** | `docs/02_INSTRUCCIONES_MAESTRAS.md` (pegar completo) |
| **Knowledge (Archivos de conocimiento)** | Todo lo que pongas en `knowledge/` (ver `docs/05_GUIA_KNOWLEDGE.md`) |
| **Actions (esquema OpenAPI)** | `scripts/openapi_action.yaml` |
| **Capabilities** | Activar *Web Browsing*, *Code Interpreter & Data Analysis*. Ver guía de despliegue. |

---

## 2. Estructura de la carpeta

```
gpt_orquestador_admin/
├── README.md                         ← este archivo (índice)
├── docs/
│   ├── 01_TITULO_DESCRIPCION.md      ← título + descripción del GPT
│   ├── 02_INSTRUCCIONES_MAESTRAS.md  ← PROMPT que va en "Instructions"
│   ├── 03_FLUJO_AGENTES.md           ← explicación del flujo y los agentes
│   ├── 04_GUIA_DESPLIEGUE.md         ← cómo montar API + Actions paso a paso
│   ├── 05_GUIA_KNOWLEDGE.md          ← qué archivos cargar como conocimiento
│   └── 06_CRITICA_Y_MEJORAS.md       ← crítica honesta + oportunidades de mejora
├── scripts/
│   ├── app.py                        ← API FastAPI (norma + jurisprudencia)
│   ├── fuentes_normativas.py         ← descarga Constitución y CPACA
│   ├── samai_busqueda.py             ← scraping del buscador del Consejo de Estado
│   ├── generar_documento.py          ← genera Word (.docx) y PDF, SIN membrete
│   ├── openapi_action.yaml           ← esquema de la Action del GPT
│   └── requirements.txt              ← dependencias Python
├── knowledge/                        ← (vacía) coloca aquí los PDFs/MD de soporte
├── templates/                        ← (vacía) plantillas Word/membrete a futuro
└── output/                           ← (vacía) salida de documentos generados
```

---

## 3. Arranque rápido (local)

```bash
cd gpt_orquestador_admin/scripts
pip install -r requirements.txt
playwright install chromium

# Probar generación de Word (sin membrete)
python generar_documento.py

# Levantar la API que consume el GPT vía Actions
uvicorn app:app --reload --port 8000
```

---

## 4. Regla de oro del flujo

El GPT **nunca** salta de la demanda directamente a la sentencia. Se detiene **obligatoriamente** en:

1. Después del **análisis del daño antijurídico** (pide aprobación del usuario).
2. Después de la **valoración probatoria** y antes de generar Word/PDF (pide visto bueno).

Esto evita providencias bien redactadas pero jurídicamente débiles.

Lee la **crítica y oportunidades de mejora** en `docs/06_CRITICA_Y_MEJORAS.md`.
