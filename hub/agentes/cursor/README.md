# Agente: cursor (Cursor IDE)

**Rol:** programador. Escribe y modifica código en este repo según las órdenes que recibe.
*(Se ajustará cuando definas el objetivo del equipo.)*

## Cómo se despierta
Cursor no tiene temporizador propio. Abre el repo en Cursor y en el chat Agent escribe:

```
Lee hub/README.md y hub/agentes/cursor/README.md y procesa tus mensajes pendientes en hub/mensajes/
```

Truco: guarda ese texto como regla en `.cursor/rules` o como prompt guardado, y
cuando `vigilar.py` o el panel te avisen de un pendiente para cursor, solo lo lanzas.
