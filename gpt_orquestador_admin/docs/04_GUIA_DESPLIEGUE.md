# Guía de despliegue paso a paso

Tienes **dos formas** de operar el GPT. Empieza por la A (más simple) y pasa a la B cuando
necesites scraping de SAMAI confiable y generación de archivos automatizada.

---

## Opción A — GPT con Code Interpreter (sin servidor propio)

La más rápida para empezar. El GPT usa navegación web + el intérprete de código para correr el
script de Word dentro del propio chat.

1. ChatGPT → **Explore GPTs** → **Create** → pestaña **Configure**.
2. **Name**: pega el título de `docs/01_TITULO_DESCRIPCION.md`.
3. **Description**: pega la descripción del mismo archivo.
4. **Instructions**: pega TODO el contenido de `docs/02_INSTRUCCIONES_MAESTRAS.md`.
5. **Capabilities**: activa **Web Browsing** y **Code Interpreter & Data Analysis**.
6. **Knowledge**: sube los archivos de `knowledge/` (ver `05_GUIA_KNOWLEDGE.md`) y, además,
   sube `scripts/generar_documento.py` para que el GPT pueda ejecutarlo y producir el `.docx`.
7. Guarda. Prueba pegando una demanda de ejemplo en texto plano.

**Limitaciones de A:** SAMAI es dinámica y la navegación web del GPT puede no rendir bien;
verifica manualmente cada providencia. La generación de PDF puede requerir el paso por LibreOffice
(no siempre disponible en el sandbox): en ese caso entrega `.docx` y convierte el PDF aparte.

---

## Opción B — GPT con Actions (servidor propio con FastAPI)

Recomendada para uso serio. Tú alojas la API (`scripts/app.py`) y el GPT la llama.

### B.1 Levantar la API localmente

```bash
cd gpt_orquestador_admin/scripts
pip install -r requirements.txt
playwright install chromium
uvicorn app:app --reload --port 8000
```

Verifica: abre `http://localhost:8000/salud` → debe responder `{"estado":"ok"}`.
Documentación interactiva: `http://localhost:8000/docs`.

### B.2 Exponerla por HTTPS público

Opción rápida (pruebas): **ngrok**
```bash
ngrok http 8000
```
Copia la URL `https://....ngrok-free.app`.

Opción estable (producción): despliega en **Render**, **Railway**, **Fly.io** o un VPS.
Recuerda instalar también el navegador de Playwright en el contenedor
(`playwright install --with-deps chromium`).

### B.3 Conectar la Action en el GPT

1. En **Configure** → **Actions** → **Create new action**.
2. Pega el contenido de `scripts/openapi_action.yaml` en el editor de schema.
3. Reemplaza `https://TU-DOMINIO-PUBLICO` por tu URL pública real.
4. Authentication: **None** para pruebas; añade API key/OAuth para producción.
5. Guarda. El GPT ya puede invocar `consultarNorma`, `buscarJurisprudencia` y `generarDocumento`.

### B.4 Endurecer SAMAI

`samai_busqueda.py` trae selectores genéricos. Para resultados fiables:
1. Corre `python samai_busqueda.py` con `headless=False` y observa la página.
2. Inspecciona (F12) los IDs reales de los campos (ASP.NET suele usar IDs largos tipo
   `ctl00$...`) y reemplaza la heurística por selectores exactos.
3. Considera capturar el enlace al PDF de cada providencia para citarlo.

---

## Checklist de verificación

- [ ] El GPT muestra el descargo de responsabilidad al iniciar un caso.
- [ ] Se detiene tras el análisis del daño antijurídico y pide aprobación.
- [ ] Se detiene antes de generar Word/PDF y pide visto bueno.
- [ ] No cita jurisprudencia sin matriz completa.
- [ ] Marca como "no verificada" toda fuente que no pudo confirmar.
- [ ] Genera `.docx` legible (Times New Roman 12, justificado, numeración de página).
