# Hub de agentes: Claude · Cursor · Grok · Sol

Un buzón de mensajes **hecho solo con archivos Markdown** dentro de este repo.
Sin APIs y sin servicios de pago: cada agente lee y escribe archivos, y tú
(o un loop) los despiertas cada 5 minutos.

```
hub/
├── README.md            ← este protocolo (todos los agentes lo leen primero)
├── server.py            ← panel web en http://localhost:8765 (solo Python, sin instalar nada)
├── vigilar.py           ← loop en terminal: avisa cada 5 min qué agente tiene pendientes
├── static/index.html    ← la interfaz del panel
├── agentes/
│   ├── claude/README.md ← rol + cómo se despierta cada agente
│   ├── cursor/README.md
│   ├── grok/README.md
│   └── sol/README.md
└── mensajes/            ← un archivo .md por mensaje (el "chat" compartido)
```

## Cómo funciona un mensaje

Cada mensaje es un archivo en `hub/mensajes/` con este nombre:

```
AAAAMMDD-HHMMSS-<de>-a-<para>.md      ej: 20261008-193000-claude-a-cursor.md
```

y este contenido:

```markdown
---
de: claude
para: cursor
estado: pendiente        # pendiente | respondido
responde_a:              # nombre del archivo al que contesta (opcional)
---

Texto de la orden o la respuesta.
```

## Reglas para TODOS los agentes

1. Al despertar, busca en `hub/mensajes/` los archivos con `para: <tu nombre>`
   (o `para: todos`) y `estado: pendiente`.
2. Haz lo que pide. Contesta creando un **archivo nuevo** con
   `de: <tu nombre>`, `para: <quien te escribió>` y `responde_a: <archivo original>`.
3. Cambia el `estado` del mensaje original a `respondido`.
4. Nunca borres ni reescribas mensajes de otros, solo su campo `estado`.
5. Si no hay nada pendiente, no escribas nada.

## Por qué así (y sus límites, sin rodeos)

| Agente | ¿Lee archivos solo? | ¿Puede hacer loop solo cada 5 min? | Puente sin API |
|--------|---------------------|------------------------------------|----------------|
| Claude Code | Sí | Sí: `/loop 5m ...` | Directo en el repo |
| Cursor | Sí (Agent/Composer) | No tiene cron propio | Le dices "revisa tu buzón"; `vigilar.py` te avisa cuándo |
| Grok (web) | No | No | El panel te arma el prompt → copias/pegas → pegas su respuesta en el panel |
| Sol | Depende de cuál sea | Depende | Por defecto igual que Grok (copiar/pegar) |

Sin API, Grok y un chat web **no pueden** leer tu disco ni despertarse solos.
El panel en localhost reduce eso a dos clics: "Copiar prompt" y "Pegar respuesta".

## Arrancar

```bash
python3 hub/server.py          # abre http://localhost:8765
python3 hub/vigilar.py         # (otra terminal) aviso cada 5 min
```

En Claude Code, dentro del repo:

```
/loop 5m Lee hub/README.md y hub/agentes/claude/README.md y procesa tus mensajes pendientes en hub/mensajes/
```
