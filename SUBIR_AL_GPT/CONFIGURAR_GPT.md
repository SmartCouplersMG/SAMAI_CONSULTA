# CONFIGURAR EL GPT — Checklist final

Todo lo necesario para dejar el GPT funcionando con la consulta a SAMAI.
Sigue los pasos en orden. Tiempo estimado: ~10 minutos.

---

## 0. Antes de empezar
- API en vivo: `https://samai-consulta.onrender.com` (ya desplegada y probada).
- En ChatGPT: abre tu GPT → **Editar GPT** → pestaña **Configurar**.

---

## 1. Nombre y descripción
- **Nombre**: el de `01_TITULO.txt`.
- **Descripción**: la de `02_DESCRIPCION.txt`.

## 2. Instrucciones
- Copia TODO el contenido de `03_INSTRUCCIONES.txt` en el campo **Instrucciones**.
  (Ya incluye el bloque "HERRAMIENTA SAMAI" con consulta continua, validación y
  manejo de errores.)

## 3. Conocimiento (Knowledge) — sube estos archivos
En **Conocimiento → Subir archivos**, carga la carpeta `knowledge/`:
- `PROTOCOLO_ESTRICTO.md`
- `CONTEXTO_METODOLOGIA_AGENTES.md`
- `FUENTES_NORMATIVAS_GUIA.md`
- `JURISPRUDENCIA_UNIFICACION_PERJUICIOS.md`
- **`HERRAMIENTA_SAMAI_API.md`  ← NUEVO: protocolo de uso de la Action SAMAI**

> Los scripts .py de `knowledge/` (app.py, samai_busqueda.py, etc.) NO se suben:
> eran el backend; ya está desplegado en Render. Solo se suben los .md.

## 4. Acción (Action) — la conexión con SAMAI
1. Baja a **Acciones → Crear nueva acción**.
2. En **Esquema**, pega TODO el contenido de `ACCION_SAMAI_openapi.yaml`.
3. Verás aparecer 2 acciones disponibles:
   - `buscarJurisprudencia`
   - `obtenerTextoProvidencia`
4. **Autenticación**: déjala en **Ninguna / None** (la API es pública).
5. (Privacidad) si pide URL de política de privacidad, puedes poner la del repo
   o cualquier URL válida; no afecta el funcionamiento.

> IMPORTANTE: NO pegues el viejo `knowledge/openapi_action.yaml` ni
> `scripts/openapi_action.yaml`: apuntaban a un backend no desplegado
> (`TU-DOMINIO-PUBLICO`) y romperían las llamadas. La única Action válida hoy es
> `ACCION_SAMAI_openapi.yaml`.

## 5. Guardar y probar
- Guarda la acción y luego **Actualizar/Guardar** el GPT.
- Prueba en el panel de vista previa:
  - "Busca jurisprudencia sobre falla del servicio y reparación directa; dame
    radicado, fecha y problema jurídico de 3 providencias."
  - "Trae el texto completo de la primera y resúmela."
- Confirma que el GPT:
  - hace varias búsquedas / pagina si hace falta,
  - cita radicado + fecha + ponente,
  - abre el texto con obtenerTextoProvidencia,
  - y, si algo falla, reintenta antes de rendirse.

---

## 6. (Recomendado) Evitar el "cold start" de Render
El plan gratis duerme el servicio tras ~15 min de inactividad; la primera
llamada tarda ~30-50 s y una Action de ChatGPT puede agotar su tiempo de espera.
Para mantenerlo despierto, crea un "ping" gratuito cada ~10 minutos:

1. Entra a un servicio gratuito de monitoreo/cron, p. ej. **cron-job.org** o
   **UptimeRobot** (crea cuenta gratis).
2. Crea un job que haga **GET** a `https://samai-consulta.onrender.com/`
   cada **10 minutos**.
3. Listo: el servicio se mantiene caliente y las consultas del GPT responden
   rápido.

(Alternativa sin pinger: el bloque de errores ya instruye al GPT a reintentar
una vez, así que igual funciona; el ping solo mejora la velocidad de la 1ª
consulta.)

---

## 7. Estado de las demás funciones (norma / generación Word-PDF)
La consulta de normas (`/norma`, `/norma/buscar`) y la generación de documentos
Word/PDF (`generarDocumento`) del diseño original NO están desplegadas todavía
(su backend `app.py` no se ha subido a un host). Por ahora:
- La verificación de NORMAS se hace por navegación web (SUIN-Juriscol / Gestor
  Normativo), como dicen las instrucciones.
- La generación de Word/PDF queda como mejora futura (habría que desplegar
  `app.py` igual que hicimos con SAMAI).

Si más adelante quieres activarlas, se despliega `app.py` en Render con el mismo
método y se añade una segunda Action.
