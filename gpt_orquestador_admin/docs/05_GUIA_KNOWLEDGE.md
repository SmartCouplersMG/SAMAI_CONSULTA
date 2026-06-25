# Guía de archivos de conocimiento (Knowledge)

Coloca en la carpeta `knowledge/` los documentos que el GPT usará como base. Súbelos en el
campo **Knowledge** del GPT Builder. Recomendado en PDF o Markdown limpio (texto seleccionable,
no escaneado).

## Mínimo indispensable

| Archivo sugerido | Contenido | Fuente oficial |
|---|---|---|
| `constitucion_politica.pdf` | Constitución Política (énfasis art. 90) | Gestor Normativo Función Pública |
| `ley_1437_2011_cpaca.pdf` | CPACA completo y vigente | `funcionpublica.gov.co/eva/gestornormativo/norma.php?i=41249` |
| `cpaca_indice_articulos.md` | Índice de artículos clave por fase | (lo elaboras tú) |

## Muy recomendable

- `codigo_general_proceso.pdf` — régimen probatorio supletorio.
- `lineas_jurisprudenciales.md` — resúmenes propios de líneas del Consejo de Estado por tema
  (falla del servicio, daño especial, riesgo excepcional, privación injusta de la libertad,
  responsabilidad médica estatal, etc.). **No** copies sentencias inventadas; solo las que
  verifiques en fuente oficial, con su radicado y enlace.
- `glosario_dano_antijuridico.md` — definiciones operativas (daño cierto/personal/antijurídico,
  imputación fáctica/jurídica, nexo causal, eximentes).
- `plantilla_providencia.md` — estructura de las 23 secciones para uniformar la redacción.

## Buenas prácticas

- Prefiere fuentes oficiales y versiones **vigentes**; anota la fecha de descarga.
- Evita PDFs escaneados sin OCR (el GPT no los lee bien). Si solo tienes escaneo, pásalo por OCR.
- No incluyas datos personales reales de expedientes en el conocimiento del GPT.
- Mantén un archivo `FUENTES.md` con la URL y fecha de cada documento para trazabilidad.

> Importante: el conocimiento cargado **complementa** pero no sustituye la verificación en vivo.
> El prompt obliga a marcar como "no verificada" cualquier providencia que no se confirme en la
> fuente oficial.
