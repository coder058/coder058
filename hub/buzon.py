"""Lectura y escritura de mensajes del hub (archivos .md con cabecera simple)."""

import re
from datetime import datetime
from pathlib import Path

HUB = Path(__file__).resolve().parent
MENSAJES = HUB / "mensajes"
OBJETIVO = HUB / "objetivo.md"
AGENTES = ["claude", "cursor", "grok", "sol"]
DESTINOS = AGENTES + ["todos", "humano"]

INICIO, FIN = "@@RESP", "@@FIN"  # marcas para recortar la respuesta de un chat web

_CABECERA = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)
_BLOQUE = re.compile(r"^=== PARA:\s*(\w+)\s*(?:\|\s*RESPONDE A:\s*(\S*)\s*)?===\s*$", re.M | re.I)


def leer(ruta: Path) -> dict:
    texto = ruta.read_text(encoding="utf-8")
    meta, cuerpo = {}, texto
    m = _CABECERA.match(texto)
    if m:
        for linea in m.group(1).splitlines():
            if ":" in linea:
                k, v = linea.split(":", 1)
                meta[k.strip()] = v.split("#", 1)[0].strip()
        cuerpo = m.group(2)
    return {
        "archivo": ruta.name,
        "de": meta.get("de", ""),
        "para": meta.get("para", ""),
        "estado": meta.get("estado", "pendiente"),
        "responde_a": meta.get("responde_a", ""),
        "cuerpo": cuerpo.strip(),
    }


def listar() -> list[dict]:
    return [leer(p) for p in sorted(MENSAJES.glob("*.md"))]


def pendientes(agente: str) -> list[dict]:
    return [
        m for m in listar()
        if m["estado"] == "pendiente" and m["para"] in (agente, "todos") and m["de"] != agente
    ]


def escribir(de: str, para: str, cuerpo: str, responde_a: str = "") -> str:
    if de not in AGENTES + ["humano"] or para not in DESTINOS:
        raise ValueError("agente desconocido")
    sello = datetime.now().strftime("%Y%m%d-%H%M%S")
    ruta = MENSAJES / f"{sello}-{de}-a-{para}.md"
    n = 1
    while ruta.exists():
        n += 1
        ruta = MENSAJES / f"{sello}-{n}-{de}-a-{para}.md"
    ruta.write_text(
        f"---\nde: {de}\npara: {para}\nestado: pendiente\nresponde_a: {responde_a}\n---\n\n{cuerpo.strip()}\n",
        encoding="utf-8",
    )
    return ruta.name


def marcar_respondido(archivo: str) -> None:
    ruta = MENSAJES / Path(archivo).name
    if ruta.exists():
        texto = ruta.read_text(encoding="utf-8")
        ruta.write_text(re.sub(r"^estado:.*$", "estado: respondido", texto, count=1, flags=re.M), encoding="utf-8")


def _historial(n: int = 12) -> str:
    ultimos = listar()[-n:]
    return "\n".join(f"- {m['archivo']} ({m['de']} → {m['para']}, {m['estado']})" for m in ultimos) or "(vacío)"


def prompt_para(agente: str, web: bool = False) -> tuple[str, list[str]]:
    """Prompt para un agente y la lista de mensajes que incluye.

    web=True: el agente es un chat sin acceso a archivos (Grok, ChatGPT), así que se
    le pide envolver la respuesta entre marcas para poder recortarla de la página.
    """
    rol = (HUB / "agentes" / agente / "README.md").read_text(encoding="utf-8")
    pend = pendientes(agente)
    p = [
        f"Eres el agente '{agente}' de un equipo de 4 IAs: claude (Head of Portfolio, el jefe), cursor, grok y sol (trabajadores).",
        "Te comunicas SOLO con bloques de mensaje. Cada bloque empieza con una línea así:",
        "=== PARA: <claude|cursor|grok|sol|todos|humano> | RESPONDE A: <archivo o vacío> ===",
        "y debajo va el texto del mensaje. Puedes escribir varios bloques seguidos.",
    ]
    if web:
        p.append(f"Escribe la línea {INICIO} antes del primer bloque y la línea {FIN} después del último.")
    p += ["", "--- TU ROL ---", rol]
    if agente == "claude":
        objetivo = OBJETIVO.read_text(encoding="utf-8") if OBJETIVO.exists() else "(sin objetivo)"
        p += [
            "--- OBJETIVO DEL EQUIPO (lo fija el humano) ---", objetivo,
            "--- ÚLTIMOS MENSAJES ---", _historial(),
            "Puedes leer cualquier archivo del repo (hub/mensajes/ incluido) para revisar el trabajo.",
            "Da la siguiente orden concreta a quien corresponda. Si el objetivo está cumplido o",
            "necesitas una decisión, escribe un bloque PARA: humano y no des más órdenes.",
        ]
    p.append(f"--- TUS MENSAJES PENDIENTES ({len(pend)}) ---")
    for m in pend:
        p.append(f"\n[{m['archivo']}] de {m['de']}:\n{m['cuerpo']}")
    if not pend:
        p.append("(ninguno)")
    return "\n".join(p), [m["archivo"] for m in pend]


def recortar_web(texto: str) -> str:
    """Saca lo que hay entre la última pareja @@RESP ... @@FIN."""
    fin = texto.rfind(FIN)
    ini = texto.rfind(INICIO, 0, fin)
    return texto[ini + len(INICIO):fin].strip() if 0 <= ini < fin else texto.strip()


def importar_respuesta(agente: str, texto: str, incluidos: list[str] | None = None) -> list[str]:
    """Convierte la salida de un agente en mensajes y marca como respondidos los que leyó."""
    if incluidos is None:
        incluidos = [m["archivo"] for m in pendientes(agente)]
    texto = texto.strip()
    creados = []
    partes = _BLOQUE.split(texto)
    if len(partes) > 1:
        for i in range(1, len(partes), 3):
            para, original, cuerpo = partes[i].lower(), partes[i + 1] or "", partes[i + 2].strip()
            if cuerpo:
                creados.append(escribir(agente, para if para in DESTINOS else "claude", cuerpo, original))
    elif texto:
        # No respetó el formato: todo va como respuesta a quien le escribió primero.
        primero = next((leer(MENSAJES / a) for a in incluidos if (MENSAJES / a).exists()), None)
        creados.append(escribir(agente, primero["de"] if primero else "claude", texto,
                                primero["archivo"] if primero else ""))
    for archivo in incluidos:
        marcar_respondido(archivo)
    return creados
