# Análisis del portfolio — 8 oct 2026 (Claude, Head of Portfolio)

Objetivo de Jordi: conseguir un buen trabajo en IA.
Este documento es una propuesta. `objetivo.md` solo cambia cuando Jordi la apruebe.

## Diagnóstico

**Lo fuerte (escaso en candidatos junior):**
- Rigor y honestidad verificables: preregistro, auditorías, postmortems y límites escritos.
- Sistemas reales en producción: VPS, CI, Docker, PostgreSQL, webhooks firmados.
- Una contribución aceptada en una librería de IA: Haystack #12635.
- Dominio real en logística, WMS y trading, que casi ningún ingeniero de IA tiene.

**Lo que frena:**
1. La web dice "Software developer", no un rol de IA. Un reclutador de IA no se ve reflejado.
2. Hay demasiados proyectos y apuntan en muchas direcciones. Cuatro son de trading
   (Polybow, Pattern Forge, ai-ocaml-bot, Event Desk), más energía, WMS, simulación y neurociencia.
3. El mejor proyecto de IA, **Event Desk**, no está en la web.
4. Las tarjetas abren con advertencias ("no prueba rentabilidad", "sin forecast").
   La honestidad es buena, pero el sitio para las advertencias es el caso de estudio, no el titular.
5. El orden propuesto (WMS, Polybow, Fly Brain) pone delante dos proyectos que no son de IA.

## Rol objetivo recomendado

**AI Engineer / LLM Applications Engineer**, con ángulo de "IA para operaciones"
(logística y finanzas). Es lo que la evidencia sostiene: RAG con evals (Info Desk),
pipeline LLM auditable en competición real (Event Desk), MCP (Relay, Event Desk),
evaluación rigurosa (Fly Brain) y PR en Haystack.

## Proyecto por proyecto

| Proyecto | Quién | Estado | Valor para IA | Recomendación |
|---|---|---|---|---|
| Event Desk | Codex (ChatGPT) | En producción; puntuación desde el 12 oct | **Máximo**: LLM + modelo local + evals prospectivas | Tarjeta n.º 1. No añadir funciones: mantenerlo vivo y publicar resultados reales cada semana |
| Info Desk | — | Publicado | Alto: RAG, citas, evals | Tarjeta n.º 2 |
| Fly Brain | Sol / ChatGPT | E1 cerrado (PR #1) | Alto para evaluación y ML | Tarjeta n.º 3. Congelar aquí y no abrir "memoria" ahora |
| Stockline (WMS) | Cursor | S2 hecho; el juego `/floor` falla | Hoy bajo (Rails, no IA) | Arreglar el juego y darle **modo agente**: ver abajo |
| Polybow | — | Cerrado | Medio: operación y datos | Tarjeta secundaria |
| Pattern Forge, Energy Monitor | — | Publicados | Bajo | "Otros proyectos" |
| ai-ocaml-bot | — | Congelado desde el 5 oct | Bajo | Dejarlo congelado; solo un enlace |
| Relay | — | Backend no público | Medio: MCP | Reutilizarlo para filtrar las ofertas de Grok |

### La idea para Stockline (que cuente para IA)
El simulador ya tiene sesiones y semillas. Repartir las 12 h de Cursor así:
- **~6 h:** arreglar la UI y la lógica del juego.
- **~6 h:** "modo agente": una API o servidor MCP para que un LLM juegue un turno
  (recibir, ubicar, picar, contar) con semilla fija, y una puntuación reproducible
  (pedidos servidos, errores de stock, roturas del ledger).

Resultado: un banco de pruebas de agentes en un almacén. Une tu experiencia en
logística con lo más demandado en IA ahora (agentes y evals).

Antes de hacerlo público, una decisión: `HANDOFF.md` dice que el código es "de la
empresa" y que está pensado para venderlo a FlexInd. Decidir si va público entero,
solo la demo, o en vídeo.

## Orden de la web propuesto
1. Event Desk · 2. Info Desk · 3. Fly Brain · 4. Stockline (con modo agente) ·
5. Polybow · después, "Otros": Pattern Forge, Energy Monitor, Relay, ai-ocaml-bot y DispatchOps.
Titular: "AI engineer — LLM systems that are evaluated, not assumed" (o similar), más
una línea sobre la experiencia en logística y cargo.

## Quién hace qué (desde el 11 oct, cuando vuelva el límite de Claude)

- **Claude (jefe):** fijar rol y mensaje; revisar cada entrega; aprobar los textos de la
  web y el CV (solo afirmaciones demostrables). Gastar el límite Pro en decisiones y
  revisiones, no en programar.
- **Cursor:** Stockline (12 h: juego y modo agente); después, las tarjetas y el orden de
  la web en `coder058/profile`.
- **Codex (Event Desk):** solo observación y operación hasta el 12 oct y después;
  informe semanal de resultados reales, sin funciones nuevas.
- **Sol (ChatGPT):** textos: tarjetas, resúmenes de casos, dos versiones del CV
  (AI Engineer / AI para logística) y la plantilla de carta. Fly Brain: solo el
  resumen para la web, sin experimentos nuevos.
- **Grok:** cuando la web esté lista: de las 1.500+ ofertas, sacar el top 50 por
  encaje real con el rol (motivo de cada una, requisitos que faltan, idioma, ubicación);
  luego investigar cada empresa para personalizar la candidatura.

## Calendario
- **9–10 oct:** Cursor en Stockline (no gasta el límite de Claude). Sol prepara borradores de textos.
- **11 oct:** Claude revisa, decide y ordena los cambios de la web y el CV.
- **12 oct:** empieza la puntuación de Event Desk. Primer dato real.
- **Semana del 13 oct:** web nueva publicada; Grok entrega el top 50; primeras 10 candidaturas personalizadas.
- **Después:** 10–15 candidaturas por semana, más 1–2 PR pequeños en librerías de IA
  (Haystack, LlamaIndex, DSPy…), que es la mejor señal para un reclutador.
