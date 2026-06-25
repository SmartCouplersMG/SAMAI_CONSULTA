# HERRAMIENTA SAMAI (API en vivo) — Protocolo de uso obligatorio

Este documento rige CÓMO el GPT consulta jurisprudencia del Consejo de Estado a
través de la Action conectada al servicio propio. Es norma operativa: ante
conflicto con métodos genéricos de búsqueda, prevalece este protocolo para todo
lo que sea SAMAI. Complementa (no reemplaza) la regla "≥2 fuentes" de F2/F4 y la
TVR de PROTOCOLO_ESTRICTO.md.

## 1. Qué hace la herramienta

Servicio propio desplegado en: `https://samai-consulta.onrender.com`
(la Action ya apunta ahí; el GPT NO arma URLs a mano, solo invoca las acciones).

Dos acciones:

- **buscarJurisprudencia(consulta, pagina, orden)** → devuelve hasta 10
  providencias por página, cada una con: `radicado`, `interno`, `clase_proceso`,
  `fecha_providencia`, `ponente`, `sala`, `actor`, `demandado`,
  `tipo_providencia`, `problema_juridico`, `url_proceso` y `url_documento`.
  También `total_paginas` (cuántas páginas hay) y `resultados_en_pagina`.
- **obtenerTextoProvidencia(url_documento)** → devuelve el TEXTO COMPLETO del
  fallo (`texto`, `paginas`, `url_pdf`). Se le pasa el `url_documento` tal cual
  vino en un resultado de buscarJurisprudencia.

Origen: portal oficial SAMAI. Lo que devuelve buscarJurisprudencia es FUENTE
OFICIAL, pero sigue exigiendo control de pertinencia (ver §4).

## 2. Cuándo usarla

- Siempre que se necesite jurisprudencia del Consejo de Estado (F2 daño
  antijurídico, F3 valoración si aplica, F4 proyecto de providencia, y cualquier
  verificación de una providencia citada).
- Para VERIFICAR una providencia que el usuario o un agente menciona (busca por
  radicado o por tesis y confirma que existe en SAMAI).
- NO inventes nunca radicado, fecha, ponente o tesis. Si la herramienta no
  devuelve respaldo, la referencia queda NO VERIFICADA (regla CERO INVENCIÓN).

## 3. Protocolo de CONSULTA CONTINUA (no te quedes con una sola llamada)

Una sola búsqueda casi nunca basta. Para construir línea jurisprudencial:

1. **Lanza varias búsquedas con formulaciones distintas** del mismo problema
   jurídico: (a) frase exacta entre comillas (`"reparación directa" "falla del
   servicio"`); (b) sinónimos/variantes; (c) términos clave sueltos si la frase
   exacta da poco. Combina con conectores cuando ayuden.
2. **Pagina** cuando el primer lote no traiga suficientes resultados pertinentes:
   repite la misma consulta con `pagina = 1, 2, …` hasta reunir 2-3 providencias
   pertinentes (revisa `total_paginas` para saber cuánto hay).
3. **Ordena** según convenga: `FechaProvidencia desc` (más reciente, default),
   `FechaProvidencia` (más antigua, útil para hitos), `` vacío (ranking de
   coincidencia, útil cuando importa la relevancia textual).
4. **Para cada providencia candidata relevante, abre su texto** con
   obtenerTextoProvidencia y confirma que realmente resuelve el problema (no te
   fíes solo del `problema_juridico` resumido).
5. **Reúne mínimo 2-3 providencias** que conformen la línea, no una sola.
   Si el caso toca perjuicios, cruza además con
   JURISPRUDENCIA_UNIFICACION_PERJUICIOS.md.

Detente de iterar cuando: tengas 2-3 providencias verificadas y pertinentes, o
hayas agotado formulaciones razonables (≥3 búsquedas distintas + paginación) sin
hallazgos. En ese segundo caso, declara el vacío (no inventes).

## 4. VALIDACIÓN de cada providencia antes de citarla

Una providencia solo puede usarse como fundamento si pasa los 3 filtros:

1. **Existencia**: vino de buscarJurisprudencia (fuente oficial SAMAI) con
   `radicado`, `fecha_providencia` y `ponente` no vacíos.
2. **Pertinencia**: su texto (vía obtenerTextoProvidencia) trata el mismo
   problema jurídico del caso; cita la ratio decidendi real, no el resumen.
3. **Aplicabilidad**: el supuesto fáctico/normativo es análogo al caso.

Registra cada una en la **TVR** (formato en PROTOCOLO_ESTRICTO.md 1-BIS):
`ID | Tipo=Jurisprudencia | Referencia=radicado + fecha + ponente |
Fuente=url_proceso o url_documento | Validación=VERIFICADA | Aplicabilidad | Por
qué se cita`. Una providencia citada pero NO abierta/confirmada se marca NO
VERIFICADA y no puede ser fundamento decisivo.

## 5. MANEJO DE ERRORES (qué hacer si la herramienta falla)

El servicio es gratuito y SAMAI a veces cae; planifica para el fallo:

| Síntoma | Causa probable | Acción del GPT |
|---|---|---|
| La primera llamada tarda mucho o da error de tiempo/5xx | Servicio "dormido" (cold start ~30-50 s) | **Reintenta UNA vez** la misma acción tras unos segundos. La 2ª suele funcionar. |
| Error 502 con detalle "Error consultando SAMAI" | Portal SAMAI caído/lento | Reintenta 1 vez. Si persiste, NO te bloquees: pasa a fuentes oficiales alternas (boletines y unificación de consejodeestado.gov.co, Relatoría ramajudicial.gov.co) por navegación web, y deja constancia. |
| `resultados` vacío (`resultados_en_pagina: 0`) | La consulta no coincidió | Reformula: quita comillas, usa sinónimos, separa términos, prueba `orden` vacío (ranking). Intenta ≥2 reformulaciones antes de concluir "sin resultados". |
| obtenerTextoProvidencia falla o da 502 | El `url_documento` caducó (enlaces de vida corta) | **Vuelve a llamar buscarJurisprudencia** para obtener un `url_documento` fresco y reintenta UNA vez. |
| Tras todo lo anterior, sigue sin haber respaldo | — | Aplica CERO INVENCIÓN: declara "No se encontró validación suficiente en fuente oficial" y, en sentencia de fondo, "VACÍO JURISPRUDENCIAL NO RESUELTO" (GATE 3). Nunca inventes la providencia. |

Reglas de oro ante error:
- Nunca presentes como verificado algo que la herramienta no confirmó.
- Nunca abandones la búsqueda al primer fallo: reintento → reformulación →
  fuente alterna → declaración de vacío, en ese orden.
- Informa al usuario, con transparencia, qué intentaste y qué resultó.

## 6. Sintaxis de `consulta` y modo de búsqueda (verificado empíricamente)

Las comillas y los conectores SÍ acotan; el truco es usar términos específicos.
Cifras reales medidas contra SAMAI (nº de páginas de resultados):

- **Comillas = frase exacta, fuerte filtro:** `"falla del servicio"` → 722 págs;
  sin comillas `falla del servicio` → 1942 págs. **Usa SIEMPRE comillas** para
  frases jurídicas.
- **`AND` = intersección real:** `"privación injusta de la libertad"` → 444 págs;
  `… AND "error judicial"` → **75 págs**. El AND filtra de verdad cuando los
  términos son distintivos (no ubicuos). Con frases muy comunes que casi siempre
  coexisten (p. ej. "falla del servicio" + "reparación directa") apenas acota:
  no es que falle, es que ambos términos están en casi todo. En ese caso, agrega
  un tercer término más específico del caso.
- **`AND NOT` = exclusión real:** `… AND NOT "absolución"` reduce de 444 a 299.
- Conectores en MAYÚSCULAS: `AND`, `OR`, `AND NOT`.

Parámetro `modo` de la acción (controla la lógica entre términos):
- **`modo=all` (por defecto) = AND**: exige todos los términos. Es lo más preciso;
  úsalo casi siempre.
- **`modo=any` = OR**: basta cualquiera de los términos (amplía mucho:
  "falla del servicio" pasa de 722 a 2643 págs). Úsalo SOLO para AMPLIAR cuando
  una búsqueda `all` quedó vacía o con muy pocos resultados.
- Otros valores (exact, phrase, boolean…) NO son válidos: devuelven 0 resultados.

Estrategia recomendada de precisión:
1. Empieza con 2 frases núcleo entre comillas en `modo=all` (AND).
2. Si hay demasiados resultados poco pertinentes, **añade un término más
   específico del caso** (no bajes a términos genéricos).
3. Si hay muy pocos o ninguno, **quita un término** o cambia a `modo=any` (OR), o
   usa `orden` vacío (ranking) para que lo más relevante suba primero.
4. Pase lo que pase, CONFIRMA pertinencia abriendo el texto (§4): la lista nunca
   basta para citar.
- Llama obtenerTextoProvidencia poco después de buscar (los enlaces caducan).
