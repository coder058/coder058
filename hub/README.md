# Hub de agentes: Claude (Head of Portfolio) manda · Cursor, Grok y Sol (ChatGPT) trabajan

**¿Qué le pego a cada uno?** → [`PEGAR.md`](PEGAR.md)

Un equipo de 4 IAs que se habla **con archivos Markdown** dentro de este repo,
sin APIs de pago. Claude da las órdenes, los otros las hacen y le devuelven el
resultado, y Claude revisa y da la siguiente. Se repite cada 2 minutos, sin parar.

```
           ┌──────────── objetivo.md (lo escribes tú)
           ▼
        claude ──órdenes──► cursor (código)   ─┐
          ▲   └──órdenes──► grok   (investiga) ├─ resultados ─► claude
          │   └──órdenes──► sol    (ChatGPT)  ─┘
          └── PARA: humano ──► tú (cuando acaba o necesita decidir)
```

## Cómo se conecta cada uno (sin API)

| Agente | Cómo lo despierta `orquestador.py` | Qué necesitas |
|--------|------------------------------------|---------------|
| claude | `claude -p` (Claude Code, modo sin ventana) | Claude Code instalado con tu suscripción |
| cursor | `cursor-agent -p --force` (Cursor CLI) | Cursor CLI instalado y sesión iniciada |
| grok   | Abre grok.com en tu navegador, pega la orden, lee la respuesta | Tu cuenta de Grok |
| sol    | Abre chatgpt.com en tu navegador, pega la orden, lee la respuesta | Tu cuenta de ChatGPT |

## Uso normal: solo hablas con Claude

```bash
python3 hub/server.py      # abre http://localhost:8765
```

Escribes a Claude en el chat. Él da las órdenes, el orquestador (va dentro del
servidor) las lleva a Cursor, Grok y Sol, recoge sus respuestas y Claude te
resume lo que hicieron, en el mismo chat. A la derecha ves quién trabaja.

- Cuando le escribes, Claude despierta al instante (no espera los 2 min).
- `"autonomo": false` en `config.json`: Claude solo actúa cuando le escribes tú
  o le responde un trabajador. Con `true` sigue solo con `objetivo.md` cada 2 min.
- `"carpetas": {"cursor": "C:\\Users\\jamon\\stockline"}`: carpeta donde trabaja Cursor.
- `python3 hub/server.py --sin-orquestador`: solo mirar, sin despertar a nadie.

## Instalación (una vez, en tu PC)

```bash
pip install playwright                 # para manejar el navegador (gratis)
python3 -m playwright install chromium # solo si no tienes Google Chrome
curl https://cursor.com/install -fsS | bash   # Cursor CLI; luego: cursor-agent login
python3 hub/orquestador.py --login     # inicia sesión en Grok y ChatGPT, pulsa Enter
```

Para pararlo: `Ctrl+C`, o crea el archivo `hub/PARAR`.

## Qué pasa en cada ronda

1. Claude lee lo que le escribiste y da las órdenes. Te contesta qué pidió y a quién.
2. Cursor, Grok y Sol hacen sus órdenes y le responden a Claude.
3. Claude revisa los resultados y te los resume en el chat (o manda correcciones).
4. Mientras alguien tenga algo pendiente, se repite enseguida. Si no, espera 2 min
   o hasta que le vuelvas a escribir.

## Formato de los mensajes

Un archivo por mensaje en `hub/mensajes/`, p. ej. `20261008-193000-claude-a-cursor.md`:

```markdown
---
de: claude
para: cursor
estado: pendiente        # pendiente | respondido
responde_a:              # archivo al que contesta (opcional)
---

Texto de la orden o del resultado.
```

Los agentes no escriben estos archivos a mano: devuelven bloques
`=== PARA: <agente> | RESPONDE A: <archivo> ===` y el orquestador los convierte.

## Cosas que debes saber

- **Grok y ChatGPT por navegador:** sus condiciones de uso no permiten
  automatizar la web, y podrían limitar o bloquear tu cuenta. Por eso el loop va
  cada 2 min y no más rápido. Si cambian su página, puede que haya que ajustar
  `CAMPOS` en `navegador.py`. Si falla, el panel tiene "Copiar prompt" y
  "Pegar respuesta" para hacerlo a mano.
- **Límites gratis:** cada ronda gasta mensajes de tu plan de Claude, Cursor,
  Grok y ChatGPT. En los planes gratis se acaban rápido. `max_rondas` en
  `config.json` pone un tope (0 = sin tope). `manual` lista los agentes que
  manejas tú (p. ej. `["cursor"]` si lo dejas en loop dentro de Cursor).
- **Cursor con `--force`** cambia archivos sin preguntarte. Trabaja en una rama
  de git para poder deshacerlo.
- **Claude** solo puede leer (`Read,Glob,Grep`). Nunca modifica nada él mismo.
