# Fuentes, normativa y verificación — Orquestador de Providencias Administrativas (Colombia)

> Archivo de conocimiento del GPT. Define la jerarquía de fuentes, los enlaces oficiales, las
> matrices de registro y las reglas anti-alucinación.

---

## 1. Jerarquía de fuentes (de mayor a menor)

1. **Constitución Política de Colombia** — en especial **art. 90** (responsabilidad patrimonial
   del Estado por daños antijurídicos imputables a la acción u omisión de autoridades públicas).
2. **CPACA — Ley 1437 de 2011** y sus reformas vigentes.
3. **Jurisprudencia del Consejo de Estado**, validada en SAMAI / Mi Relatoría.
4. **Jurisprudencia constitucional** (derechos fundamentales, debido proceso, acceso a la
   administración de justicia, igualdad, dignidad, reparación integral).
5. **Código General del Proceso** — supletorio en lo probatorio/procesal cuando el CPACA remita
   o no regule.
6. **Normativa especial** del caso: contratación estatal, responsabilidad médica estatal, fuerza
   pública, servicios públicos, función pública, ambiente, tributario, urbanismo, etc.

---

## 2. Enlaces oficiales

| Fuente | URL |
|---|---|
| CPACA (Ley 1437 de 2011) — Gestor Normativo | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=41249 |
| Constitución Política — Gestor Normativo | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=4125 |
| Buscador de Providencias Tituladas (Consejo de Estado / SAMAI) | https://samai.consejodeestado.gov.co/TitulacionRelatoria/BuscadorProvidenciasTituladas.aspx |

### 2.1 Portales oficiales para BUSCAR y VERIFICAR LEYES Y DECRETOS en la web

> La búsqueda web de normas **complementa** los PDF cargados y permite comprobar **vigencia**
> (que la norma no esté derogada/modificada/declarada inexequible). Verificar toda norma en
> ≥1 fuente oficial antes de citarla como `VERIFICADA`.

| Portal | URL | Para qué |
|---|---|---|
| **SUIN-Juriscol (MinJusticia)** | https://www.suin-juriscol.gov.co/ | **Preferente para vigencia** y afectaciones normativas; leyes, decretos, actos legislativos (fuente: Diario Oficial) |
| Gestor Normativo — Función Pública | https://www.funcionpublica.gov.co/eva/gestornormativo/ | Texto de normas (lo usa la Action `consultarNorma`) |
| Secretaría del Senado (basedoc) | http://www.secretariasenado.gov.co/ | Texto de leyes con notas de vigencia |
| Sección de Leyes del Senado | https://leyes.senado.gov.co/ | Leyes por legislatura |
| DAPRE — Presidencia | https://dapre.presidencia.gov.co/normativa/ | Leyes y decretos del Ejecutivo |
| Diario Oficial — Imprenta Nacional | (consulta del Diario Oficial) | Publicación oficial (existencia/fecha) |
| Corte Constitucional — Relatoría | https://www.corteconstitucional.gov.co/relatoria/ | Si una norma fue declarada inexequible o condicionada |

**Regla de vigencia:** si la norma está derogada/modificada/inexequible, decirlo y aplicar la
norma vigente que la sustituye; nunca citar la derogada como fundamento. El método y las
plantillas de búsqueda están en `PROTOCOLO_ESTRICTO.md` (sección 1-QUATER).

**Actions disponibles (si montas la API):**
- `consultarNorma` (POST /norma): trae un artículo del CPACA o la Constitución.
- `buscarNorma` (POST /norma/buscar): resuelve **cualquier ley/decreto** (tipo, número, año,
  artículo, tema). Si está catalogada, devuelve el texto del Gestor Normativo; en todo caso
  devuelve las **fuentes oficiales**, **consultas web** listas para usar y un **chequeo
  heurístico de vigencia** (que debe confirmarse en SUIN-Juriscol / Corte Constitucional).

---

## 3. Artículos del CPACA frecuentemente útiles por fase

> Verificar el número y el texto vigente en la fuente oficial antes de citar (la numeración puede
> variar por reformas). Lista orientativa, no exhaustiva.

- **Admisibilidad / demanda:** contenido de la demanda, anexos, inadmisión y subsanación,
  rechazo, traslado.
- **Caducidad:** términos según el medio de control.
- **Medios de control:** nulidad, nulidad y restablecimiento del derecho, reparación directa,
  controversias contractuales, entre otros.
- **Pruebas:** oportunidad, decreto, práctica, contradicción y valoración.
- **Sentencia:** contenido, congruencia, motivación, costas.

---

## 4. Regla anti-alucinación (CRÍTICA)

- **No inventar** providencias, radicados, fechas, consejeros ponentes ni tesis.
- Si no se verifica una providencia en fuente oficial, escribir literalmente:
  > "No se encontró validación suficiente en fuente oficial; no se usará como fundamento decisivo."
- Verificar con la Action (`buscarJurisprudencia`/`consultarNorma`) o navegación web. Si no es
  posible, marcar la fuente como **"no verificada"** y usarla solo como **persuasiva**.
- Una providencia citada como **decisiva** debe tener radicado verificado y enlace.

---

## 5. Matrices de registro

**Fuente jurisprudencial** (una por providencia):
Fuente No. · Corporación · Sala/Sección/Subsección · Fecha · Radicado · Consejero ponente ·
Tipo de providencia · Tema · Problema jurídico · Tesis · Ratio decidendi aplicable · Enlace ·
Validación (verificada/no verificada) · Nivel de confianza (alta/media/baja).

**Fuente normativa** (una por norma):
Norma · Artículo · Texto relevante resumido · Aplicación al caso · Fuente oficial ·
Vigencia/observación.

---

## 6. Conocimiento adicional recomendado (si lo cargas como archivos)

Por límite de 10 archivos, prioriza: (a) Constitución, (b) CPACA, (c) un MD propio de líneas
jurisprudenciales **verificadas** del Consejo de Estado por tema (falla del servicio, daño
especial, riesgo excepcional, privación injusta de la libertad, responsabilidad médica estatal).
No incluir sentencias inventadas; solo las verificadas con radicado y enlace. Preferir PDFs con
texto seleccionable (no escaneados sin OCR) y anotar fecha de descarga para trazabilidad.
