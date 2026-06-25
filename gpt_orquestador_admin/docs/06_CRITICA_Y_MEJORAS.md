# Crítica honesta y oportunidades de mejora

Esta es la parte más importante para que no te lleves una falsa sensación de seguridad.
El paquete es una buena base, pero tiene riesgos reales. Te los pongo sin adornos.

---

## 1. Riesgos jurídicos y conceptuales (los más serios)

1. **Un LLM no "valida" jurisprudencia; la parafrasea.** Aunque el prompt prohíbe inventar,
   los modelos alucinan radicados y tesis con altísima verosimilitud. El control real es el
   scraping a SAMAI + verificación humana. Mientras eso no esté sólido, trata TODA cita como
   sospechosa. **Mitigación:** ninguna providencia debe firmarse sin contrastar cada radicado
   en la fuente oficial.

2. **Frontera ética y de responsabilidad.** Generar "sentencias" roza el ejercicio del derecho
   y la función judicial. El producto debe quedar enmarcado como **borrador de apoyo** y el
   descargo de responsabilidad debe ser visible, no decorativo. Considera limitarlo a
   "proyecto de providencia para revisión".

3. **El consenso entre agentes es teatro, no garantía.** Los tres agentes son el mismo modelo
   con distintos sombreros. Su "conciliación" no aporta independencia real; puede reforzar el
   mismo error en las tres voces. **Mitigación:** usa el Agente 3 con instrucciones
   deliberadamente adversariales (buscar por qué el fallo es nulo), no confirmatorias.

4. **Cuantificación de perjuicios.** Liquidar (SMLMV, perjuicios morales en salarios mínimos,
   daño a la salud, lucro cesante con fórmulas actuariales) es terreno minado para un LLM.
   El prompt prohíbe inventar cifras, pero el riesgo de error de cálculo es alto.
   **Mejora:** mover la liquidación a un módulo de cálculo determinista (Python), no al texto.

5. **Caducidad y competencia mal calculadas = nulidad.** Son cuentas de fechas y reglas de
   reparto; el LLM se equivoca con fechas. **Mejora:** validar caducidad con código
   (fecha del daño/ejecutoria + término legal), no con prosa.

---

## 2. Riesgos técnicos

6. **SAMAI es frágil.** El script de Playwright usa heurística de "primer input visible". En
   cuanto cambie el HTML, deja de funcionar. **Mejora:** selectores exactos, manejo de
   `__VIEWSTATE` de ASP.NET, reintentos, y caché local de resultados.

7. **Extracción de artículos por regex.** `extraer_articulo` asume "ARTÍCULO N ... ARTÍCULO N+1".
   Falla con artículos derogados, con parágrafos numerados o numeración no consecutiva.
   **Mejora:** parsear por estructura del DOM y mantener un índice fijo de artículos clave.

8. **PDF depende de LibreOffice.** `convertir_a_pdf` requiere `soffice` instalado. En el sandbox
   de ChatGPT puede no existir. **Mejora:** usar `docx2pdf` (Windows/Word) o renderizar el PDF
   directamente con `reportlab`/`weasyprint` desde HTML.

9. **Sin tests, sin manejo de errores fino.** Los scripts no tienen pruebas ni reintentos ante
   timeouts de red. **Mejora:** agregar `pytest`, timeouts configurables y logging.

10. **Seguridad de la Action.** El ejemplo usa autenticación `None` y un endpoint `/descargar`
    que recibe una ruta arbitraria (riesgo de *path traversal*). **Mejora:** API key, validar y
    encerrar rutas dentro de `output/`, rate limiting.

---

## 3. Vacíos funcionales

11. **No hay manejo de adjuntos reales.** La entrada es "texto plano", pero las demandas vienen
    en PDF con anexos. **Mejora:** ingesta de PDF + OCR antes de la Fase 0.

12. **No distingue medios de control con finura.** Nulidad y restablecimiento, reparación
    directa, controversias contractuales, nulidad simple, etc., tienen reglas propias de
    caducidad y procedibilidad. El prompt lo menciona pero no lo modela por tipo.
    **Mejora:** sub-flujos por medio de control.

13. **Conciliación prejudicial como requisito.** Se nombra, pero no se fuerza su verificación
    como causal de inadmisión cuando aplica. **Mejora:** checklist duro en Fase 1.

14. **Trazabilidad y versionado.** No se guarda historial de versiones de la providencia ni de
    las fuentes usadas. **Mejora:** registrar cada versión y su matriz de fuentes en `output/`.

15. **Sin métrica de calidad.** No hay forma de medir si un borrador es bueno. **Mejora:**
    rúbrica de evaluación (congruencia, fundamento, prueba) y un set de casos de prueba con
    resultado esperado.

---

## 4. Mejoras de producto (priorizadas)

| Prioridad | Mejora | Impacto |
|---|---|---|
| 🔴 Alta | Verificación obligatoria de cada radicado contra SAMAI antes de citar | Evita alucinaciones citables |
| 🔴 Alta | Cálculo determinista de caducidad y de liquidación de perjuicios | Evita nulidades y errores de cifra |
| 🔴 Alta | Ingesta de PDF + OCR de la demanda y anexos | Entrada realista |
| 🟠 Media | Selectores SAMAI exactos + caché + reintentos | Robustez del scraping |
| 🟠 Media | Generación de PDF sin LibreOffice (weasyprint/reportlab) | Portabilidad |
| 🟠 Media | Sub-flujos por medio de control | Precisión procesal |
| 🟢 Baja | Membrete configurable por usuario (logo/encabezado/sello) | Presentación |
| 🟢 Baja | Tests automatizados + logging | Mantenibilidad |
| 🟢 Baja | Panel de versiones y trazabilidad de fuentes | Auditoría |

---

## 5. Veredicto

- **Como asistente de borrador y estructuración:** muy útil. Acelera el armado de la providencia,
  obliga a un método y deja dos puntos de control humano bien ubicados.
- **Como "juez" o fuente de verdad jurisprudencial:** no confíes. El eslabón débil es la
  verificación de fuentes y los cálculos. Hasta endurecer SAMAI y los módulos deterministas,
  el humano sigue siendo el responsable de cada cita y cada cifra.

Regla mental para el usuario final: **el GPT redacta, tú respondes.**
