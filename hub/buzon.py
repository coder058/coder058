"""Lectura y escritura de mensajes del hub (archivos .md con cabecera simple)."""

import re
from datetime import datetime
from pathlib import Path

HUB = Path(__file__).resolve().parent
MENSAJES = HUB / "mensajes"
AGENTES = ["claude", "cursor", "grok", "sol"]
DESTINOS = AGENTES + ["todos"]

_CABECERA = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)


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
    if de not in AGENTES + ["humano"] or para not in DESTINOS + ["humano"]:
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


def prompt_para(agente: str) -> str:
    """Prompt listo para copiar/pegar en un chat web (Grok, Sol...)."""
    rol = (HUB / "agentes" / agente / "README.md").read_text(encoding="utf-8")
    pend = pendientes(agente)
    partes = [
        f"Eres el agente '{agente}' en un equipo de 4 IAs (claude, cursor, grok, sol).",
        "No tienes acceso a archivos: te paso tus mensajes aquí.",
        "Responde a cada mensaje en este formato exacto, uno detrás de otro:\n",
        "=== RESPUESTA A: <nombre_de_archivo> | PARA: <agente> ===\n<tu respuesta>\n",
        "--- TU ROL ---\n" + rol,
        f"--- TUS MENSAJES PENDIENTES ({len(pend)}) ---",
    ]
    for m in pend:
        partes.append(f"\n[{m['archivo']}] de {m['de']}:\n{m['cuerpo']}")
    if not pend:
        partes.append("(ninguno)")
    return "\n".join(partes)


def importar_respuesta(agente: str, texto: str) -> list[str]:
    """Convierte lo que pegas de un chat web en archivos de respuesta."""
    bloques = re.split(r"^=== RESPUESTA A:\s*(\S+)\s*\|\s*PARA:\s*(\w+)\s*===\s*$", texto, flags=re.M)
    creados = []
    if len(bloques) > 1:
        for i in range(1, len(bloques), 3):
            original, para, cuerpo = bloques[i], bloques[i + 1].lower(), bloques[i + 2]
            creados.append(escribir(agente, para if para in DESTINOS else "claude", cuerpo, original))
            marcar_respondido(original)
    else:
        # El chat no respetó el formato: una sola respuesta a quien le escribió primero.
        pend = pendientes(agente)
        para = pend[0]["de"] if pend else "claude"
        creados.append(escribir(agente, para, texto, pend[0]["archivo"] if pend else ""))
        for m in pend:
            marcar_respondido(m["archivo"])
    return creados
