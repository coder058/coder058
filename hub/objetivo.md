# Objetivo del equipo (fijado por Jordi, 8 oct 2026)

Claude es el Head of Portfolio. Prioridad en este orden:

## 1. Cursor — el juego de almacén de Stockline (mínimo 12 h)
- Repo: `C:\Users\jamon\stockline` (GitHub `coder058/stockline`, privado).
- El "juego" es el simulador de la pantalla `/floor` (Warehouse Pilot Simulator):
  `app/views/pages/floor.html.erb`, `app/javascript/controllers/warehouse_controller.js`,
  `app/services/warehouse/*`, `app/assets/stylesheets/pages/floor.css`.
- Problemas que ve Jordi: **la UI no se ve bien** y **el juego no funciona bien**.
- Mínimo 12 horas de desarrollo solo en el juego antes de pasar a otra cosa.
  La hora de inicio es la que Cursor escriba en su `ACK #9` de `STATUS.md`.
- Reglas de siempre en ese repo: `docs/AGENT_BRIEF.md`, `docs/DEMO_SPEC.md`,
  ledger con Audit en 0, tests y RuboCop limpios, commits pequeños, nada con el nombre FlexInd.
- Al acabar las 12 h, y si el juego está bien: subirlo a GitHub. Hacer público el repo
  es decisión de Jordi; Claude se lo pregunta antes (mensaje PARA: humano).
- Después: reordenar las tarjetas de proyectos de la web `coder058/profile` (`index.html`)
  en este orden:
  1. **Stockline (WMS)**: tarjeta nueva, con su página `projects/stockline.html`.
  2. **Polybow**.
  3. **Fly Brain**: pasa de la caja "Research in progress" a tarjeta propia
     (su página `projects/fly-brain.html` ya existe).
  4. Los demás: Info Desk, Pattern Forge, Energy Monitor.
  Mismo estilo que las tarjetas actuales. Solo afirmar lo que cada repo demuestra.

## 2. Sol (ChatGPT) — su proyecto actual
Estaba con un proyecto de investigación/OCaml: `coder058/fly-brain` (Python) o
`coder058/ai-ocaml-bot` (OCaml). Primero que confirme cuál y en qué punto está; luego sigue.

## 3. Grok — en espera
Ya buscó y verificó más de 1.500 ofertas de trabajo. Ahora **no tiene tarea**.
No darle órdenes hasta que el portfolio esté listo (juego + web). Entonces: candidaturas.

## Cómo se comunica cada uno
- Jordi solo habla con Claude en el chat de http://localhost:8765.
- Todas las órdenes van por `hub/mensajes/`. El orquestador lleva cada orden a su
  trabajador y trae la respuesta: Cursor con `cursor-agent` en la carpeta de
  `carpetas.cursor` de `config.json`, y Grok y Sol en el navegador.
- La bandeja antigua de Stockline (`docs/INBOX_FROM_CLAUDE.md`) queda como historial.
