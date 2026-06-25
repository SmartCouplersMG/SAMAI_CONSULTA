# Flujo de agentes y puntos de control

## Diagrama del flujo

```
        [ DEMANDA EN TEXTO PLANO ]
                   │
                   ▼
        Fase 0 · Extracción de datos
                   │
                   ▼
        Fase 1 · Control de admisibilidad ───► ¿Admite?
                   │                              │ NO
                   │ SÍ                           ▼
                   │                   Proyecto de AUTO (inadmite /
                   │                   rechaza / remite) → FIN
                   ▼
        Fase 2 · Análisis del DAÑO ANTIJURÍDICO
            Agente 1 (D. Administrativo) ─┐
            Agente 2 (Jurisprudencia) ────┤ concilian
                   │                       │
                   ▼                       ▼
            ⛔ PUNTO DE CONTROL 1: aprobación del usuario
                   │ (aprueba o modifica)
                   ▼
        Fase 3 · Valoración PROBATORIA (CPACA, cap. pruebas)
                   │
                   ▼
        Fase 4 · Proyecto de SENTENCIA / AUTO
                   │
                   ▼
        Fase 5 · Opiniones: parte demandante / demandada
                   │
                   ▼
        Fase 6 · Agente 3 (Juez validador) → Aprobado / con ajustes / no
                   │
                   ▼
            ⛔ PUNTO DE CONTROL 2: visto bueno del usuario
                   │ (aprueba o modifica)
                   ▼
        Fase 8 · Generación WORD + PDF (con/sin membrete)
                   │
                   ▼
              [ SALIDA: .docx + .pdf ]
```

## Roles resumidos

| Agente | Función | Salida clave |
|---|---|---|
| **A1 — Derecho Administrativo** | Admisibilidad, régimen de responsabilidad, elementos del daño | Concepto técnico-procesal |
| **A2 — Jurisprudencia** | Línea jurisprudencial del Consejo de Estado, ratio decidendi | Matriz de providencias verificadas |
| **A3 — Juez validador** | Control de fuentes, motivación y congruencia | Veredicto: aprobado / ajustes / no |
| **Rep. demandante** | Defiende prosperidad de pretensiones | Opinión sustentada |
| **Rep. demandada** | Defiende excepciones / falta de prueba | Opinión sustentada |

## Por qué dos puntos de control humanos

- **Control 1 (tras daño antijurídico):** evita gastar esfuerzo en pruebas y redacción si el
  análisis de fondo está mal encuadrado. El usuario corrige el régimen, los hechos o el enfoque.
- **Control 2 (antes de generar documentos):** evita producir un PDF "definitivo" con errores.
  El usuario aprueba o edita el texto antes de materializarlo.

Estos dos `stops` son la salvaguarda central contra "providencias bonitas pero jurídicamente
débiles".

## Posibles desenlaces (todos válidos como salida)

1. **Auto inadmisorio / de rechazo** (no supera Fase 1).
2. **Sentencia inhibitoria** (falta presupuesto procesal advertido tarde).
3. **Sentencia que niega pretensiones** (no probado daño/imputación/nexo o perjuicio).
4. **Sentencia condenatoria** (concurren los elementos y hay prueba suficiente).
5. **Auto que decreta pruebas** (faltan pruebas para decidir de fondo).
